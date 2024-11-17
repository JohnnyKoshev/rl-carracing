import multiprocessing
import time

import numpy as np
import gym
import pygame
from pyglet.window import key
from stable_baselines3 import DQN, PPO, SAC
from stable_baselines3.common.vec_env import DummyVecEnv, VecTransposeImage
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.env_util import make_vec_env

from player import player_vs_cars
from bots import bots_only

def run_with_retries(target, retries=5):
    attempt = 0
    while attempt < retries:
        process = multiprocessing.Process(target=target)
        process.start()
        process.join()

        if process.exitcode == 0:
            return  # Exit if the process finished successfully
        else:
            print(f"Process failed with exit code {process.exitcode}. Retrying... ({attempt + 1}/{retries})")
            attempt += 1
            time.sleep(1)  # Add a slight delay before retrying

    print("Max retries reached. Exiting.")



def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Car Racing")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    menu_items= ["1. Player vs RL Models", "2. RL Models only"]
    selected_item = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    pygame.quit()
                    if selected_item == 0:
                        run_with_retries(player_vs_cars)
                    elif selected_item == 1:
                        run_with_retries(bots_only)

        for i, item in enumerate(menu_items):
            if i == selected_item:
                text = font.render(item, True, (255, 0, 0))
            else:
                text = font.render(item, True, (255, 255, 255))
            screen.blit(text, (100, 100 + i * 40))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main_menu()