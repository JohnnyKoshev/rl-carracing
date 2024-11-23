import multiprocessing
import threading
import time
import pygame
from player import player_vs_cars
from bots import bots_only


def run_with_retries(target, retries=10):
    attempt = 0
    while attempt < retries:
        process = multiprocessing.Process(target=target)
        process.start()
        process.join()

        if process.exitcode == 0:
            return  # Exit if the process finished successfully
        else:
            print(f"Initialization Step: ({attempt + 1})")
            attempt += 1
            time.sleep(1)  # Add a slight delay before retrying

    print("Max retries reached. Exiting.")


def play_background_music():
    pygame.mixer.init()  # Initialize the mixer for audio playback
    pygame.mixer.music.load("music.mp3")  # Replace with your music file path
    pygame.mixer.music.set_volume(0.4)  # Set volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # Play the music in a loop (-1 for infinite looping)


def selected_item_function(selected_item):
    pygame.quit()
    if selected_item == 0:
        run_with_retries(player_vs_cars)
    elif selected_item == 1:
        run_with_retries(bots_only)


def main_menu():
    pygame.init()

    play_background_music()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("RL Car Racing")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)
    footer_font = pygame.font.Font(None, 24)

    # Load background image
    background_image = pygame.image.load("menu.png")  # Replace with your image path
    background_image = pygame.transform.scale(background_image, (800, 600))

    title = "RL Car Racing"
    footer = "Abdulaziz Zakirov, Komiljon Yuldashev"

    menu_items = ["1. Player vs RL Models", "2. RL Models only"]
    selected_item = 0

    while True:
        screen.blit(background_image, (0, 0))  # Draw the background image

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
                    selected_item_function(selected_item)
                    return  # Exit after the process is completed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click (or tap)
                    mouse_pos = event.pos
                    for i, item in enumerate(menu_items):
                        item_rect = pygame.Rect(100, 150 + i * 40, 600, 40)
                        if item_rect.collidepoint(mouse_pos):
                            selected_item_function(i)
                            return  # Exit after the process is completed
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for i, item in enumerate(menu_items):
                    item_rect = pygame.Rect(100, 150 + i * 40, 600, 40)
                    if item_rect.collidepoint(mouse_pos):
                        selected_item = i

        title_text = title_font.render(title, True, (255, 255, 0))
        screen.blit(title_text, (400 - title_text.get_width() // 2, 50))

        for i, item in enumerate(menu_items):
            if i == selected_item:
                text = font.render(item, True, (255, 0, 0))
            else:
                text = font.render(item, True, (255, 255, 255))
            screen.blit(text, (100, 150 + i * 40))

        footer_font = pygame.font.Font(None, 32)

        shadow_text = footer_font.render(footer, True, (0, 0, 0))
        screen.blit(shadow_text, (400 - shadow_text.get_width() // 2 + 3, 550 + 3))

        footer_text = footer_font.render(footer, True, (255, 255, 255))
        screen.blit(footer_text, (400 - footer_text.get_width() // 2, 550))

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.mixer.music.stop()  # Stop music on exit
        exit(0)
