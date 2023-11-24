import random


class Maze:
    def __init__(self, width, height):
        self.start_node = None
        self.goal_node = None
        self.width = width
        self.height = height
        self.maze = [[0 for _ in range(width)] for _ in range(height)]

    def set_start_node(self, x, y):
        self.start_node = (x, y)

    def set_goal_node(self, x, y):
        self.goal_node = (x, y)

    def set_barrier_nodes(self, barrier_nodes):
        for node in barrier_nodes:
            x, y = node
            self.maze[y][x] = 1

    def print_maze(self):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == self.start_node:
                    print('S', end=' ')
                elif (x, y) == self.goal_node:
                    print('G', end=' ')
                elif self.maze[y][x] == 1:
                    print('B', end=' ')
                else:
                    print('0', end=' ')
            print()  # Move to the next line after each row
        print()


def setup_maze():
    maze = Maze(6, 6)
    barrier_coordinates = []
    # Randomly select a starting node
    start_node = random.randint(0, 11)
    start_node_x = start_node // 6
    start_node_y = start_node % 6
    maze.set_start_node(start_node_x, start_node_y)

    # Randomly select a goal node
    goal_node = random.randint(24, 35)
    goal_node_x = goal_node // 6
    goal_node_y = goal_node % 6
    maze.set_goal_node(goal_node_x, goal_node_y)

    # Randomly select four barrier nodes
    barrier_nodes = random.sample(list(set(range(36)) - {start_node, goal_node}), 4)
    for node in barrier_nodes:
        # Calculate the row index (y-coordinate) by performing integer division by 6
        barrier_node_x = node // 6
        # Calculate the column index (x-coordinate) by taking the remainder when dividing by 6
        barrier_node_y = node % 6
        # Create a tuple (x, y) and append it to the barrier_coordinates list
        barrier_coordinates.append((barrier_node_x, barrier_node_y))
    maze.set_barrier_nodes(barrier_coordinates)

    return maze


def dfs(maze):
    start_node = maze.start_node
    goal_node = maze.goal_node
    path = []
    visited_nodes = [start_node]
    visited = [start_node]
    time_taken = 1
    while len(visited) > 0:
        current_cell = visited.pop()
        path.append(current_cell)
        if current_cell == goal_node:
            break
        x, y = current_cell
        neighbor_cells = [
            (x - 1, y), (x + 1, y),
            (x, y - 1), (x, y + 1),
            # (x - 1, y - 1), (x - 1, y + 1),
            # (x + 1, y - 1), (x + 1, y + 1)
        ]
        # Process neighbors in increasing order
        neighbor_cells.sort()
        for neighbor_cell_x, neighbor_cell_y in neighbor_cells:
            neighbor_cell = (neighbor_cell_x, neighbor_cell_y)
            if (
                    0 <= neighbor_cell_x < maze.width
                    and 0 <= neighbor_cell_y < maze.height
                    and maze.maze[neighbor_cell_y][neighbor_cell_x] != 1
                    and neighbor_cell not in path
            ):
                visited.append(neighbor_cell)
                visited_nodes.append(neighbor_cell)
                time_taken += 1
            if neighbor_cell == goal_node:
                break
    return list(path), list(visited_nodes), time_taken


def heuristic_cost(maze):
    goal_node = maze.goal_node
    heuristic_values = [[0 for _ in range(maze.width)] for _ in range(maze.height)]
    for y in range(maze.height):
        for x in range(maze.width):
            x1, y1 = goal_node
            heuristic_value = abs(x - x1) + abs(y - y1)
            heuristic_values[y][x] = heuristic_value
    return heuristic_values


my_maze = setup_maze()
my_maze.print_maze()

path, visited_nodes, time = dfs(my_maze)


print("\nVisited Nodes:")
print(visited_nodes)
print("\nPath:")
print(path)
print("\nThe time taken to find the goal is " + str(time) + " minutes\n")

heuristic_costs = heuristic_cost(my_maze)
for row in heuristic_costs:
    print(row)
