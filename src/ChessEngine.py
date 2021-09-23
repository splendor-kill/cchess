class ChessEngine:
    def __init__(self, human_color='b'):
        self.human_color = human_color

    def human_move(self, coord, mcts_or_net):
        pass

    def check_end(self):
        pass

    def get_hint(self, mcts_or_net, reverse, disp_mcts_msg_handler):
        pass

    def select_move(self, mcts_or_net):
        pass
