import numpy as np
import gym
import torch
from pyglet.window import key
import random

from stable_baselines3 import DQN, PPO, SAC

try:
    gym.register(
        id='MultiCarRacing-v0',
        entry_point='merger:MultiCarRacing',
        max_episode_steps=1000,
        reward_threshold=900
    )
except:
    pass


def model_policy(observation, model):
    obs = np.copy(observation)
    pred = model.predict(obs, deterministic=True)
    return pred[0]


def bots_only():
    NUM_CARS = 3

    # actions = np.zeros((NUM_CARS, 3))
    actions = [
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        0,
    ]

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    dqn_model = DQN.load("DQN_RL_1M", device=device)
    ppo_model_1m = PPO.load("PPO_RL_1M", device=device)
    ppo_model_2m = PPO.load("PPO_RL_2M", device=device)

    print("Model loaded")

    env = gym.make("MultiCarRacing-v0", num_agents=NUM_CARS, direction='CCW',
                   use_random_direction=True,
                   use_ego_color=True, continuous_actions=[True, True, False],
                   car_labels=["PPO_1M", "PPO_2M", "DQN_1M"])

    obs = env.reset()

    is_open = True
    stopped = False
    while is_open and not stopped:
        obs = env.reset()
        total_reward = np.zeros(NUM_CARS)
        steps = 0
        restart = False
        while True:
            actions[0] = model_policy(obs[0], ppo_model_1m)
            actions[1] = model_policy(obs[1], ppo_model_2m)
            actions[2] = model_policy(obs[2], dqn_model)

            obs, r, done, info = env.step(actions)
            total_reward += r
            if steps % 200 == 0 or done:
                print("\nActions: " + str.join(" ", [f"Car {x}: " + str(actions[x]) for x in range(NUM_CARS)]))
                print(f"Step {steps} Total_reward " + str(total_reward))
            steps += 1
            is_open = env.render().all()
            if stopped or done or restart or is_open == False:
                break
    env.close()
