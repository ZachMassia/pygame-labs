#!/usr/bin/env python
import sys
import pygame
from pygame.math import Vector2
from basic_game.app import App


class Game(object):

    # Class constants:
    KEY = 0
    MOUSE = 1
    JOY = 2

    def __init__(self):
        self.evt_mgr = None   # Injected by App
        self.scr_surf = None  # Injected by App

        self.sounds = list()

    def update(self, dt):
        """Update the game logic."""
        pass

    def draw(self):
        """Blit surfaces to the display surface."""
        for m in self.marios:
            m.draw(self.scr_surf)

    def build(self):
        """Called before the game loop starts and after pygame is initialized."""
        self.setup_event_handlers()

        # Use key repeat
        pygame.key.set_repeat(250, 25)

    def setup_event_handlers(self):
        """Register methods with specific Pygame events."""
        pass


if __name__ == '__main__':
    # Create the configuration dict.
    cfg = {
        'SCR_SIZE': (640, 480),
        'SCR_CAP': 'Pygame and Python 3 Test',
        'SCR_FLAGS': pygame.HWSURFACE | pygame.DOUBLEBUF
    }

    # Initialize the app and run it.
    app = App(cfg, Game())
    app.run()
