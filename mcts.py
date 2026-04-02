import math
import random


class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        # Current game state
        self.state = state

        # Parent node
        self.parent = parent

        # Move that led to this state
        self.move = move

        # Children nodes
        self.children = []

        # MCTS statistics
        self.wins = 0
        self.visits = 0

        # Moves not yet explored
        self.untried_moves = state.get_legal_moves()

    def is_fully_expanded(self):
        # True if all moves have been tried
        return len(self.untried_moves) == 0

    def best_child(self, c=1.41):
        """
        Select child using UCB1 formula:
        UCB1 = (wins / visits) + C * sqrt(ln(parent_visits) / visits)
        """
        best_score = -float('inf')
        best_node = None

        for child in self.children:
            if child.visits == 0:
                return child  # explore unvisited nodes immediately

            exploitation = child.wins / child.visits
            exploration = c * math.sqrt(
                math.log(self.visits + 1) / child.visits   # +1 FIX
            )

            score = exploitation + exploration

            if score > best_score:
                best_score = score
                best_node = child

        return best_node

    def best_move(self):
        """
        Return move with highest visit count
        (NOT highest win rate, per assignment)
        """
        return max(self.children, key=lambda c: c.visits).move


# 1. SELECTION
def select(node):
    """
    Traverse the tree using UCB1 until:
    - node is not fully expanded OR
    - node is terminal
    """
    while not node.state.is_terminal():
        if not node.is_fully_expanded():
            return node
        if not node.children:
            return node
        node = node.best_child()
    return node


# 2. EXPANSION
def expand(node):
    """
    Expand one untried move
    """
    move = node.untried_moves.pop()
    next_state = node.state.make_move(move)

    child = MCTSNode(next_state, parent=node, move=move)
    node.children.append(child)

    return child


# 3. SIMULATION
def simulate(state):
    """
    Play random moves until game ends
    """
    current_state = state

    while not current_state.is_terminal():
        move = random.choice(current_state.get_legal_moves())
        current_state = current_state.make_move(move)

    return current_state.utility()


# 4. BACKPROPAGATION
def backpropagate(node, result):
    """
    Update nodes from leaf to root
    Only count win if favorable for player who made the move
    """
    while node is not None:
        node.visits += 1

        # If the player who JUST moved at this node won
        if node.state.current_player == -result:
            node.wins += 1

        node = node.parent


# MAIN MCTS LOOP
def mcts(state, iterations=10000):
    root = MCTSNode(state)

    for _ in range(iterations):

        # 1. Selection
        leaf = select(root)

        # 2. Expansion
        if not leaf.state.is_terminal():
            leaf = expand(leaf)

        # 3. Simulation
        result = simulate(leaf.state)

        # 4. Backpropagation
        backpropagate(leaf, result)

    # Return best move (NOT state)
    if not root.children:
        return random.choice(state.get_legal_moves())
    return root.best_move()
