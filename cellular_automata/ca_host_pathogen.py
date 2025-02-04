import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Grid parameters
grid_size = 50
timesteps = 100

# Probabilities
p_infection = 0.3  # Probability of infection spreading
p_recovery = 0.1   # Probability of an infected host recovering
p_death = 0.05     # Probability of an infected host dying
p_reproduction = 0.1  # Probability of a healthy host reproducing in empty space

# States
HEALTHY = 1
INFECTED = 2
EMPTY = 0

# Initialize grid with random distribution of healthy and infected hosts
grid = np.random.choice([HEALTHY, INFECTED, EMPTY], size=(grid_size, grid_size), p=[0.7, 0.2, 0.1])

# Store population data
healthy_counts = []
infected_counts = []

# Neighborhood infection function
def count_neighbors(x, y, state):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx != 0 or dy != 0) and (0 <= x + dx < grid_size) and (0 <= y + dy < grid_size):
                if grid[x + dx, y + dy] == state:
                    count += 1
    return count

# Simulation loop
for t in range(timesteps):
    new_grid = np.copy(grid)
    
    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x, y] == HEALTHY:
                infected_neighbors = count_neighbors(x, y, INFECTED)
                if np.random.rand() < p_infection * infected_neighbors:  # Infection chance increases with infected neighbors
                    new_grid[x, y] = INFECTED

            elif grid[x, y] == INFECTED:
                if np.random.rand() < p_recovery:  # Recovery
                    new_grid[x, y] = HEALTHY
                elif np.random.rand() < p_death:  # Death
                    new_grid[x, y] = EMPTY

            elif grid[x, y] == EMPTY:
                healthy_neighbors = count_neighbors(x, y, HEALTHY)
                if np.random.rand() < p_reproduction * healthy_neighbors:  # Reproduction based on neighboring hosts
                    new_grid[x, y] = HEALTHY
    
    grid = new_grid
    
    # Collect population data
    healthy_counts.append(np.sum(grid == HEALTHY))
    infected_counts.append(np.sum(grid == INFECTED))

    # Visualization at specific timesteps
    if t % 20 == 0 or t == timesteps - 1:
        plt.figure(figsize=(6,6))
        sns.heatmap(grid, cmap="coolwarm", cbar=False, xticklabels=False, yticklabels=False)
        plt.title(f"Host-Pathogen System at Timestep {t}")
        plt.show()

# Plot population changes over time
plt.figure(figsize=(8, 4))
plt.plot(healthy_counts, label="Healthy Hosts", color="blue")
plt.plot(infected_counts, label="Infected Hosts", color="red")
plt.xlabel("Time")
plt.ylabel("Population")
plt.title("Host & Pathogen Populations Over Time")
plt.legend()
plt.show()
