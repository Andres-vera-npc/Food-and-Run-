# minigames/juego2.py

# minigames/juego2.py

import pygame
import random
from minigames.minigame_base import MinigameBase
from config import WHITE, BLACK, RED, BLUE, WINDOW_WIDTH, WINDOW_HEIGHT, MINIGAME_DURATION

class Juego2(MinigameBase):
    def __init__(self):
        super().__init__()
        self.player_size = 50
        self.player_pos = pygame.Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)
        self.player_speed = 300  # pixeles por segundo

        self.obstacle_size = 40
        self.obstacle_speed = 250
        self.obstacles = []

        self.spawn_timer = 0
        self.spawn_interval = 0.7  # segundos entre obstáculos

        self.font = pygame.font.SysFont("arial", 36)
        self.background_color = BLACK

        self.elapsed_time = 0  # tiempo que ha pasado en el minijuego

    def start(self):
        self.finished = False
        self.success = False
        self.player_pos = pygame.Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)
        self.obstacles.clear()
        self.spawn_timer = 0
        self.elapsed_time = 0  # reiniciar contador

    def update(self, dt):
        self.elapsed_time += dt

        # Si ya pasó el tiempo límite, gana el jugador
        if self.elapsed_time >= MINIGAME_DURATION:
            self.finished = True
            self.success = True
            return  # para no seguir actualizando

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_pos.x -= self.player_speed * dt
        if keys[pygame.K_RIGHT]:
            self.player_pos.x += self.player_speed * dt

        # Limitar al ancho de la pantalla
        self.player_pos.x = max(0, min(WINDOW_WIDTH - self.player_size, self.player_pos.x))

        # Controlar aparición de obstáculos
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            x_pos = random.randint(0, WINDOW_WIDTH - self.obstacle_size)
            self.obstacles.append(pygame.Rect(x_pos, -self.obstacle_size, self.obstacle_size, self.obstacle_size))
            self.spawn_timer = self.spawn_interval

        # Mover obstáculos hacia abajo
        for obs in self.obstacles:
            obs.y += int(self.obstacle_speed * dt)

        # Quitar obstáculos fuera de pantalla
        self.obstacles = [o for o in self.obstacles if o.y < WINDOW_HEIGHT]

        player_rect = pygame.Rect(self.player_pos.x, self.player_pos.y, self.player_size, self.player_size)

        # Revisar colisiones con obstáculos
        for obs in self.obstacles:
            if player_rect.colliderect(obs):
                self.finished = True
                self.success = False

    def draw(self, screen):
        screen.fill(self.background_color)

        # Dibujar jugador (cuadro azul)
        pygame.draw.rect(screen, BLUE, (self.player_pos.x, self.player_pos.y, self.player_size, self.player_size))

        # Dibujar obstáculos (cuadros rojos)
        for obs in self.obstacles:
            pygame.draw.rect(screen, RED, obs)

        # Texto de instrucciones (centrado abajo)
        instr = self.font.render("Esquiva los cuadros rojos con las flechas", True, WHITE)
        instr_rect = instr.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        screen.blit(instr, instr_rect)