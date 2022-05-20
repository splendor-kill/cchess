from model.nn import NNModel
from config import cfg
from common.utils import load_cfg
from agent.player_mcts import MCTSPlayer
from agent.helper import flip_ucci_labels
import os
import sys
from logging import getLogger
from multiprocessing import Manager

from keras import backend as K
from flask import Flask, jsonify, request
from xiangqi import Camp, Env, get_iccs_action_space

sys.path.append('../')


logger = getLogger(__name__)
config_path = '../config.yaml'
cfg.update(load_cfg(config_path))
cfg.labels = get_iccs_action_space()
cfg.n_labels = len(cfg.labels)
print(f'action space size: {cfg.n_labels}')
flipped = flip_ucci_labels(cfg.labels)
cfg.unflipped_index = [cfg.labels.index(x) for x in flipped]

nn_model_config_path = cfg.resource.model_best_config_path
nn_model_weight_path = cfg.resource.model_best_weight_path
print(os.path.abspath(nn_model_config_path))
print(os.path.exists(nn_model_weight_path))

model = NNModel(cfg)
model.load(nn_model_config_path, nn_model_weight_path)
model.session = K.get_session()
model.graph = model.session.graph

app = Flask(__name__)

m = Manager()
pipes_bundle_r = m.list([model.get_pipes(cfg.play.search_threads) for _ in range(cfg.play.max_processes)])
pipes_strand_r = pipes_bundle_r.pop()

pipes_bundle_b = m.list([model.get_pipes(cfg.play.search_threads) for _ in range(cfg.play.max_processes)])
pipes_strand_b = pipes_bundle_b.pop()


players = {
    Camp.RED: MCTSPlayer(Camp.RED, cfg, pipes_strand=pipes_strand_r, play_config=cfg.play),
    Camp.BLACK: MCTSPlayer(Camp.BLACK, cfg, pipes_strand=pipes_strand_b, play_config=cfg.play)
}


@app.route('/play', methods=['GET', 'POST'])
def play():
    data = request.get_json()
    fen = data['position']
    # print(fen)
    fen += ' - - 0 1'  # adapt to Xiangqi
    env = Env.from_fen(fen)
    for p in players.values():
        p.env = env
    ob = env.reset()
    action = players[env.cur_player].make_decision(**ob)
    return jsonify({'move': action})
