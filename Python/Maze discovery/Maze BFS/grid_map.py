import numpy as np
import random

class GridMap:
    def __init__(self, size: int = 40, min_room_size: int = 5, max_depth: int = 4, door_size: int = 3, resolution_factor: int = 10):
        """
        Generates a building plan using BSP subdivision.
        
        Parameters:
          - size: The size of the coarse grid (including the outer wall).
          - min_room_size: The minimal size of a room required to allow further subdivision.
          - max_depth: Maximum recursion depth for subdivision.
          - door_size: The size (in cells) of the door openings between rooms.
          - resolution_factor: Factor to scale up the exploration grid. The fine exploration grid will be of size (size*resolution_factor) x (size*resolution_factor).
          
        In self.grid:
          1 represents a wall.
          0 represents free space.
        """
        self.size = size
        self.door_size = door_size
        self.resolution_factor = resolution_factor

        # Initialize the coarse grid with walls (1)
        self.grid = np.ones((size, size), dtype=int)
        # Subdivide the interior (from index 1 to size-2) to create rooms
        self.subdivide(
            x1=1, 
            y1=1, 
            x2=size - 2, 
            y2=size - 2, 
            depth=0, 
            min_room_size=min_room_size, 
            max_depth=max_depth
        )
        # Create the fine exploration grid (size*resolution_factor x size*resolution_factor)
        self.exploration = np.zeros((size * resolution_factor, size * resolution_factor), dtype=int)

    def subdivide(self, x1, y1, x2, y2, depth, min_room_size, max_depth):
        """
        Recursively subdivides the rectangular area defined by [x1, y1] to [x2, y2]
        to form rooms separated by walls with a door opening of specified size.
        """
        width = x2 - x1 + 1
        height = y2 - y1 + 1

        # Stop subdividing if maximum depth is reached or the area is too small to subdivide.
        if (depth >= max_depth 
            or width < 2 * min_room_size + 1
            or height < 2 * min_room_size + 1):
            # Empty the area to create a single room (0 = free space)
            for i in range(x1, x2 + 1):
                for j in range(y1, y2 + 1):
                    self.grid[i, j] = 0
            return

        # Choose whether to cut horizontally or vertically.
        if width > height:
            horizontal_cut = False
        elif height > width:
            horizontal_cut = True
        else:
            horizontal_cut = bool(random.getrandbits(1))

        if horizontal_cut:
            # Horizontal cut: choose a cut row ensuring room margins.
            cut = random.randint(y1 + min_room_size, y2 - min_room_size)
            for x in range(x1, x2 + 1):
                self.grid[x, cut] = 1
            # Create a door opening of size door_size in this horizontal wall.
            door_center = random.randint(x1, x2)
            door_half = self.door_size // 2
            door_start = max(x1, door_center - door_half)
            door_end = min(x2, door_start + self.door_size - 1)
            for x in range(door_start, door_end + 1):
                self.grid[x, cut] = 0

            # Subdivide the areas above and below the wall.
            self.subdivide(x1, y1, x2, cut - 1, depth + 1, min_room_size, max_depth)
            self.subdivide(x1, cut + 1, x2, y2, depth + 1, min_room_size, max_depth)
        else:
            # Vertical cut: choose a cut column ensuring room margins.
            cut = random.randint(x1 + min_room_size, x2 - min_room_size)
            for y in range(y1, y2 + 1):
                self.grid[cut, y] = 1
            # Create a door opening of size door_size in this vertical wall.
            door_center = random.randint(y1, y2)
            door_half = self.door_size // 2
            door_start = max(y1, door_center - door_half)
            door_end = min(y2, door_start + self.door_size - 1)
            for y in range(door_start, door_end + 1):
                self.grid[cut, y] = 0

            # Subdivide the areas to the left and right of the wall.
            self.subdivide(x1, y1, cut - 1, y2, depth + 1, min_room_size, max_depth)
            self.subdivide(cut + 1, y1, x2, y2, depth + 1, min_room_size, max_depth)

    def get_maze(self):
        return self.grid.copy()

    def get_exploration(self):
        return self.exploration.copy()
