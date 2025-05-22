# minigames/minigame_base.py

import pygame

# minigames/minigame_base.py

class MinigameBase:
    def __init__(self):
        self.finished = False
        self.success = False

    def start(self):
        """Inicializa el minijuego. Se llama cuando empieza."""
        self.finished = False
        self.success = False

    def update(self, dt):
        """Actualiza la lógica del minijuego.

        Args:
            dt (float): tiempo transcurrido en segundos desde el último frame.
        """
        pass

    def draw(self, screen):
        """Dibuja el minijuego en la pantalla.

        Args:
            screen (pygame.Surface): superficie donde dibujar.
        """
        pass

    def handle_event(self, event):
        """Maneja eventos de entrada (teclado, mouse, etc).

        Args:
            event (pygame.Event): evento a manejar.
        """
        pass

    def is_finished(self):
        """Indica si el minijuego terminó."""
        return self.finished

    def was_successful(self):
        """Indica si el jugador ganó el minijuego."""
        return self.success
