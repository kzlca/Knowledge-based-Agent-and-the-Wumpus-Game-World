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


