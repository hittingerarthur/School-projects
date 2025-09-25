import heapq
import math

class Problem:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state  
        self.goal_state = goal_state        
        self.operators = ['up', 'down', 'left', 'right']

    def goal_test(self, state):
        return state == self.goal_state

    def find_blank(self, state):
        """Finds the position of the blank tile (0) in the state."""
        for i, row in enumerate(state):
            for j, tile in enumerate(row):
                if tile == 0:
                    return i, j
        return None

    def get_neighbors(self, node):
        """Generates all possible neighbor nodes by moving the blank tile."""
        neighbors = []
        x, y = self.find_blank(node.state)
        moves = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        for move in self.operators:
            dx, dy = moves[move]
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(node.state) and 0 <= new_y < len(node.state[0]):
                # new state by swapping blank tile with adjacent tile
                new_state = [list(row) for row in node.state]
                new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
                new_state = tuple(tuple(row) for row in new_state)
                neighbor_node = PuzzleNode(
                    state=new_state,
                    parent=node,
                    g=node.g + 1
                )
                neighbors.append(neighbor_node)
        return neighbors

class PuzzleNode:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state  
        self.parent = parent
        self.g = g          # cost so far
        self.h = h          # heuristic value
        self.f = self.g + self.h  # total cost

    def __lt__(self, other):
        """Comparison method for priority queue ordering based on f(n)."""
        return self.f < other.f

def misplaced_tile_heuristic(state, goal):
    """Heuristic function that counts the number of misplaced tiles."""
    h = 0
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                h += 1
    return h

def euclidean_distance_heuristic(state, goal):
    """Heuristic function that calculates the sum of Euclidean distances of tiles from their goal positions."""
    h = 0
    goal_positions = {}
    for i in range(len(goal)):
        for j in range(len(goal[0])):
            tile = goal[i][j]
            goal_positions[tile] = (i, j)
    for i in range(len(state)):
        for j in range(len(state[0])):
            tile = state[i][j]
            if tile != 0:
                goal_i, goal_j = goal_positions[tile]
                h += math.sqrt((i - goal_i) ** 2 + (j - goal_j) ** 2)
    return h

def A_Star_Search(problem, heuristic):
    """A* search algorithm implementation."""
    start_node = PuzzleNode(
        state=problem.initial_state,
        parent=None,
        g=0,
        h=heuristic(problem.initial_state, problem.goal_state)
    )
    start_node.f = start_node.g + start_node.h

    frontier = []
    heapq.heappush(frontier, start_node)
    explored = set()
    nodes_expanded = 0
    max_frontier_size = 1

    print("Expanding state")
    for row in start_node.state:
        print(' '.join('b' if tile == 0 else str(tile) for tile in row))
    print()

    while frontier:
        current_node = heapq.heappop(frontier)
        nodes_expanded += 1

        print(f"The best state to expand with g(n) = {current_node.g} and h(n) = {int(current_node.h)} is...")
        for row in current_node.state:
            print(' '.join('b' if tile == 0 else str(tile) for tile in row))
        print("Expanding this node...\n")

        if problem.goal_test(current_node.state):
            print("Goooooooal ! ! ! ")
            print(f"To solve this problem the search algorithm expanded a total of {nodes_expanded} nodes.")
            print(f"The maximum number of nodes in the queue at any one time: {max_frontier_size}.")
            print(f"The depth of the goal node was {current_node.g}.")
            return {
                'path': reconstruct_path(current_node),
                'nodes_expanded': nodes_expanded,
                'max_frontier_size': max_frontier_size,
                'depth': current_node.g
            }

        explored.add(current_node.state)
        neighbors = problem.get_neighbors(current_node)
        for neighbor in neighbors:
            if neighbor.state not in explored and neighbor not in frontier:
                neighbor.h = heuristic(neighbor.state, problem.goal_state)
                neighbor.f = neighbor.g + neighbor.h
                heapq.heappush(frontier, neighbor)
                if len(frontier) > max_frontier_size:
                    max_frontier_size = len(frontier)
    print("No solution found.")
    return None  # no solution found

def reconstruct_path(goal_node):
    """Reconstructs the path from the initial state to the goal state."""
    path = []
    current = goal_node
    while current:
        path.append(current.state)
        current = current.parent
    path.reverse()
    return path

def main():
    print("Welcome to hples00 & ahitt003 8 puzzle solver.")
    choice = input('Type "1" to use a default puzzle, or "2" to enter your own puzzle.\n')
    if choice == '1':
        initial_state = (
            (1, 2, 3),
            (4, 8, 0),
            (7, 6, 5)
        )
    elif choice == '2':
        print("Enter your puzzle, use a zero to represent the blank")
        initial_state = []
        for i in range(3):
            row_input = input(f"Enter the {['first', 'second', 'third'][i]} row, use space or tabs between numbers\n")
            row = [int(num) for num in row_input.strip().split()]
            if len(row) != 3:
                print("Invalid row length. Please enter exactly 3 numbers.")
                return
            initial_state.append(tuple(row))
        initial_state = tuple(initial_state)
    else:
        print("Invalid choice!")
        return

    print("Enter your choice of algorithm")
    print("1. Uniform Cost Search")
    print("2. A* with the Misplaced Tile heuristic.")
    print("3. A* with the Euclidean distance heuristic.")
    algo_choice = input()

    if algo_choice == '1':
        heuristic = lambda s, g: 0  # uniform cost search heuristic is zero
    elif algo_choice == '2':
        heuristic = misplaced_tile_heuristic
    elif algo_choice == '3':
        heuristic = euclidean_distance_heuristic
    else:
        print("Invalid algorithm choice!")
        return

    goal_state = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0)
    )

    problem = Problem(initial_state, goal_state)

    result = A_Star_Search(problem, heuristic)

    if result:
        #  results are already printed inside the A_Star_Search function
        pass
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
