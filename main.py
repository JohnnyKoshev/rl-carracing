import multiprocessing
import time
import pygame
from player import player_vs_cars
from bots import bots_only
import fontTools


def run_with_retries(target, retries=10):
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
    pygame.mixer.init()  # Initialize the mixer for audio playback

    # Load and play background music
    pygame.mixer.music.load("music.mp3")  # Replace with your music file path
    pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # Play the music in a loop (-1 for infinite looping)

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Car Racing")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)
    footer_font = pygame.font.Font(None, 24)

    # Load background image
    background_image = pygame.image.load("background.jpg")  # Replace with your image path
    background_image = pygame.transform.scale(background_image, (800, 600))

    title = "Car Racists"
    footer = "U2110292 Abdulaziz Zakirov, U2110289 Komiljon Yuldashev"

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
                    pygame.quit()
                    if selected_item == 0:
                        run_with_retries(player_vs_cars)
                    elif selected_item == 1:
                        run_with_retries(bots_only)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click (or tap)
                    mouse_pos = event.pos
                    for i, item in enumerate(menu_items):
                        item_rect = pygame.Rect(100, 150 + i * 40, 600, 40)
                        if item_rect.collidepoint(mouse_pos):
                            pygame.quit()
                            if i == 0:
                                run_with_retries(player_vs_cars)
                            elif i == 1:
                                run_with_retries(bots_only)
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for i, item in enumerate(menu_items):
                    item_rect = pygame.Rect(100, 150 + i * 40, 600, 40)
                    if item_rect.collidepoint(mouse_pos):
                        selected_item = i

        # Render and display the title
        title_text = title_font.render(title, True, (255, 255, 0))
        screen.blit(title_text, (400 - title_text.get_width() // 2, 50))

        # Render and display menu items
        for i, item in enumerate(menu_items):
            if i == selected_item:
                text = font.render(item, True, (255, 0, 0))
            else:
                text = font.render(item, True, (255, 255, 255))
            screen.blit(text, (100, 150 + i * 40))

        # Render and display the footer
        footer_text = footer_font.render(footer, True, (255, 255, 255))
        screen.blit(footer_text, (400 - footer_text.get_width() // 2, 550))

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        pygame.mixer.music.stop()  # Stop music on exit
        exit(0)