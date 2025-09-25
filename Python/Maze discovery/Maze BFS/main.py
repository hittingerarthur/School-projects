import numpy as np
import matplotlib.pyplot as plt
import random
import time

from grid_map import GridMap
from robot import Robot
from robot_controller import RobotController

def create_rgb_image(fine_maze: np.ndarray, exploration: np.ndarray):
    """
    Builds an RGB image from the fine maze and exploration grid.
      - fine_maze: fine-resolution representation of the walls (obtained by repeating the coarse grid)
      - exploration: fine-resolution grid marked by the LIDAR scan.
    Colors:
      - Walls: black.
      - Unexplored free cells: white.
      - Explored cells: red for robot 1, green for robot 2, blue for robot 3.
    """
    size = fine_maze.shape[0]
    img = np.zeros((size, size, 3))
    white = [1, 1, 1]
    black = [0, 0, 0]
    robot_colors = {1: [1, 0, 0], 2: [0, 1, 0], 3: [0, 0, 1]}
    for i in range(size):
        for j in range(size):
            if fine_maze[i, j] == 1:
                img[i, j] = black
            else:
                if exploration[i, j] != 0:
                    img[i, j] = robot_colors.get(exploration[i, j], white)
                else:
                    img[i, j] = white
    return img

def calculate_exploration_stats(exploration, maze, resolution_factor):
    """Calculate exploration statistics for display."""
    coarse_rows, coarse_cols = exploration.shape[0] // resolution_factor, exploration.shape[1] // resolution_factor
    total_free_cells = np.sum(maze == 0)
    
    explored_by_robot = {}
    for robot_id in range(1, 4):
        robot_explored = np.zeros((coarse_rows, coarse_cols), dtype=bool)
        for r in range(coarse_rows):
            for c in range(coarse_cols):
                if np.any(exploration[r*resolution_factor:(r+1)*resolution_factor, 
                                     c*resolution_factor:(c+1)*resolution_factor] == robot_id):
                    robot_explored[r, c] = True
        
        explored_by_robot[robot_id] = np.sum(robot_explored & (maze == 0))
    
    # Calculate total explored cells
    total_explored = np.zeros((coarse_rows, coarse_cols), dtype=bool)
    for r in range(coarse_rows):
        for c in range(coarse_cols):
            if np.any(exploration[r*resolution_factor:(r+1)*resolution_factor, 
                                 c*resolution_factor:(c+1)*resolution_factor] != 0):
                total_explored[r, c] = True
    
    total_explored_cells = np.sum(total_explored & (maze == 0))
    
    # Calculate exploration percentage
    exploration_percentage = (total_explored_cells / total_free_cells) * 100 if total_free_cells > 0 else 100
    
    return {
        'total_explored': total_explored_cells,
        'total_free': total_free_cells,
        'percentage': exploration_percentage,
        'robot_stats': explored_by_robot
    }

