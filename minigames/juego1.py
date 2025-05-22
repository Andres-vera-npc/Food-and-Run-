# minigames/juego1.py

import pygame
from minigames.minigame_base import MinigameBase
from config import WHITE, BLACK, WINDOW_WIDTH, WINDOW_HEIGHT, MINIGAME_DURATION

class Juego1(MinigameBase):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("arial", 36)
        self.background_color = BLACK

        self.bar_max = 100
        self.bar_value = 0
        self.bar_rect = pygame.Rect(100, WINDOW_HEIGHT // 2, 400, 40)
        self.bar_speed = 20  # cuánto se llena por pulsación, cambiará con dificultad

    def start(self):
        self.finished = False
        self.success = False
        self.bar_value = 0

    def update(self, dt):
        # Si la barra se llena antes del tiempo, gana
        if self.bar_value >= self.bar_max:
            self.finished = True
            self.success = True

    def draw(self, screen):
        screen.fill(self.background_color)

        # Dibuja barra vacía
        pygame.draw.rect(screen, (100, 100, 100), self.bar_rect)

        # Dibuja barra llena proporcional
        fill_width = int((self.bar_value / self.bar_max) * self.bar_rect.width)
        fill_rect = pygame.Rect(self.bar_rect.x, self.bar_rect.y, fill_width, self.bar_rect.height)
        pygame.draw.rect(screen, (0, 255, 0), fill_rect)

        # Instrucciones
        instr = self.font.render("Presiona ESPACIO rápido para llenar la barra", True, WHITE)
        screen.blit(instr, (50, self.bar_rect.y - 50))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.bar_value += self.bar_speed
            if self.bar_value > self.bar_max:
                self.bar_value = self.bar_max
