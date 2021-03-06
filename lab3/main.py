#!/usr/bin/env python
import sys
import random
import pygame
from pygame.math import Vector2

from basic_game.app import App
from sprites import Car, FinishLine
from hud import HUD


class Game(object):
    """Main game class. Contains all game logic."""

    def __init__(self):
        # The following objects are injected by the App class.
        self.evt_mgr = None
        self.scr_surf = None
        self.logging_enabled = False

        self.sounds = dict()
        self.sprites = pygame.sprite.Group()
        self.finish_line = None
        self.background = None
        self.racing = False

        self.hud = None

    def update(self, dt):
        """Update the game logic."""
        if self.racing:
            self.update_car_vel(dt)
            self.check_for_winner()

        self.sprites.update(dt)

    def draw(self):
        """Blit surfaces to the display surface."""
        self.scr_surf.blit(self.background, (0, 0))
        self.scr_surf.blit(self.finish_line.image, self.finish_line.rect)
        self.sprites.draw(self.scr_surf)
        self.hud.draw()

    def build(self):
        """Called before the game loop starts."""
        self.setup_cars()
        self.setup_finish_line()
        self.setup_event_handlers()
        self.setup_hud()

        # Load the background and scale to screen size.
        self.background = pygame.image.load('street.png')
        self.background = pygame.transform.scale(self.background,
                                                 self.scr_surf.get_size())

        # Set the delay before a key starts repeating, and the repeat rate.
        pygame.key.set_repeat(250, 25)

        self.hud.flash("Press G to start, R to reset", 2500)

        try:
            self.sounds['race_start'] = pygame.mixer.Sound(file='gunshot.ogg')
            self.sounds['race_end'] = pygame.mixer.Sound(file='winner.ogg')
        except pygame.error:
            print('Error loading sounds: {}'.format(pygame.get_error()))
            exit(1)

        if self.logging_enabled:
            import logging
            logging.info('Game done building.')

    def on_keydown(self, evt):
        """Start or restart the race."""
        if evt.key == pygame.K_g:
            self.start_race()
        elif evt.key == pygame.K_r:
            self.reset_cars()

    def update_car_vel(self, dt):
        """Set both car's velocities to a random float from 0 to 1."""
        for car in self.sprites:
            car.vel.x = 0.01 + random.random()

    def check_for_winner(self):
        """Check if either car has hit the finish line."""
        collisions = pygame.sprite.spritecollide(self.finish_line, self.sprites,
                                                 False)
        n = len(collisions)
        log_msg = ''

        if n >= 2:
            log_msg = 'Race was a tie.'
            for car in self.sprites:
                car.adj_score(1)
                self.move_car_to_finish_area(car)
        elif n == 1:
            winner = collisions[0]
            log_msg = '{} won the race.'.format(winner)
            winner.adj_score(1)
            self.move_car_to_finish_area(winner)

        if log_msg:  # At least one car hit the finish line.
            self.racing = False
            self.play_sound('race_end')

            # Stop both cars.
            for car in self.sprites:
                car.vel.x = 0

            self.hud.flash(log_msg, 2250)

            if self.logging_enabled:
                logging.info(log_msg)

    def start_race(self):
        """Start a new race."""
        if self.logging_enabled:
            logging.info('Starting a new race')

        self.reset_cars()
        self.racing = True
        self.play_sound('race_start')

    def reset_cars(self):
        """Reset all cars to the left side and set velocity to 0."""
        if self.logging_enabled:
            logging.debug('Resetting cars')

        for car in self.sprites:
            # Move to the left side.
            car.rect.x = 0
            car.vel.x = 0

            # Set the red car on top, and blue car bellow.
            scr_y = self.scr_surf.get_size()[1]
            half_car = car.image.get_size()[1] / 2
            if car.name == 'red_car':
                car.rect.y = scr_y * 0.37 - half_car
            elif car.name == 'blue_car':
                car.rect.y = scr_y * 0.62 - half_car

    def setup_cars(self):
        """Initialize the Car sprites."""
        # Create cars using colored blocks for now.
        size = (64, 64)

        red_car = Car('red_car', pygame.Surface(size))
        red_car.image.fill((255, 0, 0))

        blue_car = Car('blue_car', pygame.Surface(size))
        blue_car.image.fill((0, 0, 255))

        # Register the cars with the sprite group.
        self.sprites.add(red_car, blue_car)

        # Give the cars their initial position.
        self.reset_cars()

    def move_car_to_finish_area(self, car):
        """Moves a car into the area after the finish line."""
        scr_x = self.scr_surf.get_size()[0]
        finish_line_left = self.finish_line.rect.x + self.finish_line.rect.width
        finish_area_mid_point = scr_x - ((scr_x - finish_line_left) / 2)

        car.rect.x = finish_area_mid_point - (car.rect.width / 2)

    def setup_finish_line(self):
        """Create the finish line surface."""
        self.finish_line = FinishLine('finish', self.scr_surf, 0.03, 0.8)

    def setup_hud(self):
        """Create the HUD object"""
        scr_x, scr_y = self.scr_surf.get_size()

        # Scale font based on screen size.
        font_height = 0.075
        max_width = 0.2

        # Create the HUD and register cars.
        self.hud = HUD(
            target=self.scr_surf,
            font_size=(scr_y * font_height),
            width=(scr_x * max_width),
            flash_size=(scr_x, (scr_y * font_height * 2))
        )
        self.hud.register_cars(self.sprites.sprites())

    def setup_event_handlers(self):
        """Register methods with specific Pygame events."""
        self.evt_mgr.subscribe(pygame.KEYDOWN, self.on_keydown)

    def play_sound(self, name):
        "Plays a sound and catches any exceptions."
        try:
            self.sounds[name].play()
        except IndexError:
            print('Error: sound {} not loaded.'.format(name))
        except pygame.error:
            print('Error: could not play sound {}.'.format(name))

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
