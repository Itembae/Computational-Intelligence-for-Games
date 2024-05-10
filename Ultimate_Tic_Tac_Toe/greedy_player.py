import random

class GreedyPlayer:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def choose_move(self, state):
        available_moves = state.get_legal_actions()
        for move in available_moves:
            next_state = state.get_next_state(move)

            if next_state.check_small_winner(next_state.board[move[0]]):
                return move
    
        if available_moves:
            return random.choice(available_moves)