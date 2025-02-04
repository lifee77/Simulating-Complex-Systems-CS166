import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import random

# Grid size and initial probability of panic
n = 100  # Grid size
p = 0.30  # Initial probability of panic

def initialize():
    """Initialize the grid with random values (0 = normal, 1 = panicky)."""
    global config, nextconfig
    config = np.zeros((n, n))
    for x in range(n):
        for y in range(n):
            config[x, y] = 1 if random.random() < p else 0
    nextconfig = np.zeros((n, n))

def update():
    """Update the grid based on the cellular automata rule."""
    global config, nextconfig
    for x in range(n):
        for y in range(n):
            count = sum([config[(x + dx) % n, (y + dy) % n] 
                         for dx in [-1, 0, 1] for dy in [-1, 0, 1]])
            nextconfig[x, y] = 1 if count >= 4 else 0
    config, nextconfig = nextconfig, config

def observe():
    """Update visualization at each iteration."""
    plt.cla()
    plt.imshow(config, vmin=0, vmax=1, cmap='binary')
    plt.title("Cellular Automata Simulation - Panic Spread")
    plt.pause(0.1)  # Adjust pause duration to control animation speed

# Run the simulation
initialize()
plt.figure(figsize=(6,6))

for _ in range(100):  # Simulate 100 steps
    update()
    observe()

plt.show()
