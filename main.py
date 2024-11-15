import numpy as np
import gym
from pyglet.window import key
import random

from stable_baselines3 import DQN

gym.register(
    id='MultiCarRacing-v0',
    entry_point='merger:MultiCarRacing',
    max_episode_steps=1000,
    reward_threshold=900
)


def random_policy(observation):
    return np.array([random.uniform(-1, 1), random.uniform(0, 1), random.uniform(0, 1)])


def discrete_random_policy(observation):
    return random.randint(0, 4)


def model_policy(observation, model):
    obs = np.copy(observation)
    pred = model.predict(obs)

    if isinstance(pred[0], np.ndarray):  # continuous action
        return pred[0]  # Return the continuous action
    else:  # discrete action
        return pred[0]  # Return the discrete action (an integer)


if __name__ == "__main__":
    NUM_CARS = 2

    CAR_CONTROL_KEYS = [[key.LEFT, key.RIGHT, key.UP, key.DOWN]]

    # actions = np.zeros((NUM_CARS, 3))
    actions = [
        [0.0, 0.0, 0.0],
        0
    ]

    model = DQN.load("DQN_RL_100")

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
                   use_random_direction=True,
                   use_ego_color=True, continuous_actions=[True, False], car_labels=["Johnny", "DQN"])

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
            actions[1] = model_policy(obs[1], model)

            obs, r, done, info = env.step(actions)
            total_reward += r
            if steps % 200 == 0 or done:
                print("\nActions: " + str.join(" ", [f"Car {x}: " + str(actions[x]) for x in range(NUM_CARS)]))
                print(f"Step {steps} Total_reward " + str(total_reward))
                # import matplotlib.pyplot as plt
                # plt.imshow(s)
                # plt.savefig("test.jpeg")
            steps += 1
            is_open = env.render().all()
            if stopped or done or restart or is_open == False:
                break
    env.close()
