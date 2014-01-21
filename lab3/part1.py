#!/usr/bin/env python
import sys
import pygame
from pygame.math import Vector2
from basic_game.app import App
from car import Car


class Game(object):

    def __init__(self):
        self.evt_mgr = None   # Injected by App
        self.scr_surf = None  # Injected by App

        self.sounds = list()
        self.cars = pygame.sprite.Group()

    def update(self, dt):
        """Update the game logic."""
        self.cars.update(dt)

    def draw(self):
        """Blit surfaces to the display surface."""
        self.cars.draw(self.scr_surf)

    def build(self):
        """Called before the game loop starts and after pygame is initialized."""
        self.setup_cars()
        self.setup_event_handlers()

        # Use key repeat
        pygame.key.set_repeat(250, 25)

    def setup_cars(self):
        """Initialize the Car sprites."""
        # Create cars using colored blocks for now.
        size = (64, 64)
        x_vel = 0.5

        red_car = Car(pygame.Surface(size))
        red_car.image.fill((255, 0, 0))
        red_car.vel.x = x_vel

        blue_car = Car(pygame.Surface(size))
        blue_car.image.fill((0, 0, 255))
        blue_car.rect.y = size[1]
        blue_car.vel.x = x_vel * 0.9

        # Register the cars with the Sprite group.
        self.cars.add(red_car, blue_car)

    def setup_event_handlers(self):
        """Register methods with specific Pygame events."""
        pass


if __name__ == '__main__':
    # Create the configuration dict.
    cfg = {
        'SCR_SIZE': (1024, 480),
        'SCR_CAP': 'Pygame and Python 3 Test',
        'SCR_FLAGS': pygame.HWSURFACE | pygame.DOUBLEBUF
    }

    # Initialize the app and run it.
    app = App(cfg, Game())
    app.run()
