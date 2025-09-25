import math
import heapq

class Problem:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state  
        self.operators = ['up', 'down', 'left', 'right']

    def goal_test(self, state):
        return state == self.goal_state

    def find_blank(self, state):
        for i, row in enumerate(state):
            for j, tile in enumerate(row):
                if tile == 0:
                    return i, j
        return None
    
    def get_neighbors(self, node):
        """get neighbor nodes by moving the blank tile"""
        neighbors = []
        x, y = self.find_blank(node.state)
        moves = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        for move in self.operators:
            change_x, change_y = moves[move]
            new_x, new_y = x + change_x, y + change_y
            if 0 <= new_x < len(node.state) and 0 <= new_y < len(node.state[0]):
                # swap the tiles
                new_state = []
                for row in node.state:
                    new_state.append(list(row)) 

                new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
                for i in range(len(new_state)):
                    new_state[i] = tuple(new_state[i])
                new_state = tuple(new_state)
                
                neighbor = PuzzleNode(state=new_state, parent=node, g=node.g + 1)
                neighbors.append(neighbor)
        return neighbors

def reconstruct_path(goal_node):
    """make the path from the initial state to the goal state"""
    path = []
    current = goal_node
    while current:
        path.append(current.state)
        current = current.parent
    path.reverse()
    return path

class PuzzleNode:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g          # cost so far
        self.h = h          # heuristic value
        self.f = self.g + self.h  # total cost

    def __lt__(self, other):
        return self.f < other.f


def misplaced_tile_heuristic(state, goal):
    """counts number of misplaced tiles"""
    h = 0
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                h += 1
    return h

def euclidean_distance_heuristic(state, goal):
    """calculates the sum of euclidean distances of tiles from vs their goal positions"""
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

def uniform_cost_heuristic(state, goal):
    return 0

def A_Star_Search(problem, heuristic):
    """A* search algo"""
    start_node = PuzzleNode(
        state=problem.initial_state,
        parent=None,
        g=0,
        h=heuristic(problem.initial_state, problem.goal_state)
    )
    start_node.f = start_node.g + start_node.h

    exploration_queue = []
    heapq.heappush(exploration_queue, start_node)
    explored_states = set()

    nodes_expanded = 0
    max_queue_size = 1

    while exploration_queue:
        current_node = heapq.heappop(exploration_queue)
        nodes_expanded += 1
        # if reach goal state, return path
        if problem.goal_test(current_node.state) == True:
            return reconstruct_path(current_node), nodes_expanded, max_queue_size
        
        
        explored_states.add(current_node.state)
        neighbors = problem.get_neighbors(current_node)

        for neighbor in neighbors:
            neighbor_state = neighbor.state
            if neighbor_state not in explored_states:
                neighbor.h = heuristic(neighbor.state, problem.goal_state)
                neighbor.f = neighbor.g + neighbor.h
                heapq.heappush(exploration_queue, neighbor)
                if len(exploration_queue) > max_queue_size:
                    max_queue_size = len(exploration_queue)
    return None, nodes_expanded, max_queue_size  # no solution found



# if __name__ == "__main__":

#     initial_state = (
#         (1, 2, 3),
#         (4, 0, 6),
#         (7, 5, 8)
#     )
#     goal_state = (
#         (1, 2, 3),
#         (4, 5, 6),
#         (7, 8, 0)
#     )

#     problem = Problem(initial_state, goal_state)
#     solution_path = A_Star_Search(problem, misplaced_tile_heuristic)

#     if solution_path:
#         print(f"got a solution in {len(solution_path)-1} moves!!")
#         for state in solution_path:
#             for row in state:
#                 print(row)
#             print()
#     else:
#         print("No solutions was found")

def main():

    print("Welcome to hples00 & ahitt003 8-puzzle solver.")

    choice = input('Type 1 to use default puzzle, Type 2 to enter custom puzzle.\n')
    
    if choice == '1':
        initial_state = (
            (1, 2, 3),
            (4, 8, 0),
            (7, 6, 5)
        )
    elif choice == '2':
        print("Enter puzzle, remember to use 0 to represent the blank space.")

        initial_state = []
        for i in range(3):
            row_input = input(f"Enter the {['first', 'second', 'third'][i]} row, with spaces between numbers:\n")
            row = []
            for num in row_input.strip().split():
                row.append(int(num))

            if len(row) != 3:
                print("That row length doesnt work. Enter exactly 3 numbers in a row with spaces.")
                return
            initial_state.append(tuple(row))
        initial_state = tuple(initial_state)
    else:
        print("choice not valid!")
        return

    print("Select search algorithm:")
    print("1. Uniform Cost Search")
    print("2. A* with the Misplaced Tile heuristic")
    print("3. A* with the Euclidean Distance heuristic")
    algo_choice = input()

    if algo_choice not in ['1', '2', '3']:
        print("Invalid algorithm choice!")
        return
    elif algo_choice == '1':
        heuristic = uniform_cost_heuristic
    elif algo_choice == '2':
        heuristic = misplaced_tile_heuristic
    elif algo_choice == '3':
        heuristic = euclidean_distance_heuristic

    goal_state = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0)
    )

    problem = Problem(initial_state, goal_state)

    result, nodes_expanded, max_queue_size = A_Star_Search(problem, heuristic)

    if result:
        print(f"found a solution in {len(result) - 1} moves:")
        print(f"number of nodes expanded: {nodes_expanded}")
        print(f"max queue size: {max_queue_size}")
        for state in result:
            for row in state:
                print(row)
            print()
    else:
        print("No solution was found.")
        print(f"number of nodes expanded: {nodes_expanded}")
        print(f"max queue size: {max_queue_size}")

if __name__ == "__main__":
    main()

