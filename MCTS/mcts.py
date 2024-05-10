from abc import ABC, abstractmethod
from game import State
import itertools as it
import math
import random
import time

class Node:
    def __init__(self, state, parent=None, ):
        self.state = state
        self.parent = parent
        self.children = []
        self.value = 0
        self.visits = 0

    def add_child(self, child_state):
        child = Node(child_state, self)
        self.children.append(child)
   
   
def mcts_policy(time):
    def intermediate(position):
        move = helper(time, position)
        return move
    return intermediate
    

def helper(duration, position):
        
    root = Node(position)
    
    start_time = time.time()
    current_time = time.time()
    while (current_time - start_time) < duration:

        # returns the leaf node selected via UCB
        leaf = traverse(root)

        if leaf.state.is_terminal() is False:
            if leaf.visits > 0:
                leaf = expand(leaf)
            # run randomly to terminal states, updates visit and reward counters
        reward = simulate(leaf)
        # propagate changes up to root
        update(leaf, reward)
        current_time = time.time()
    return last_action(root)
    

                
# propagate reward from leaf node to root node
def update(leaf, reward):
    current = leaf
    # iterate until root; root node should be only node without a parent, 
    while current != None:
        current.visits += 1
        current.value += reward
        current = current.parent

# add nodes children to the tree
def expand(leaf):

    # this check should be redundant given when function is called
    if len(leaf.children) == 0:
        action_list = leaf.state.get_actions()
        for action in action_list:
            # successor function tells you the resulting position from an action at that position
            child = leaf.state.successor(action)
            leaf.add_child(child)

    # return arbitrary child
    arbitrary_child = random.choice(leaf.children)
    return arbitrary_child
         
# CHECKED
def traverse(root):
    # takes in root node, moves from root to leaf

    current = root

    # travels until you reach a leaf
    while len(current.children)!= 0:
        # picks the best action at each stage
        next_node = UCB(current)
        current = next_node 

    # node without children is a leaf node
    leaf = current

    return leaf


# simulates game from a leaf
#CHECKED
def simulate(leaf):
    current = leaf.state
    # random path to erminal state
    while current.is_terminal() is False:
        options = current.get_actions()
        next_action = random.choice(options)
        next_state = current.successor(next_action)
        current = next_state
    reward = current.payoff()
    return reward
    
def UCB(leaf):
    children = leaf.children
    best_move = None


    if leaf.state.actor() == 0:
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
    best_move = None


    if root.state.actor() == 0:
        max_score = float("-inf")
        # print([node.state for node in children])
        # print([node.value for node in children])
        # print([node.visits for node in children])
        
        for node in children:

            if node.value/node.visits > max_score:
                max_score = node.value/node.visits
                best_move = node
    else:
        min_score = float("inf")
        for node in children:
            if node.value/node.visits < min_score:
                min_score = node.value/node.visits
                best_move = node

    actions = root.state.get_actions()
    for action in actions:
        if root.state.successor(action) == best_move.state:
            return action
        
