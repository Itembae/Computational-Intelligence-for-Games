import mcts
class MCTSPlayer:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


    def choose_move(self, state):
        available_moves = state.get_legal_actions()
        if available_moves:
            return mcts.mcts_policy(state)
        return None