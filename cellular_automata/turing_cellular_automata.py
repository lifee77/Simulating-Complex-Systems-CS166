import numpy as np
import matplotlib.pyplot as plt

# Parameters
grid_size = 100  # Size of the 2D grid
timesteps = 100  # Number of simulation steps
Ra = 2  # Activation radius
Ri = 5  # Inhibition radius
wa = 1.0  # Strength of activation
wi = 0.5  # Strength of inhibition

# Initialize the grid randomly
grid = np.random.choice([0, 1], size=(grid_size, grid_size))

# Function to compute activation and inhibition influence
def compute_at(x, y, grid):
    active_neighbors = 0
    inhibitory_neighbors = 0
    
    for dx in range(-Ri, Ri + 1):
        for dy in range(-Ri, Ri + 1):
            if dx**2 + dy**2 <= Ri**2:  # Within inhibition radius
                if 0 <= x + dx < grid_size and 0 <= y + dy < grid_size:
                    inhibitory_neighbors += grid[x + dx, y + dy]
                    
            if dx**2 + dy**2 <= Ra**2:  # Within activation radius
                if 0 <= x + dx < grid_size and 0 <= y + dy < grid_size:
                    active_neighbors += grid[x + dx, y + dy]
    
    return wa * active_neighbors - wi * inhibitory_neighbors

# Simulation loop
for t in range(timesteps):
    new_grid = np.copy(grid)
    
    for x in range(grid_size):
        for y in range(grid_size):
            at_value = compute_at(x, y, grid)
            new_grid[x, y] = 1 if at_value > 0 else 0  # Update rule
    
    grid = new_grid
    
    # Visualization at specific timesteps
    if t % 20 == 0 or t == timesteps - 1:
        plt.imshow(grid, cmap='gray')
        plt.title(f"Timestep {t}")
        plt.show()
