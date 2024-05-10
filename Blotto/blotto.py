import sys
import itertools
from scipy import optimize
# use numpy tool package as well as scipy to address space and efficiency issues 

def main():

    inputs = len(sys.argv)
    task = sys.argv[1]

    if sys.argv[2] == "--tolerance":
        tolerance = float(sys.argv[3])
        game_type = sys.argv[4]
        # print("tolerance", tolerance)

        if task == "--find":
            units = int(sys.argv[6])
            # array of battlefield points
            battlefield = []
            for i in range(7, inputs):
                battlefield.append(int(sys.argv[i]))
            find(units, battlefield, game_type, tolerance)

        else: 
            # how to parse stdin for battlefield reading
            strategies = []
            battlefield = []
            for i in range(5, inputs):
                battlefield.append(int(sys.argv[i]))
            s_input = sys.stdin 
            
            # each line is a strategy and the probability with which it is played.
            lines = []
            for line in s_input:
                lines.append(line)
            
            units = 0
            strategies = []
            probabilities = []
            for line in lines:
                # distributions are in the first n-1 entries
                values = line.split(",")
                length = len(values)
                units = 0
                strategy = []
                # sum up how many units were played
                for i in range(length - 1):
                    strategy.append(int(values[i]))
                    units += int(values[i])

                probability = float(values[length - 1])
                strategy.append(probability)
                strategies.append(strategy)
                probabilities.append(probability)

            verify(strategies, units, battlefield, game_type, probabilities, tolerance) 
            ##### PARSE strategies and probability they are played with.

    # if no tolerance argument is given
    else:
        game_type = sys.argv[2]
        if task == "--find":
            units = int(sys.argv[4])
            battlefield = []
            for i in range(5, inputs):
                battlefield.append(int(sys.argv[i]))
            find(units, battlefield, game_type)

        # VERIFY
        else: 
            battlefield = []
            for i in range(3, inputs):
                battlefield.append(int(sys.argv[i]))
            s_input = sys.stdin 
            
            # each line is a strategy and the probability with which it is played.
            lines = []
            for line in s_input:
                lines.append(line)
            
            units = 0
            strategies = []
            probabilities = []
            for line in lines:
                # distributions are in the first n-1 entries
                values = line.split(",")
                length = len(values)
                units = 0
                strategy = []
                # sum up how many units were played
                for i in range(length - 1):
                    strategy.append(int(values[i]))
                    units += int(values[i])

                probability = float(values[length - 1])
                strategy.append(probability)
                strategies.append(strategy)
                probabilities.append(probability)

            verify(strategies, units, battlefield, game_type, probabilities)
            

def verify(strategies, units, battlefield, game_type, probabilities, tolerance = 1e-6):
        # acceptable threshold: 0.5 * total sum * sum(probs)
        pure_strategies = combinator(units, battlefield)
        length = len(battlefield)


        if game_type == "--win":


            for pure_strategy in pure_strategies:
                # print(pure_strategy)

                weighted_wins = 0
                for strategy in strategies:
                    score = 0

                    for battle in range(length):
                        if strategy[battle] > pure_strategy[battle]:
                            score += battlefield[battle]
                        elif strategy[battle] == pure_strategy[battle]:
                            score += (.5 * battlefield[battle])
                        else:
                            score += 0
                    if score > (sum(battlefield)*.5):  
                        win = 1
                    elif score < sum(battlefield)*0.5:
                        win = 0
                    else: 
                        win = 0.5
                    weighted_wins += win * strategy[length]

                if weighted_wins < 0.5*(sum(probabilities)**2) - tolerance:
                    # print("wins",weighted_wins)
                    print("FAIL")
                    return
            print("PASSED")
            
        elif game_type == "--lottery":
            length = len(battlefield)

            weighted_score = 0
            for pure_strategy in pure_strategies:
                for strategy in strategies:
                    score = 0
                    for battle in range(length):
                        if strategy[battle] == 0 and pure_strategy[battle] == 0:
                            win_probability = 1/2
                        else:
                            win_probability = (strategy[battle]**2)/ ((strategy[battle]**2)+(pure_strategy[battle]**2))
                        score += battlefield[battle] * win_probability  
                    weighted_score += score * strategy[length]
                # how do you incorporate tolerance here
                if weighted_score < (0.5 * sum(battlefield) * (sum(probabilities))**2 - tolerance):
                    print("FAIL")
                    return
            print("PASSED")


        elif game_type == "--score":
            weighted_score = 0
            for pure_strategy in pure_strategies:
                for strategy in strategies:
                    score = 0
                    for battle in range(length):
                        if strategy[battle] > pure_strategy[battle]:
                            score += battlefield[battle]
                        elif strategy[battle] == pure_strategy[battle]:
                            score += (.5 * battlefield[battle])
                        else:
                            score += 0
                    weighted_score += score * strategy[length]
                if weighted_score < (0.5 * sum(battlefield) * (sum(probabilities))**2 - tolerance):
                    print("FAIL")
                    return
            print("PASSED")




