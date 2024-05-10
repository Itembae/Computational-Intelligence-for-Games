import random
from state import State

class HeuristicPlayer:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def choose_move(self, state):
        actions = state.get_legal_actions()

        score_dict = {}
        for action in actions:
            score_dict[action] = 0
        
        for action in actions:
            # check if it's a center piece
            if action[1] == (1, 1):
                score_dict[action] += 0.4
            
            # corner pieces are also better than the others
            if action[1] == (0, 0) or action[1] == (0, 2) or action[1] == (2, 0) or action[1] == (2, 2):
                score_dict[action] += 0.1
            
            next_state = state.get_next_state(action)

            # check if player wins the board
            if next_state.check_small_winner(next_state.board[action[0]]):
                score_dict[action] += 1
            
            if next_state.check_big_winner():
                score_dict[action] += float('inf')
            
            flag = 0
            other_players_actions = next_state.get_legal_actions()
            for other_action in other_players_actions:
                two_next_state = next_state.get_next_state(other_action)

                if two_next_state.check_small_winner(two_next_state.board[other_action[0]]):
                    flag = 1
                
                if two_next_state.check_big_winner():
                    flag = 2
            
            # This means that the other player can win a grid in the next action
            if flag == 1:
                score_dict[action] -= 1
            
            if flag == 2:
                score_dict[action] -= 99

            # check if next subgrid is taken or full
            #print(action)
            next_board_num = 3*action[1][0] + action[1][1]

            next_sub_board = state.board[next_board_num]
            if state.check_small_winner(next_sub_board) or state.is_full(next_sub_board):
                score_dict[action] -= 0.5
            
            # check if can block player in current sub board
            board_num = action[0]
            row = action[1][0]
            col = action[1][1]
            other_symbol = 'X'
            if self.symbol == 'X':
                other_symbol == 'O'

            sub_board = state.board[board_num]
            if col == 0:
                if sub_board[row][1] == other_symbol and sub_board[row][2] == other_symbol:
                    score_dict[action] += 0.2
            elif col == 1:
                if sub_board[row][0] == other_symbol and sub_board[row][2] == other_symbol:
                    score_dict[action] += 0.2
            else:
                if sub_board[row][0] == other_symbol and sub_board[row][1] == other_symbol:
                    score_dict[action] += 0.2
            
            if row == 0:
                if col == 0:
                    if sub_board[1][1] == other_symbol and sub_board[2][2] == other_symbol:
                        score_dict[action] += 0.2
                elif col == 2:
                    if sub_board[1][1] == other_symbol and sub_board[2][0] == other_symbol:
                        score_dict[action] += 0.2
                if sub_board[1][col] == other_symbol and sub_board[2][col] == other_symbol:
                    score_dict[action] += 0.2
            elif row == 1:
                if sub_board[0][col] == other_symbol and sub_board[2][col] == other_symbol:
                    score_dict[action] += 0.2
            else:
                if col == 0:
                    if sub_board[1][1] == other_symbol and sub_board[0][2] == other_symbol:
                        score_dict[action] += 0.2
                elif col == 2:
                    if sub_board[1][1] == other_symbol and sub_board[0][0] == other_symbol:
                        score_dict[action] += 0.2

                if sub_board[0][col] == other_symbol and sub_board[1][col] == other_symbol:
                    score_dict[action] += 0.2
            
            
        
        max_val = float('-inf')
        max_state = None
        for key, val in score_dict.items():
            if val > max_val:
                max_val = val
                max_state = key
        

            
            
            #print(action[1])
        return max_state
