#!/usr/bin/env python
import pygame
from .basic_game.app import App


class Game(object):

    def __init__(self):
        self.evt_mgr = None   # Injected by App
        self.SCR_SURF = None  # Injected by App

        self.input_vec = pygame.math.Vector2()
        self.key_mario_pos = pygame.math.Vector2()
        self.mouse_mario_pos = pygame.math.Vector2()

    def update(self, dt):
        """Update the game logic."""
        self.key_mario_pos += self.input_vec * dt
        self.mouse_mario_pos = pygame.mouse.get_pos()

        self.input_vec = pygame.math.Vector2()  # reset input vec.

    def draw(self):
        """Blit surfaces to the display surface."""
        # Keyboard Mario
        self.SCR_SURF.blit(self.mario_img, (self.key_mario_pos.x,
                                            self.key_mario_pos.y))
        # Mouse Mario
        self.SCR_SURF.blit(self.mario_img, self.mouse_mario_pos)

    def build(self):
        """Called before the game loop starts."""
        # Load mario at scale him
        self.mario_img = pygame.image.load("mario.png")
        self.mario_img = pygame.transform.scale(self.mario_img, (64, 64))
        # Use (0,0) as colorkey
        self.mario_img.set_colorkey(self.mario_img.get_at((0, 0)))

        self.setup_event_handlers()

        # Use key repeat
        pygame.key.set_repeat(25, 25)

    def move_key_mario(self, evt):
        """Update the keyboard input vector on key down."""
        # X Axis
        if evt.key == pygame.K_LEFT:
            self.input_vec.x = -1
        elif evt.key == pygame.K_RIGHT:
            self.input_vec.x = 1
        else:
            self.input_vec.x = 0

        # Y Axis
        if evt.key == pygame.K_UP:
            self.input_vec.y = -1
        elif evt.key == pygame.K_DOWN:
            self.input_vec.y = 1
        else:
            self.input_vec.y = 0

        if not self.input_vec.is_normalized():
            self.input_vec.normalize()

    def play_key_sounds(self, evt):
        """Play sounds for number keys 1-4."""
        num = None

        if evt.key == pygame.K_1:
            num = 1
        elif evt.key == pygame.K_2:
            num = 2
        elif evt.key == pygame.K_3:
            num = 3
        elif evt.key == pygame.K_4:
            num = 4
        #TODO Actually play the sound

    def setup_event_handlers(self):
        self.evt_mgr.subscribe(pygame.KEYDOWN, self.move_key_mario)
        self.evt_mgr.subscribe(pygame.KEYDOWN, self.play_key_sounds)


if __name__ == '__main__':
    app = App({
        'SCR_SIZE': (640, 480),
        'SCR_CAP': 'Pygame and Python 3 Test',
        'SCR_FLAGS': pygame.HWSURFACE | pygame.DOUBLEBUF
    }, Game())
    app.run()
