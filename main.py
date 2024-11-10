import numpy as np
import gym
import gym_multi_car_racing
from pyglet.window import key
import random


def random_policy(observation):
    # action[0] is steering: range [-1, 1]
    # action[1] is gas: range [0, 1]
    # action[2] is brake: range [0, 1]
    return np.array([random.uniform(-1, 1), random.uniform(0, 1), random.uniform(0, 1)])


if __name__ == "__main__":
    NUM_CARS = 2

    CAR_CONTROL_KEYS = [[key.LEFT, key.RIGHT, key.UP, key.DOWN]]

    actions = np.zeros((NUM_CARS, 3))


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
                   use_random_direction=True, backwards_flag=True,
                   h_ratio=0.25, use_ego_color=False)

    obs = env.reset()


    for viewer in env.viewer:
        viewer.window.on_key_press = key_press
        viewer.window.on_key_release = key_release

    record_video = False
    if record_video:
        from gym.wrappers.monitor import Monitor

        env = Monitor(env, '/tmp/video-test', force=True)

    isopen = True
    stopped = False
    while isopen and not stopped:
        obs = env.reset()
        total_reward = np.zeros(NUM_CARS)
        steps = 0
        restart = False
        while True:
            actions[1] = random_policy(obs[1])

            obs, r, done, info = env.step(actions)
            total_reward += r
            if steps % 200 == 0 or done:
                print("\nActions: " + str.join(" ", [f"Car {x}: " + str(actions[x]) for x in range(NUM_CARS)]))
                print(f"Step {steps} Total_reward " + str(total_reward))
                # import matplotlib.pyplot as plt
                # plt.imshow(s)
                # plt.savefig("test.jpeg")
            steps += 1
            isopen = env.render().all()
            if stopped or done or restart or isopen == False:
                break
    env.close()
