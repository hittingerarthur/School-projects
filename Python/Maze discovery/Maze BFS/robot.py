import math
import random
import numpy as np

class Robot:
    def __init__(self, robot_id: int, coarse_position: tuple, lidar_radius: float = 4.0, resolution_factor: int = 10):
        """
        Parameters:
          - robot_id: Unique identifier for the robot.
          - coarse_position: The robot's position on the coarse grid (tuple of (row, col)).
          - lidar_radius: LIDAR range in coarse-units.
          - resolution_factor: Factor to convert coarse coordinates to the fine grid.
        """
        self.robot_id = robot_id
        self.coarse_position = coarse_position  # (row, col) on the coarse grid
        self.lidar_radius = lidar_radius
        self.resolution_factor = resolution_factor
        self.previous_positions = [coarse_position]  # Track recent positions to detect if robot is stuck
        self.scan_angles = list(range(0, 360, 5))  # Reduced number of angles for efficiency
        
    def scan(self, maze: np.ndarray, exploration: np.ndarray):
        """
        Performs a high-resolution LIDAR scan using the DDA algorithm on the fine exploration grid.
        Optimized to use fewer angles for faster processing.
        """
        r_factor = self.resolution_factor
        # Convert the coarse position to fine coordinates (center of the cell)
        coarse_x, coarse_y = self.coarse_position
        pos_x = coarse_x * r_factor + r_factor / 2.0
        pos_y = coarse_y * r_factor + r_factor / 2.0

        max_distance = self.lidar_radius * r_factor

        # Mark the starting cell in the fine exploration grid.
        start_cell_x = int(pos_x)
        start_cell_y = int(pos_y)
        
        # Mark the entire cell occupied by the robot
        cell_start_x = coarse_x * r_factor
        cell_start_y = coarse_y * r_factor
        
        for rx in range(cell_start_x, cell_start_x + r_factor):
            for ry in range(cell_start_y, cell_start_y + r_factor):
                if 0 <= rx < exploration.shape[0] and 0 <= ry < exploration.shape[1]:
                    exploration[rx, ry] = self.robot_id

        # Use pre-computed scan angles to improve performance
        for angle in self.scan_angles:
            rad = math.radians(angle)
            dx = math.cos(rad)
            dy = math.sin(rad)

            # Use optimized DDA algorithm for ray casting
            self._cast_ray(pos_x, pos_y, dx, dy, max_distance, maze, exploration, r_factor)
            
    def _cast_ray(self, pos_x, pos_y, dx, dy, max_distance, maze, exploration, r_factor):
        """Helper method to cast a single ray for the LIDAR scan."""
        current_x = pos_x
        current_y = pos_y
        cell_x = int(current_x)
        cell_y = int(current_y)

        tDeltaX = abs(1.0 / dx) if dx != 0 else float('inf')
        tDeltaY = abs(1.0 / dy) if dy != 0 else float('inf')

        if dx >= 0:
            stepX = 1
            next_boundary_x = cell_x + 1
            tMaxX = (next_boundary_x - current_x) / dx if dx != 0 else float('inf')
        else:
            stepX = -1
            next_boundary_x = cell_x
            tMaxX = (current_x - next_boundary_x) / abs(dx)

        if dy >= 0:
            stepY = 1
            next_boundary_y = cell_y + 1
            tMaxY = (next_boundary_y - current_y) / dy if dy != 0 else float('inf')
        else:
            stepY = -1
            next_boundary_y = cell_y
            tMaxY = (current_y - next_boundary_y) / abs(dy)

        distance = 0.0
        while distance < max_distance:
            if tMaxX < tMaxY:
                distance = tMaxX
                cell_x += stepX
                tMaxX += tDeltaX
            else:
                distance = tMaxY
                cell_y += stepY
                tMaxY += tDeltaY

            if distance > max_distance:
                break

            # Check bounds of the fine grid
            if cell_x < 0 or cell_x >= exploration.shape[0] or cell_y < 0 or cell_y >= exploration.shape[1]:
                break

            # Mark cell as explored by this robot
            if exploration[cell_x, cell_y] == 0:
                exploration[cell_x, cell_y] = self.robot_id

            # For collision detection, convert fine cell index to coarse index
            coarse_cell_x = cell_x // r_factor
            coarse_cell_y = cell_y // r_factor
            if coarse_cell_x < 0 or coarse_cell_x >= maze.shape[0] or coarse_cell_y < 0 or coarse_cell_y >= maze.shape[1]:
                break
                
            if maze[coarse_cell_x, coarse_cell_y] == 1:
                break
                
    def update_position_history(self):
        """Update the position history to detect if robot is stuck."""
        self.previous_positions.append(self.coarse_position)
        if len(self.previous_positions) > 10:  # Keep only last 10 positions
            self.previous_positions.pop(0)
            
    def is_stuck(self):
        """Check if the robot is stuck (oscillating between positions)."""
        if len(self.previous_positions) < 5:
            return False
            
        # If the robot has been in the same location multiple times
        position_counts = {}
        for pos in self.previous_positions[-5:]:  # Look at last 5 positions
            position_counts[pos] = position_counts.get(pos, 0) + 1
            
        return max(position_counts.values()) >= 3  # Robot is in same position 3+ times