
import random
import time

def q_learn(model, duration):
    rows = 9 # Number of rows
    columns = model.offensive_playbook_size() # Number of columns

    q = [[0 for _ in range(columns)] for _ in range(rows)]
    alpha = [[0.1 for _ in range(columns)] for _ in range(rows)]

    probability = 0.0001
    start_time = time.time()
    current_time = time.time()

    while (current_time - start_time) < duration:
        state = model.initial_position()
        
        while model.game_over(state) is False:
            index = partition(state)
            action = best_action(index, q, probability, columns)
            # state resulting from action taken
            next_state, _ = model.result(state, action)

            if model.game_over(next_state) is True:
                if model.win(next_state) is True:
                    reward = 1
                else:
                    reward = -1
                q[index][action] += alpha[index][action]*(reward - q[index][action])
            else:
                next_index = partition(next_state)
                next_action = best_action(next_index, q, probability, columns)
                q[index][action] += alpha[index][action]*(q[next_index][next_action] - q[index][action])
               
            alpha[index][action] *= .999999
            state = next_state
        current_time = time.time()

    play = [0]*9

    for bucket in range(rows):
        play[bucket] = best_action(bucket, q, 0, columns)
    
    def function(state):
        index = partition(state)
        return play[index]
    
    return function
                



def best_action(index, q, probability, actions):
    #return the action that maximized q value
    max_score = float("-inf")
    best_action = None

    for action in range(actions):
        if q[index][action] > max_score:
            best_action = action
            max_score = q[index][action]

    # WARNING: check random function
    if random.random() <= (1 - probability):
        return best_action
    else:
        return random.randint(0, 2)
        

def partition(state):
    # (yards-to-score, downs-left, distance, ticks

    # WARNING: make sure yards-to-score and first down are not mixed up here
    yards_to_score = state[0]
    downs_left = state[1]
    yards_to_first_down = state[2]
    time_left = state[3]

    x_axis = yards_to_first_down/downs_left
    y_axis = yards_to_score/time_left

    if 0 <= x_axis <= 2:
        index = 0
    elif 2 < x_axis < 5.1:
        index = 1
    else:
        index = 2
    
    # WARNING: reconfigure bounds
    if 0 <= y_axis <= 2:
        index += 0
    elif 2 < y_axis <= 5:
        index += 3
    else:
        index += 6

    return index