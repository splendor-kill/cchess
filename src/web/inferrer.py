from logging import getLogger
from multiprocessing import Manager

from flask import Flask, request, jsonify
from keras import backend as K
from xiangqi import Env, Camp, get_iccs_action_space

import sys

sys.path.append('../')

from agent.helper import flip_ucci_labels
from agent.player_mcts import MCTSPlayer
from common.utils import load_cfg
from config import cfg
from model.nn import NNModel

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
model = NNModel(cfg)
model.load(nn_model_config_path, nn_model_weight_path)
model.session = K.get_session()
model.graph = model.session.graph

app = Flask(__name__)

m = Manager()
pipes_bundle = m.list([model.get_pipes(cfg.play.search_threads)
                       for _ in range(cfg.play.max_processes)])

pipes_strand = pipes_bundle.pop()

players = {Camp.RED: MCTSPlayer(Camp.RED, cfg, pipes_strand=pipes_strand, play_config=cfg.play),
           Camp.BLACK: MCTSPlayer(Camp.BLACK, cfg, pipes_strand=pipes_strand, play_config=cfg.play)
           }


@app.route('/play', methods=["GET", "POST"])
def play():
    data = request.get_json()
    print(data["position"])
    env = Env.from_fen(data["position"])
    for p in players.values():
        p.env = env
    ob = env.reset()
    action = players[env.cur_player].make_decision(**ob)
    return jsonify(action)
