QFL: an NFL Game Strategy Simulator

This project implements Q-learning to provide the optimal strategies for a given NFL game. It includes code for a simplified NFL game environment as well as code for defining strategies, running simulations, and testing the effectiveness of learned policies.

Overview of Modules
  nfl_strategy.py: Defines the NFL strategy game model, including the initialization of game states and the computation of outcomes based on various plays.
  qfl.py: Implements a Q-learning algorithm to learn optimal strategies within the NFL game context.
  test_qfl.py: A script for testing the Q-learning implementation using predefined game scenarios.

Usage
  To simulate game strategies run the following code in your terminal:
      python test_qfl.py [model-number] [learning-time] [num-games]
    
  model-number: Select the model configuration for the simulation.
  learning-time: Set the maximum time allowed for the Q-learning algorithm.
  num-games: Define the number of games to simulate to test the learned strategy.

Setup
  Ensure Python 3.x is installed. This project uses standard Python libraries, so no additional installation is required.
