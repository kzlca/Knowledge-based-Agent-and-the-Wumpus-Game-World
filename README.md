# Wumpus World

Wumpus World is a classic artificial intelligence problem where an agent navigates through a grid-based environment, avoiding hazards like pits and a deadly Wumpus, to find the hidden gold. This implementation uses the Pygame library to create a visual representation of the Wumpus World environment and an intelligent agent that makes decisions based on sensory information.

## Features

- **Dynamic Environment:** The Wumpus World environment is dynamically generated with a random placement of the Wumpus, pits, and gold, providing a unique challenge in each playthrough.

- **Sensory Perception:** The agent can sense the presence of stench, breeze, and glitter in cells, allowing it to make informed decisions about its actions.

- **Intelligent Decision Making:** The agent uses a knowledge base to keep track of visited cells and sensory information, making strategic decisions to navigate the environment safely and achieve its goal.

- **Wumpus Elimination:** If the agent identifies the Wumpus, it strategically eliminates it, making the environment safer to explore.

## Getting Started

1. Install Pygame:
   ```bash
   pip install pygame
2. Run the Wumpus World simulation:
3. ```bash
   python WumpusGameWorld.py

<img src="https://github.com/kzlca/knowledge-based-agent-AI-for-Wumpus-game-world/blob/main/Drawing.sketchpad.png" width="50%" height="50%">

## Customization

The Wumpus World simulation offers flexibility in customizing the environment to suit your preferences. Here are the main parameters you can adjust:

- **Grid Size:** The size of the grid can be modified to create larger or smaller environments. The default grid size is 4x4. To change the grid size, modify the `GRID_SIZE` variable in the `wumpus_world.py` file.

    ```python
    GRID_SIZE = 4  # Change this value to your desired grid size (e.g., GRID_SIZE = 6)
    ```

- **Cell Size:** The size of each cell in the grid determines the visual representation of the environment. Adjust the `CELL_SIZE` variable in the `wumpus_world.py` file to change the cell size. Larger cell sizes may require adjustments to the overall screen size.

    ```python
    CELL_SIZE = 100  # Change this value to your desired cell size (e.g., CELL_SIZE = 80)
    ```

Feel free to experiment with different grid sizes and cell sizes to tailor the Wumpus World simulation to your preferences.

