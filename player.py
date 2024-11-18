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


CAR_CONTROL_KEYS = [[key.LEFT, key.RIGHT, key.UP, key.DOWN]]


def player_vs_cars():
    NUM_CARS = 4
    car_labels = ["Player", "PPO_1M", "PPO_Discrete_2M", "DQN_1M"]

    # actions = np.zeros((NUM_CARS, 3))
    actions = [
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        0,
        0,
    ]

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    dqn_model = DQN.load("DQN_RL_1M", device=device)
    ppo_model_1m = PPO.load("PPO_RL_1M", device=device)
    ppo_discrete_model_2m = PPO.load("PPO_Discrete_RL_2M.zip", device=device)

    print("Model loaded")

    def key_press(k, mod):
        global restart, stopped, CAR_CONTROL_KEYS
        if k == 0xff1b: stopped = True
        if k == 0xff0d: restart = True
        if k == CAR_CONTROL_KEYS[0][0]: actions[0][0] = -1.0
        if k == CAR_CONTROL_KEYS[0][1]: actions[0][0] = +1.0
        if k == CAR_CONTROL_KEYS[0][2]: actions[0][1] = +1.0
        if k == CAR_CONTROL_KEYS[0][3]: actions[0][2] = +0.8

    def key_release(k, mod):
        global CAR_CONTROL_KEYS

        if k == CAR_CONTROL_KEYS[0][0] and actions[0][0] == -1.0: actions[0][0] = 0
        if k == CAR_CONTROL_KEYS[0][1] and actions[0][0] == +1.0: actions[0][0] = 0
        if k == CAR_CONTROL_KEYS[0][2]: actions[0][1] = 0
        if k == CAR_CONTROL_KEYS[0][3]: actions[0][2] = 0

    env = gym.make("MultiCarRacing-v0", num_agents=NUM_CARS, direction='CCW',
                   use_ego_color=True, continuous_actions=[True, True, False, False],
                   car_labels=car_labels)

    obs = env.reset()

    for viewer in env.viewer:
        viewer.window.on_key_press = key_press
        viewer.window.on_key_release = key_release

    is_open = True
    stopped = False
    while is_open and not stopped:
        obs = env.reset()
        total_reward = np.zeros(NUM_CARS)
        steps = 0
        restart = False
        while True:
            actions[1] = model_policy(obs[1], ppo_model_1m)
            actions[2] = model_policy(obs[2], ppo_discrete_model_2m)
            actions[3] = model_policy(obs[3], dqn_model)

            obs, r, done, info = env.step(actions)
            total_reward += r

            if steps % 200 == 0:
                print("\n\nStep " + str(steps))
                for i in range(NUM_CARS):
                    print(f"{car_labels[i]} action: {actions[i]}")

            if done:
                print("\n\nDone:")
                for i in range(NUM_CARS):
                    print(f"{car_labels[i]} reward: {total_reward[i]}")
                print(f"Step {steps} Total_reward " + str(total_reward))

                print("The winner by total reward is:", car_labels[np.argmax(total_reward)])
                stopped = True
                break

            steps += 1
            is_open = env.render().all()
            if stopped or done or restart or is_open == False:
                break
    env.close()
