import numpy as np
from collections import deque
import random

def get_coarse_explored(exploration, resolution_factor):
    """Returns a coarse grid indicating explored cells."""
    coarse_rows, coarse_cols = exploration.shape[0] // resolution_factor, exploration.shape[1] // resolution_factor
    coarse_explored = np.zeros((coarse_rows, coarse_cols), dtype=bool)
    for r in range(coarse_rows):
        for c in range(coarse_cols):
            if np.any(exploration[r*resolution_factor:(r+1)*resolution_factor, c*resolution_factor:(c+1)*resolution_factor] != 0):
                coarse_explored[r, c] = True
    return coarse_explored

def get_frontier_cells(maze, coarse_explored):
    """Returns the list of frontier cells (unexplored cells adjacent to explored cells)."""
    frontier_cells = []
    rows, cols = coarse_explored.shape
    for r in range(rows):
        for c in range(cols):
            # If cell is unexplored and not a wall
            if not coarse_explored[r, c] and not maze[r, c]:
                # Check if it's adjacent to any explored cell
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and coarse_explored[nr, nc] and not maze[nr, nc]:
                        frontier_cells.append((r, c))
                        break
    return frontier_cells

def get_regions(frontier_cells, num_regions=10): # 3 
    """Group frontier cells into regions for more efficient multi-robot exploration."""
    if not frontier_cells:
        return []
    
    if len(frontier_cells) <= num_regions:
        return [[cell] for cell in frontier_cells]
        
    # Use K-means clustering to group frontier cells
    regions = [[] for _ in range(num_regions)]
    # Start with random cells as centroids
    centroids = random.sample(frontier_cells, num_regions)
    
    for _ in range(15):  # 5 iterations of k-means
        # Clear regions
        for region in regions:
            region.clear()
            
        # Assign cells to nearest centroid
        for cell in frontier_cells:
            distances = [np.sqrt((cell[0] - c[0])**2 + (cell[1] - c[1])**2) for c in centroids]
            nearest_region = np.argmin(distances)
            regions[nearest_region].append(cell)
            
        # Update centroids
        for i, region in enumerate(regions):
            if region:
                centroids[i] = (sum(r[0] for r in region) // len(region), 
                                sum(r[1] for r in region) // len(region))
    
    # Handle empty regions
    for i, region in enumerate(regions):
        if not region and frontier_cells:
            regions[i] = [frontier_cells.pop()]
            
    return regions

def bfs_path(maze, start, goal):
    """Returns the shortest path from start to goal using BFS."""
    if start == goal:
        return [start]
        
    queue = deque([[start]])
    visited = set()
    visited.add(start)
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == goal:
            return path
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and not maze[nx, ny] and (nx, ny) not in visited:
                queue.append(path + [(nx, ny)])
                visited.add((nx, ny))
    return None

def calculate_path_cost(path, robot_positions, safety_distance=2):
    """Calculate path cost considering other robots' positions."""
    if not path:
        return float('inf')
        
    cost = len(path)
    
    # Add cost for paths that come close to other robots
    for point in path:
        for robot_pos in robot_positions:
            distance = abs(point[0] - robot_pos[0]) + abs(point[1] - robot_pos[1])  # Manhattan distance
            if distance < safety_distance:
                cost += (safety_distance - distance) * 2  # Higher cost for points close to other robots
                
    return cost

class RobotController:
    def __init__(self, robots, maze, exploration, resolution_factor):
        """
        Parameters:
          - robots: List of Robot instances.
          - maze: The coarse grid (building plan) for collision detection.
          - exploration: The fine-resolution exploration grid.
          - resolution_factor: Factor to convert coarse coordinates to the fine grid.
        """
        self.robots = robots
        self.maze = maze
        self.exploration = exploration
        self.resolution_factor = resolution_factor
        self.assigned_regions = {}  # Maps robot ID to its assigned region
        self.target_cells = {}      # Maps robot ID to its target cell
        self.move_cooldown = {robot.robot_id: 0 for robot in robots}  # Cooldown timer for robots stuck in place
        self.explored_percentage = 0  # Track exploration progress

    def update(self):
        coarse_explored = get_coarse_explored(self.exploration, self.resolution_factor)
        
        # Calculate exploration percentage
        total_cells = np.sum(self.maze == 0)
        explored_cells = np.sum(coarse_explored & (self.maze == 0))
        self.explored_percentage = (explored_cells / total_cells) * 100 if total_cells > 0 else 100
        
        if self.explored_percentage >= 99:
            print(f"Map fully explored! ({self.explored_percentage:.1f}%)")
            return
            
        # Get frontier cells and divide into regions
        frontier_cells = get_frontier_cells(self.maze, coarse_explored)
        if not frontier_cells:
            print("No more frontier cells!")
            return
            
        # Divide frontiers into regions - one region per robot
        regions = get_regions(frontier_cells, len(self.robots))
        
        # Get current positions of all robots
        robot_positions = [robot.coarse_position for robot in self.robots]
        
        # Process each robot's movement
        proposed_moves = {}
        for robot in self.robots:
            # Check if the robot is stuck (no movement in multiple turns)
            if self.move_cooldown[robot.robot_id] > 0:
                self.move_cooldown[robot.robot_id] -= 1
                
            # Assign or update region for the robot
            if robot.robot_id not in self.assigned_regions or not self.assigned_regions[robot.robot_id]:
                # Find closest region
                min_dist = float('inf')
                closest_region = None
                
                for region in regions:
                    if not region:
                        continue
                    
                    # Calculate average distance to region
                    avg_dist = sum(abs(robot.coarse_position[0] - cell[0]) + 
                                  abs(robot.coarse_position[1] - cell[1]) 
                                  for cell in region) / len(region)
                    
                    # Check if this region is already assigned to another robot
                    region_assigned = False
                    for r_id, assigned_region in self.assigned_regions.items():
                        if r_id != robot.robot_id and assigned_region and set(assigned_region) == set(region):
                            region_assigned = True
                            break
                    
                    if not region_assigned and avg_dist < min_dist:
                        min_dist = avg_dist
                        closest_region = region
                
                if closest_region:
                    self.assigned_regions[robot.robot_id] = closest_region
                    regions.remove(closest_region)  # Remove assigned region
                else:
                    # If no suitable region, try to find any frontier cell
                    if frontier_cells:
                        self.assigned_regions[robot.robot_id] = [random.choice(frontier_cells)]
            
            # Find best target cell in robot's region
            current_region = self.assigned_regions.get(robot.robot_id, [])
            start = robot.coarse_position
            
            best_target = None
            best_path = None
            best_cost = float('inf')
            
            for target in current_region:
                path = bfs_path(self.maze, start, target)
                if path:
                    # Calculate path cost considering other robots
                    other_positions = [pos for i, pos in enumerate(robot_positions) if i != robot.robot_id - 1]
                    cost = calculate_path_cost(path, other_positions)
                    
                    if cost < best_cost:
                        best_cost = cost
                        best_path = path
                        best_target = target
            
            # If no valid path found in current region, try to find any accessible frontier cell
            if not best_path and frontier_cells:
                # Sort frontier cells by distance to the robot
                frontier_cells.sort(key=lambda cell: abs(cell[0] - start[0]) + abs(cell[1] - start[1]))
                
                for target in frontier_cells[:2]:  # Try the 10 closest cells
                    path = bfs_path(self.maze, start, target)
                    if path:
                        best_path = path
                        best_target = target
                        self.assigned_regions[robot.robot_id] = [target]
                        break
            
            # If we found a path, propose the next step
            if best_path and len(best_path) > 1:
                proposed_moves[robot] = best_path[1]
                self.target_cells[robot.robot_id] = best_target
            else:
                # Robot can't move, reset its assigned region after some time
                if self.move_cooldown[robot.robot_id] <= 0:
                    self.move_cooldown[robot.robot_id] = 1  # Wait 5 turns before trying a new region
                    if robot.robot_id in self.assigned_regions:
                        del self.assigned_regions[robot.robot_id]
                proposed_moves[robot] = start  # Stay in place
        
        # Resolve conflicts
        move_counts = {}
        for move in proposed_moves.values():
            move_counts[move] = move_counts.get(move, 0) + 1
            
        # Execute moves with no conflicts
        for robot, move in proposed_moves.items():
            if move_counts[move] == 1 and not any(other.coarse_position == move for other in self.robots if other != robot):
                robot.coarse_position = move
                # If robot reached its target, clear the assigned region
                if self.target_cells.get(robot.robot_id) == move:
                    if robot.robot_id in self.assigned_regions:
                        del self.assigned_regions[robot.robot_id]