def find(units, battlefields, game_type, tolerance = 1e-6):
    strategy = combinator(units, battlefields)
    c = [1] * len(strategy)
    b = [-.5] *len(strategy)
    
    if game_type == "--win":
        win_matrix = find_wins(strategy, battlefields)
        A = win_matrix
        
    elif game_type == "--lottery":
        lottery_matrix = find_lottery(strategy, battlefields)
        A = lottery_matrix

    elif game_type == "--score":
        score_matrix = find_score(strategy, battlefields)
        A = score_matrix

    answer = optimize.linprog(c, A_ub=A, b_ub=b, bounds=(0,1))

    eq = answer.x/answer.fun

    for i in range(len(eq)):
        if eq[i] > tolerance:
            for number in strategy[i]:
                print(number, end = ",")
            print(round(eq[i],20))

    return 0



# returns every possible pure strategy
def combinator(units, battlefields):
    m = len(battlefields)
    n = units
    dividers = itertools.combinations(range(n + m -1), m - 1)
    strategies = []
    # iterate over list of combinations
    for divider in dividers:
        length = len(divider)
        start = -1
        distribution = []
        allocated = 0
        # convert dividers to troop distributions
        for i in range(length):
            troops = abs(divider[i] - start - 1)
            distribution.append(troops)
            start = divider[i]
            allocated += troops
        distribution.append(units - allocated)
        strategies.append(distribution)
        # print(distribution)

    return strategies

def find_wins(strategy, battlefields):
    length = len(strategy)
    nums = len(battlefields)
    war_total = sum(battlefields)
    win_matrix = [[0]*length for i in range(length)]
    for i in range(length):
        for j in range(length):
            p1_score = 0
            # can avoid using p2 score by calculating war total
            for battle in range(nums):
                if strategy[i][battle] > strategy[j][battle]:
                    p1_score += battlefields[battle]
                elif strategy[i][battle] < strategy[j][battle]:
                    p1_score += 0
                else:
                    p1_score += .5 * battlefields[battle]
            p2_score = war_total * .5
            if p1_score > p2_score:
                win_matrix[j][i] = 1 *-1
            elif p1_score < p2_score:
                win_matrix[j][i] = 0 *-1
            else: 
                win_matrix[j][i] = 0.5 *-1
    return win_matrix


def find_lottery(strategy, battlefields):
    length = len(strategy)
    nums = len(battlefields)
    lottery_matrix = [[0]*length for i in range(length)]
    for i in range(length):
        for j in range(length):
            p1_score = 0
            for battle in range(nums):
                if strategy[i][battle] == 0 and strategy[j][battle] == 0:
                    win_probability = 1/2
                else:
                    win_probability = (strategy[i][battle]**2)/ ((strategy[i][battle]**2)+(strategy[j][battle]**2))
                p1_score += battlefields[battle] * win_probability
            lottery_matrix[j][i] = p1_score *-1
    return lottery_matrix


def find_score(strategy, battlefields):
    length = len(strategy)
    nums = len(battlefields)
    score_matrix = [[0]*length for i in range(length)]
    for i in range(length):
        for j in range(length):
            p1_score = 0
            for battle in range(nums):
                if strategy[i][battle] > strategy[j][battle]:
                    p1_score += battlefields[battle]
                elif strategy[i][battle] < strategy[j][battle]:
                    p1_score += 0
                else:
                    p1_score += .5 * battlefields[battle]
            score_matrix[j][i] = p1_score *-1

    return score_matrix


if __name__ == "__main__":
    main()