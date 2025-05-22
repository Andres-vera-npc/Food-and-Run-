# main.py

import pygame
from game import GameManager
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Food and Run!!!")
    clock = pygame.time.Clock()

    game_manager = GameManager()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game_manager.handle_event(event)

        game_manager.update(dt)
        game_manager.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
