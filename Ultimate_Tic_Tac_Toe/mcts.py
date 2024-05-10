from abc import ABC, abstractmethod
from state import State
import itertools as it
import math
import random
import time


# need modifications for whose perspective you're playing from
class Node:
    def __init__(self, state, parent=None, action = None ):
        self.state = state
        self.action = action
        self.parent = parent
        self.children = []
        self.value = 0
        self.visits = 0

    def add_child(self, child):
        self.children.append(child)
   
   
def mcts_policy(state):
    time = .1

    # print("player:", state.current_player)
    move = helper(time, state)
    # state.get_next_state(move).print_board()
    # print(move)
    return move
    

def helper(duration, position):
        
    root = Node(position)
    
    start_time = time.time()
    current_time = time.time()
    loop = 0
    while (current_time - start_time) < duration:
        # returns the leaf node selected via UCB
        leaf = traverse(root)
        if not leaf.state.is_terminal()[0]:
            # print("not sterminal")
            if leaf.visits > 0:
                leaf = expand(leaf)
                # print("leaf node:", leaf)
            # run randomly to terminal states, updates visit and reward counters
        reward = simulate(leaf)
        # propagate changes up to root
        update(leaf, reward)
        # print("reward:", reward)
        current_time = time.time()
        loop +=1
    return last_action(root)
    
def traverse(root):
    # print("traversing")
    current = root
    # current.state.print_board()
    # print("children:", len(current.children))
    while len(current.children)!= 0:
        # picks the best action at each stage
        next_node = UCB(current)
        current = next_node 
        # print("current_player at node:", current.state.current_player)
    leaf = current
    # print("post_traversal")
    # leaf.state.print_board()
    return leaf

def expand(leaf):
    # print("expanding")
    if len(leaf.children) == 0:
        action_list = leaf.state.get_legal_actions()
        # print("actions:", action_list)
        for action in action_list:
            # successor function tells you the resulting position from an action at that position
            # print("action:", action)
            # child is already a sate
            next_state = leaf.state.get_next_state(action)
            # child.action = action
            # print(child.action)
            # print("new_state")
            # child.print_board()
            leaf.add_child(Node(next_state, leaf, action))
    # return arbitrary child
    # print(f"Expanded {len(leaf.children)} children.")
    arbitrary_child = random.choice(leaf.children)
    # print("selected random move:")
    # arbitrary_child.state.print_board()
    return arbitrary_child
         
# simulates game from a leaf
def simulate(leaf):
    # print("simulating")
    current = leaf.state
    # random path to erminal state
    while not current.is_terminal()[0]:
        options = current.get_legal_actions()
        next_action = random.choice(options)
        next_state = current.get_next_state(next_action)
        next_state.action = next_action
        # print("simulate", next_state.action)
        current = next_state
    # current.print_board()
    winner = current.check_big_winner()
    if winner == "X":
        reward = 1
    elif winner == "O":
        reward = -1
    else:
        # print("draw")
        reward = 0
    return reward
                
# propagate reward from leaf node to root node
def update(leaf, reward):
    # print("updating")
    current = leaf
    # iterate until root; root node should be only node without a parent, 
    while current != None:
        current.visits += 1
        current.value += reward
        current = current.parent
    
def UCB(leaf):
    children = leaf.children
    best_move = None


    if leaf.state.current_player== 'X':
        max_score = float("-inf")

        for node in children:
            v = node.value
            N = node.parent.visits
            n = node.visits

            if n == 0:
                score = float("inf")
            else:
                score = v/n + (1.41 *  math.sqrt(math.log(N)/n))

            if score > max_score:
                max_score = score
                best_move = node


    else:
        min_score = float("inf")

        for node in children:
            v = node.value
            N = node.parent.visits
            n = node.visits

            if n == 0:
                score = float("-inf")
            else:
                score = v/n - (1.41 * math.sqrt(math.log(N)/n))

            if score < min_score:
                min_score = score
                best_move = node
        
    return best_move

def last_action(root):
    children = root.children
    # print(f"Total Children: {len(children)}")
    best_move = None

    if root.state.current_player == 'X':
        max_score = float("-inf")
        # print([node.state for node in children])
        # print("value:",[node.value for node in children])
        # print("visits:",[node.visits for node in children])
        # print("first max:", max_score)
        
        for node in children:
            if node.visits > 0:
                # print("iterating")
                if node.value/node.visits > max_score and node.visits > 0:
                    max_score = node.value/node.visits
                    best_move = node
                
    else:
        min_score = float("inf")
        for node in children:
            if node.visits > 0:
                if node.value/node.visits < min_score:
                    min_score = node.value/node.visits
                    best_move = node

    # best_move.state.print_board()
    return best_move.action