def main():
    final_size = 40          # Coarse grid size (building plan)
    resolution_factor = 10   # Fine resolution factor (40x40 becomes 400x400)
    door_size = 5            # Larger door openings
    
    # Create the building plan (coarse grid) with the updated grid_map.
    grid_map = GridMap(size=final_size, min_room_size=5, max_depth=4, door_size=door_size, resolution_factor=resolution_factor)
    maze = grid_map.get_maze()                # Coarse maze (40x40)
    exploration = grid_map.get_exploration()    # Fine exploration grid (400x400)
    
    # Create a fine representation of the maze for display
    fine_maze = np.repeat(maze, resolution_factor, axis=0)
    fine_maze = np.repeat(fine_maze, resolution_factor, axis=1)
    
    # Select free positions from the coarse maze (cells where maze==0)
    free_positions = list(zip(*np.where(maze == 0)))
    if len(free_positions) < 3:
        print("Not enough free positions for robots!")
        return
        
    # Select positions that are far apart from each other
    robot_positions = []
    min_distance = (final_size // 3)  # Minimum distance between robots
    
    while len(robot_positions) < 3 and free_positions:
        # Pick a random position
        pos = random.choice(free_positions)
        free_positions.remove(pos)
        
        # Check if it's far enough from existing robots
        if all(abs(pos[0] - rpos[0]) + abs(pos[1] - rpos[1]) >= min_distance 
               for rpos in robot_positions):
            robot_positions.append(pos)
    
    # If we couldn't find well-separated positions, use random ones
    while len(robot_positions) < 3 and free_positions:
        robot_positions.append(free_positions.pop(random.randrange(len(free_positions))))
    
    robots = []
    # Create robots with their coarse positions and high-res scanning settings.
    for i, pos in enumerate(robot_positions, start=1):
        robots.append(Robot(robot_id=i, coarse_position=pos, lidar_radius=5.0, resolution_factor=resolution_factor))
    
    # Create the robot controller which plans moves toward frontiers.
    controller = RobotController(robots, maze, exploration, resolution_factor)
    
    # Initial LIDAR scan for each robot.
    for robot in robots:
        robot.scan(maze, exploration)
    
    # Track exploration progress
    start_time = time.time()
    exploration_history = []
    step_count = 0
    
    plt.ion()  # Turn on interactive mode for animation.
    fig = plt.figure(figsize=(12, 6))
    
    # Create two subplots - one for the maze and one for exploration stats
    ax1 = fig.add_subplot(121)  # Maze visualization
    ax2 = fig.add_subplot(122)  # Exploration progress chart
    
    try:
        while True:
            step_count += 1
            
            # Update robot positions using the controller
            controller.update()
            
            # After moving, each robot performs a LIDAR scan to update exploration
            for robot in robots:
                robot.scan(maze, exploration)
                robot.update_position_history()
            
            # Calculate exploration statistics
            stats = calculate_exploration_stats(exploration, maze, resolution_factor)
            exploration_history.append(stats['percentage'])
            
            # Create updated image from the fine maze and fine exploration grid
            img = create_rgb_image(fine_maze, exploration)
            
            # Update the maze visualization
            ax1.clear()
            ax1.imshow(img, origin='upper')
            ax1.set_title(f"Building Exploration ({stats['percentage']:.1f}% complete)")
            ax1.set_xticks([])
            ax1.set_yticks([])
            
            # Mark robot positions and their assigned frontiers
            for robot in robots:
                coarse_x, coarse_y = robot.coarse_position
                fine_x = coarse_x * resolution_factor + resolution_factor / 2.0
                fine_y = coarse_y * resolution_factor + resolution_factor / 2.0
                ax1.scatter(fine_y, fine_x, c='yellow', edgecolors='black', s=100, marker='o')
                ax1.text(fine_y, fine_x, str(robot.robot_id), color='black', ha='center', va='center', fontsize=12)
                
                # Draw a line to the robot's target cell if it exists
                if robot.robot_id in controller.target_cells and controller.target_cells[robot.robot_id]:
                    target = controller.target_cells[robot.robot_id]
                    target_x = target[0] * resolution_factor + resolution_factor / 2.0
                    target_y = target[1] * resolution_factor + resolution_factor / 2.0
                    ax1.plot([fine_y, target_y], [fine_x, target_x], 'y--', alpha=0.6)
            
            # Update the exploration progress chart
            ax2.clear()
            ax2.plot(exploration_history, 'b-')
            ax2.set_title(f"Exploration Progress (Step {step_count})")
            ax2.set_xlabel("Steps")
            ax2.set_ylabel("% Explored")
            ax2.set_ylim(0, 105)
            ax2.grid(True)
            
            # Add exploration stats
            elapsed_time = time.time() - start_time
            stats_text = (
                f"Time: {elapsed_time:.1f}s\n"
                f"Steps: {step_count}\n"
                f"Explored: {stats['total_explored']}/{stats['total_free']} cells\n"
                f"Robot 1: {stats['robot_stats'][1]} cells\n"
                f"Robot 2: {stats['robot_stats'][2]} cells\n"
                f"Robot 3: {stats['robot_stats'][3]} cells"
            )
            ax2.text(0.05, 0.6, stats_text, transform=ax2.transAxes)
            
            plt.tight_layout()
            plt.draw()
            plt.pause(0.1)
            
            # Break if exploration is essentially complete (>99%)
            if stats['percentage'] > 99.0:
                print(f"Exploration complete in {step_count} steps and {elapsed_time:.2f} seconds!")
                plt.savefig('final_exploration.png')  # Save the final state
                break
                
    except KeyboardInterrupt:
        print("Simulation interrupted by user.")
        print(f"Reached {stats['percentage']:.1f}% exploration in {step_count} steps and {elapsed_time:.2f} seconds.")

if __name__ == '__main__':
    main()