This project creates a decision-making agent that uses the Monte_Carlo Tree Search Algorithm to play a wide variety of games. Included is an implementation of the games Kalah and Cribbage, as well as a Minimax agent for comparison. Below is an overview of the primary components:

Modules
  cribbage.py: Handles the logic specific to the game of Cribbage, including card handling and scoring.
  deck.py: Provides a generic deck of cards used by card games.
  game.py: Abstract base classes and utility functions for game management.
  kalah.py: Implements the Kalah game logic.
  mcts.py: A Monte Carlo Tree Search algorithm used for decision making in games.
  minimax.py: A Minimax algorithm with enhancements for evaluating game positions.
  peg_game.py, pegging.py: Manage the pegging phase in Cribbage.
  scoring.py: Functions to compute scores in different games based on current game states.
  test_mcts.py: Script for testing and comparing the performance of the MCTS algorithm against other strategies.

Setup
  To run the simulations or play the games, ensure you have Python 3.8 or higher installed. No external libraries are required for the base functionality.

Running the Tests
  Execute the following command to run tests on the MCTS implementations:
            python test_mcts.py
  You can adjust parameters such as the number of games, decision time per move, and which game to test through command line arguments.
