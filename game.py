import pygame
import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, MINIGAME_DURATION
from minigames.juego1 import Juego1
from minigames.juego2 import Juego2

class GameManager:
    def __init__(self):
        self.score = 0
        self.state = "start"
        self.timer = 0
        self.result_timer = 2.0
        self.last_result = None
        self.rounds_played = 0

        self.speed_up_timer = 2.0
        self.speed_up_active = False
        self.base_speed = 100

        self.lives = 3
        self.font = pygame.font.SysFont(None, 48)

        self.minigames = [Juego1(), Juego2()]
        self.current_game = None

        self.interlude_timer = 2.5
        self.character_y = WINDOW_HEIGHT // 2
        self.character_direction = 1
        self.character_speed = 120

    def start_new_game(self):
        self.score = 0
        self.lives = 3
        self.rounds_played = 0
        self.state = "interlude"
        self.interlude_timer = 2.5
        self.character_y = WINDOW_HEIGHT // 2
        self.character_direction = 1

    def _start_minigame(self):
        difficulty_level = self.rounds_played // 3
        self.timer = MINIGAME_DURATION
        self.current_game = random.choice(self.minigames)

        if hasattr(self.current_game, 'bar_speed'):
            self.current_game.bar_speed = self.base_speed + difficulty_level * 20
        if hasattr(self.current_game, 'obstacle_speed'):
            self.current_game.obstacle_speed = 250 + difficulty_level * 50
        if hasattr(self.current_game, 'spawn_interval'):
            self.current_game.spawn_interval = max(0.2, 0.7 - difficulty_level * 0.1)

        self.current_game.start()
        self.state = "playing"
        self.speed_up_active = False

    def update(self, dt):
        if self.state == "speed_up":
            self.speed_up_timer -= dt
            if self.speed_up_timer <= 0:
                self.rounds_played += 1
                self._start_minigame()

        elif self.state == "playing":
            self.timer -= dt
            if self.timer <= 0:
                self.current_game.finished = True
                self.current_game.success = False

            self.current_game.update(dt)

            if self.current_game.is_finished():
                self.last_result = bool(self.current_game.was_successful())
                if self.last_result:
                    self.score += 1
                else:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.state = "game_over"
                        return

                self.state = "result"
                self.result_timer = 2.0

        elif self.state == "result":
            self.result_timer -= dt
            if self.result_timer <= 0:
                self.state = "interlude"
                self.interlude_timer = 2.5
                self.character_y = WINDOW_HEIGHT // 2
                self.character_direction = 1

        elif self.state == "interlude":
            self.character_y += self.character_direction * self.character_speed * dt
            if self.character_y <= 100 or self.character_y >= WINDOW_HEIGHT - 100:
                self.character_direction *= -1

            self.interlude_timer -= dt
            if self.interlude_timer <= 0:
                if self.rounds_played > 0 and self.rounds_played % 3 == 0:
                    self.state = "speed_up"
                    self.speed_up_timer = 2.0
                else:
                    self.rounds_played += 1
                    self._start_minigame()

    def draw(self, screen):
        screen.fill((0, 0, 0))

        if self.state == "start":
            text = self.font.render(f"Puntuación: {self.score}", True, (255, 255, 255))
            screen.blit(text, (20, 20))

            info = self.font.render("Presiona ENTER para jugar", True, (200, 200, 200))
            screen.blit(info, (WINDOW_WIDTH // 2 - info.get_width() // 2, WINDOW_HEIGHT // 2))

        elif self.state == "playing":
            if self.current_game:
                self.current_game.draw(screen)
            timer_text = self.font.render(f"Tiempo: {int(self.timer)}", True, (255, 255, 255))
            screen.blit(timer_text, (WINDOW_WIDTH - 200, 20))

            score_text = self.font.render(f"Puntos: {self.score}", True, (255, 255, 255))
            screen.blit(score_text, (20, 20))

            lives_text = self.font.render(f"Vidas: {self.lives}", True, (255, 255, 255))
            screen.blit(lives_text, (20, 60))

        elif self.state == "result":
            if self.last_result:
                result_text = self.font.render("¡Ganaste!", True, (0, 255, 0))
            else:
                result_text = self.font.render("Perdiste", True, (255, 0, 0))
            screen.blit(result_text, (WINDOW_WIDTH // 2 - result_text.get_width() // 2, WINDOW_HEIGHT // 2))

            score_text = self.font.render(f"Puntuación: {self.score}", True, (255, 255, 255))
            screen.blit(score_text, (20, 20))

        elif self.state == "interlude":
            pygame.draw.rect(screen, (0, 128, 255), (WINDOW_WIDTH // 2 - 25, int(self.character_y), 50, 50))

            lives_text = self.font.render(f"Vidas: {self.lives}", True, (255, 255, 255))
            screen.blit(lives_text, (20, 20))

        elif self.state == "speed_up":
            speed_text = self.font.render("¡Más rápido!", True, (255, 215, 0))
            screen.blit(speed_text, (WINDOW_WIDTH // 2 - speed_text.get_width() // 2, WINDOW_HEIGHT // 2))

        elif self.state == "game_over":
            over_text = self.font.render("¡Fin del juego!", True, (255, 0, 0))
            screen.blit(over_text, (WINDOW_WIDTH // 2 - over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 40))

            score_text = self.font.render(f"Puntuación final: {self.score}", True, (255, 255, 255))
            screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2 + 20))

            restart_text = self.font.render("Presiona ENTER para reiniciar", True, (200, 200, 200))
            screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 80))

    def handle_event(self, event):
        if self.state in ["start", "game_over"]:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.start_new_game()
        elif self.state == "playing" and self.current_game:
            self.current_game.handle_event(event)

    def is_round_over(self):
        return self.current_game.is_finished() if self.current_game else False

    def get_result(self):
        return self.current_game.was_successful() if self.current_game else False
