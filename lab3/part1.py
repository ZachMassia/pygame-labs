#!/usr/bin/env python
import sys
import pygame
from pygame.math import Vector2
from basic_game.app import App
from sprites import Car, FinishLine


class Game(object):
    """Main game class. Contains all game logic."""

    def __init__(self):
        # The following objects are injected by the App class.
        self.evt_mgr = None
        self.scr_surf = None
        self.logging_enabled = False

        self.sounds = list()
        self.sprites = pygame.sprite.Group()
        self.finish_line = None

    def update(self, dt):
        """Update the game logic."""
        self.sprites.update(dt)
        self.check_for_winner()

    def draw(self):
        """Blit surfaces to the display surface."""
        self.scr_surf.blit(self.finish_line.image, self.finish_line.rect)
        self.sprites.draw(self.scr_surf)

    def build(self):
        """Called before the game loop starts and after pygame is initialized."""
        self.setup_cars()
        self.setup_finish_line()
        self.setup_event_handlers()

        # Set the delay before a key starts repeating, and the repeat rate.
        pygame.key.set_repeat(250, 25)

        if self.logging_enabled:
            import logging
            logging.info('Game done building.')

    def on_keydown(self, evt):
        """Start or restart the race."""
        if evt.key == pygame.K_g:
            self.start_race()
        elif evt.key == pygame.K_r:
            self.reset_cars()

    def check_for_winner(self):
        """Check if either car has hit the finish line."""
        collisions = pygame.sprite.spritecollide(self.finish_line, self.sprites, False)
        n = len(collisions)
        log_msg = ''

        if n >= 2:
            log_msg = 'Race was a tie.'
            self.reset_cars()
        elif n == 1:
            log_msg = '{} won the race.'.format(collisions[0])
            self.reset_cars()

        if log_msg and self.logging_enabled:
            logging.info(log_msg)

    def start_race(self):
        """Start a new race."""
        if self.logging_enabled:
            logging.info('Starting a new race')

    def reset_cars(self):
        """Reset all cars to the left side and set velocity to 0."""
        if self.logging_enabled:
            logging.info('Resetting cars')

        for car in self.sprites:
            car.rect.x = 0
            car.vel.x = 0

    def setup_cars(self):
        """Initialize the Car sprites."""
        # Create cars using colored blocks for now.
        size = (64, 64)
        x_vel = 0.5

        red_car = Car('red_car', pygame.Surface(size))
        red_car.image.fill((255, 0, 0))
        red_car.vel.x = x_vel

        blue_car = Car('blue_car', pygame.Surface(size))
        blue_car.image.fill((0, 0, 255))
        blue_car.rect.y = size[1]
        blue_car.vel.x = x_vel * 0.9

        # Register the cars with the Sprite group.
        self.sprites.add(red_car, blue_car)

    def setup_finish_line(self):
        """Create the finish line surface."""
        self.finish_line = FinishLine('finish', self.scr_surf, 0.03, 0.8)

    def setup_event_handlers(self):
        """Register methods with specific Pygame events."""
        self.evt_mgr.subscribe(pygame.KEYDOWN, self.on_keydown)


if __name__ == '__main__':
    import logging
    # Create the configuration dict.
    cfg = {
        'SCR_SIZE': (1024, 480),
        'SCR_CAP': 'Pygame and Python 3 Test',
        'SCR_FLAGS': pygame.HWSURFACE | pygame.DOUBLEBUF,
        'LOGGING': 'True',
        'LOG_LEVEL': logging.DEBUG,
        'LOG_FILE': 'log.txt'
    }

    # Initialize the app and run it.
    app = App(cfg, Game())
    app.run()
