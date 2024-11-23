# RL Car Racing

<img src="visuals/gameplay.gif" alt="Gameplay Demo" style="width:100%; max-width:800px; display:block; margin:auto;">

RL Car Racing is a Python-based simulation game that combines reinforcement learning (RL) models with interactive
gameplay. Players can compete against RL-driven cars or watch RL models race against each other.

## Features

- **Player vs RL Models:** Race against pre-trained reinforcement learning models such as PPO and DQN.
- **RL Models Only Mode:** Simulate races where RL agents compete using advanced algorithms.
- **Custom Racing Environment:** Utilizes a modified version of OpenAI's `gym` for multi-car racing.
- **Dynamic Track Generation:** Randomized tracks for unique challenges in each race.
- **Customizable Cars:** Individual settings for cars and models.

## Requirements

- Python 3.7
- Dependencies listed in `requirements.txt`:
    - `gym`
    - `pygame`
    - `torch`
    - `stable-baselines3`
    - Other dependencies for running RL and game mechanics

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/JohnnyKoshev/rl-carracing.git
   cd rl-carracing
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add the required RL model files and assets (e.g., `PPO_RL_1M`, `DQN_RL_1M`, `menu.png`, `music.mp3`) to the project
   directory.

## Usage

1. Start the game:
   ```bash
   python main.py
   ```

2. Choose a game mode:
    - **Player vs RL Models**: Control a car using your keyboard and race against RL models.
    - **RL Models Only**: Watch RL models compete with each other.

## Project Structure

- `main.py`: Entry point, includes menu navigation and game initialization.
- `player.py`: Implements the "Player vs RL Models" mode.
- `bots.py`: Implements the "RL Models Only" mode.
- `merger.py`: Contains the `MultiCarRacing` environment logic.
- `ppo_discrete.ipynb`, `ppo.ipynb`, `dqn.ipynb`: Notebooks for training RL models.

#### Feel free to train your own RL models using the provided notebooks and add them to the game!

## Authors

- Komiljon Yuldashev
- Abdulaziz Zakirov

---

Enjoy the race!
