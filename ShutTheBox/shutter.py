import sys
import itertools
#can compute P1 expected wins = 1 - P2 expected wins

# optimal move is the one that maximized expected wins

# calculate P2 expected wins first, use that to calculate P1s


#leaf and branch nodes: leaves have given state, branch nodes require us rolling and feeding that in


rolls = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7:6, 8:5, 9:4, 10: 3, 11:2, 12:1}
memo = {}

def main():

    player = sys.argv[1]
    task = sys.argv[2]
    position = sys.argv[3]
    tiles = convert(position)

    if player == "--one":
        opp_score = 0
        if task == "--move":
            roll = int(sys.argv[4])
            best_move = move(tiles, opp_score, roll)
            print(best_move)
        else:
            expected_wins = evaluate_one(tiles)
            # print(round(expected_wins,6))
            print('{0:0.6f}'.format(round(expected_wins, 6)))

    else:
        opp_score = int(sys.argv[4])
        if task == "--move": 
            roll = int(sys.argv[5])
            best_move = move(tiles, opp_score, roll)
            print(best_move)
        else:
            expected_wins = evaluate(tiles, opp_score)
            # print(round(expected_wins,7))
            print('{0:0.6f}'.format(round(expected_wins, 6)))
    
def move(tiles, opp_score, rolled):
    # best move is the one that returns the highest score
    if opp_score == 0:
        best_move = score_one(tiles, rolled, 1)
    else: 
        best_move = score(tiles, rolled, opp_score, 1)
    return best_move
    
def evaluate(tiles, opp_score):
    key = (tuple(tiles), opp_score)

    if key in memo:
        expected_score = memo[key]

    else:
        if sum(tiles) < opp_score: 
            expected_score = 1
        elif sum(tiles) <= 6:
            expected_score = 0
            for i in range(1,7):
                expected_score += 1/6 * score(tiles, i, opp_score)
        else:
            expected_score = 0
            for i in range(2,13):
                expected_score += (rolls[i]/36) * score(tiles, i, opp_score)
        memo[key] = expected_score
    return expected_score

def score(tiles, rolled, opp_score, flag = 0):
    # create array of possible moves
    legal_moves = check_options(tiles, rolled)

    max_score = 0
    best_move = []
    
    if len(legal_moves)==0:
        if sum(tiles) == opp_score:
            return 0.5
        elif sum(tiles) > opp_score:
            return 0
    
    for move in legal_moves: 
        new_state = tiles.copy()
        for flipped_tile in move:
            new_state.remove(flipped_tile)
        expected_wins = evaluate(new_state, opp_score)

        if expected_wins > max_score:
            max_score = expected_wins
            # print("score:", max_score)
            best_move = move
            # print("move:", move)

    if flag == 1:
        # print("flagged")
        return best_move
    return max_score



def evaluate_one(tiles):
    #can you memoize for player one
    key = (tuple(tiles), 0)

    if key in memo:
        expected_score = memo[key]

    else:
        # box closed, you win
        if len(tiles) == 0: 
            expected_score = 1
        # check probability for one dice
        elif sum(tiles) <= 6:
            expected_score = 0
            for i in range(1,7):
                expected_score += 1/6 * score_one(tiles, i)
        else:
            expected_score = 0
            for i in range(2,13):
                expected_score += (rolls[i]/36) * score_one(tiles, i)

    memo[key] = expected_score
    return expected_score


def score_one(tiles, rolled, flag = 0):
    # create array of possible moves
    legal_moves = check_options(tiles, rolled)

    max_score = 0
    best_move = []

    # if you are shutting the box, calculate player two's expected score.
    if len(legal_moves) == 0:
        #run for player two's expected wins
        max_score = 1 - evaluate([i for i in range(1,10)], sum(tiles))
    
    for move in legal_moves: 
        new_state = tiles.copy()
        for flipped_tile in move:
            new_state.remove(flipped_tile)
        expected_wins = evaluate_one(new_state)

        if expected_wins > max_score:
            max_score = expected_wins
            best_move = move
    if flag == 1:
        return best_move
    return max_score


def check_options(tiles, rolled):
    valid = []
    subsets = []
    for i in range(1,5):
        for x in itertools.combinations(tiles, i):
            subsets.append(list(x))
    for combo in subsets:
        if sum(combo) == rolled:
            valid.append(combo)
    return valid

def convert(string):
    array = []
    for letter in string:
        array.append(int(letter))
    return array

if __name__ == "__main__":
    main()