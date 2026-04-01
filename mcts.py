import random
import math
from game import TicTacToe

class Node:
    def __init__(self, game, parent=None):
        # The current game state at this node
        self.game = game
        # Parent node
        self.parent = parent
        # List of child nodes (possible future states)
        self.children = []
        # Number of times this node has been visited
        self.visits = 0
        # Total value (wins - losses accumulated)
        self.value = 0
        # Moves we have not explored yet from this state
        self.untried_moves = game.get_legal_moves()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c_param=1.4):
        """
        Select the best child using the UCB1 formula:
        value/visits + C * sqrt(log(parent_visits) / visits)
        """
        choices = []
        for child in self.children:
            ucb = (child.value / (child.visits + 1e-5)) + \
                  c_param * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-5))
            choices.append(ucb)
        return self.children[choices.index(max(choices))]

    def expand(self):
        """
        Take one untried move and create a new child node
        """
        move = self.untried_moves.pop()
        next_game = self.game.make_move(move)
        child = Node(next_game, self)
        self.children.append(child)
        return child

    def simulate(self):
        """
        Play a random game (rollout) from this position until terminal state
        """
        current_game = self.game

        while not current_game.is_terminal():
            # Pick a random legal move
            move = random.choice(current_game.get_legal_moves())
            current_game = current_game.make_move(move)
        
        # Return result of the game:
        # +1 (X wins), -1 (O wins), 0 (draw)
        return current_game.utility()

    def backpropagate(self, result):
        """
        Update this node and all ancestors with the simulation result
        """
        # Increase visit count
        self.visits += 1
        # Add result to total value
        self.value += result

        # Recursively update parent
        if self.parent:
            self.parent.backpropagate(result)


def mcts(root_game, iterations=10000):
    """
    Perform Monte Carlo Tree Search starting from root_game
    Returns the best next game state
    """
    root = Node(root_game)

    for _ in range(iterations):
        node = root

        # 1. Selection
        # Move down the tree using best_child until we reach a node
        # that is not fully expanded
        while node.is_fully_expanded() and node.children:
            node = node.best_child()

        # 2. Expansion
        # If the node is not terminal, expand it
        if not node.game.is_terminal():
            node = node.expand()

        # 3. Simulation
        result = node.simulate()

        # 4. Backpropagation
        node.backpropagate(result)

    # Pick best move (most visits)
    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.game
