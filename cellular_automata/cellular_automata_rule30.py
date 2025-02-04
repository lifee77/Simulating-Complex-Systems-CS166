import numpy as np
import matplotlib.pyplot as plt

def rule_30(initial_state, steps):
    """
    Simulates Rule 30 cellular automaton.
    
    Parameters:
        initial_state (list): Initial row of the automaton (e.g., [0, 0, 1, 0, 0]).
        steps (int): Number of steps to simulate.
        
    Returns:
        grid (numpy.ndarray): Grid of all states over time.
    """
    # Define the rule table as a dictionary
    rule = {
        (1, 1, 1): 0,
        (1, 1, 0): 0,
        (1, 0, 1): 0,
        (1, 0, 0): 1,
        (0, 1, 1): 1,
        (0, 1, 0): 1,
        (0, 0, 1): 1,
        (0, 0, 0): 0,
    }
    
    # Initialize the grid to store states
    width = len(initial_state)
    grid = np.zeros((steps, width), dtype=int)
    grid[0] = initial_state  # Set the initial state
    
    # Iterate over each time step
    for t in range(1, steps):
        for i in range(width):
            # Get the left, center, and right neighbors (wrap around using modulo)
            left = grid[t-1][(i-1) % width]
            center = grid[t-1][i]
            right = grid[t-1][(i+1) % width]
            
            # Determine the new state based on the rule
            grid[t][i] = rule[(left, center, right)]
    
    return grid

# Initial configuration (one cell in the middle is "1")
width = 51  # Total number of cells in the row
initial_state = [0] * (width // 2) + [1] + [0] * (width // 2)

# Simulate Rule 30
steps = 25  # Number of steps to visualize
grid = rule_30(initial_state, steps)

# Visualize the cellular automaton
plt.figure(figsize=(10, 10))
plt.imshow(grid, cmap="binary", interpolation="nearest")
plt.title("Rule 30 Cellular Automaton")
plt.xlabel("Cell")
plt.ylabel("Time Step")
plt.show()

def interpret_triangle(grid):
    """
    Analyzes and interprets the triangular pattern of Rule 30.

    Parameters:
        grid (numpy.ndarray): The grid representing the cellular automaton evolution.
    
    Prints:
        - The number of time steps.
        - Total number of active cells (1s) at each time step.
        - Symmetry analysis of the triangle edges.
    """
    steps, width = grid.shape
    
    print(f"Total Time Steps: {steps}")
    print(f"Width of the Grid: {width}")
    
    # Total active cells at each step
    print("\nActive Cells at Each Time Step:")
    for t, row in enumerate(grid):
        active_cells = np.sum(row)
        print(f"Step {t}: {active_cells} active cell(s)")
    
    # Analyze symmetry
    print("\nSymmetry Analysis:")
    left_edge = [row[0] for row in grid if np.sum(row) > 0]
    right_edge = [row[-1] for row in grid if np.sum(row) > 0]
    
    if left_edge == right_edge:
        print("The edges are symmetric.")
    else:
        print("The edges are asymmetric.")

    # Identify the chaotic center size
    chaotic_center_sizes = [np.max(np.nonzero(row)) - np.min(np.nonzero(row)) + 1 
                            for row in grid if np.sum(row) > 0]
    print("\nChaotic Center Sizes at Each Step:")
    for t, size in enumerate(chaotic_center_sizes):
        print(f"Step {t}: {size} cells wide")
    
# Call the interpret_triangle function
interpret_triangle(grid)
