import threading

import numpy as np
import gym
import pygame
import torch
from pyglet.window import key
import random

from stable_baselines3 import DQN, PPO, SAC


def play_audio():
    pygame.mixer.init()  # Initialize the mixer for audio
    pygame.mixer.music.load('car.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)  # Play the audio looped (-1 means infinite loop)


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
    car_labels = ["PPO_1M", "PPO_Discrete_2M", "DQN_1M"]
    # actions = np.zeros((NUM_CARS, 3))
    actions = [
        [0.0, 0.0, 0.0],
        0,
        0,
    ]

    continuous_actions = [True, False, False]

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    ppo_model_1m = PPO.load("PPO_RL_1M", device=device)
    dqn_model = DQN.load("DQN_RL_1M", device=device)
    ppo_discrete_model_1m = PPO.load("PPO_Discrete_RL_2M.zip", device=device)

    print("Model loaded")

    env = gym.make("MultiCarRacing-v0", num_agents=NUM_CARS, direction='CCW',
                   use_random_direction=True,
                   use_ego_color=True, continuous_actions=continuous_actions,
                   car_labels=car_labels)

    obs = env.reset()

    audio_thread_started = False
    audio_thread = threading.Thread(target=play_audio)
    audio_thread.daemon = True

    is_open = True
    stopped = False

    while is_open and not stopped:
        obs = env.reset()
        total_reward = np.zeros(NUM_CARS)
        steps = 0
        restart = False

        while True:
            actions[0] = model_policy(obs[0], ppo_model_1m)
            actions[1] = model_policy(obs[1], ppo_discrete_model_1m)
            actions[2] = model_policy(obs[2], dqn_model)

            obs, r, done, info = env.step(actions)
            total_reward += r

            # Start the audio thread only once during each game loop
            if not audio_thread_started:
                audio_thread.start()
                audio_thread_started = True  # Mark that the audio thread has been started

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
