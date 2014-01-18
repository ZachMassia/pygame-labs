#!/usr/bin/env python
import sys
import pygame
from pygame.math import Vector2
from basic_game.app import App
from mario import Mario


class Game(object):

    def __init__(self):
        self.evt_mgr = None   # Injected by App
        self.scr_surf = None  # Injected by App

        self.sounds = list()
        self.mario_img = None
        self.marios = dict()

        self.input_vec = Vector2()

    def update(self, dt):
        """Update the game logic."""
        self.marios['key'].set_dir(self.input_vec)

        # Get the unit vector pointing to the mouse from mouse mario's
        # current location.
        new_dir = Vector2(pygame.mouse.get_pos()) - self.marios['mouse'].pos

        dead_zone = 10   # keeps jittering effect from happening.
        if new_dir.length() > dead_zone:
            self.marios['mouse'].set_dir(new_dir)
        else:
            self.marios['mouse'].set_dir(Vector2(0, 0))

        [m.update(dt) for m in self.marios.values()]

        # Reset input vec.
        self.input_vec = pygame.math.Vector2()

    def draw(self):
        """Blit surfaces to the display surface."""
        [m.draw(self.scr_surf) for m in self.marios.values()]

    def build(self):
        """Called before the game loop starts and after pygame is initialized."""
        self.setup_event_handlers()
        self.load_mario_img()
        self.load_sounds()

        try:
            self.marios['key'] = Mario(self.mario_img, Vector2(0, 0))
            self.marios['mouse'] = Mario(self.mario_img, Vector2(self.scr_surf.get_width() - self.mario_img.get_width(), 0))
            self.marios['joy'] = Mario(self.mario_img, Vector2(0, self.scr_surf.get_height() - self.mario_img.get_height()))
        except ValueError:
            print('Couldn\'t create marios')
            sys.exit(-1)

        # Use key repeat
        pygame.key.set_repeat(250, 25)

    def update_key_input_vec(self, evt):
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

    def play_key_sounds(self, evt):
        """Play sounds for number keys 1-4."""
        if evt.key == pygame.K_1:
            self.safely_play_sound(0)
        elif evt.key == pygame.K_2:
            self.safely_play_sound(1)
        elif evt.key == pygame.K_3:
            self.safely_play_sound(2)
        elif evt.key == pygame.K_4:
            self.safely_play_sound(3)

    def play_mouse_sound(self, evt):
        """Play sounds for mouse buttons."""
        self.safely_play_sound(evt.button)

    def safely_play_sound(self, index):
        """Wraps a call to Sound.play() in a try/except."""
        try:
            self.sounds[index].play()
        except IndexError:
            print('Error: sound {} not loaded.'.format(index))
        except pygame.error:
            print('Error: could not play sound {}.'.format(index))

    def load_mario_img(self):
        """Load mario and scale him."""
        self.mario_img = pygame.image.load("mario.png")
        self.mario_img = pygame.transform.scale(self.mario_img, (64, 64))

        # Use (0,0) as color key
        self.mario_img.set_colorkey(self.mario_img.get_at((0, 0)))

    def load_sounds(self):
        """Load all required sound effects."""
        for i in range(4):
            try:
                sound = pygame.mixer.Sound(file='sound{}.ogg'.format(i))
                self.sounds.append(sound)
            except pygame.error:
                # TODO: Should this cause the game to shutdown?
                continue

    def setup_event_handlers(self):
        """Register methods with specific Pygame events."""
        self.evt_mgr.subscribe(pygame.KEYDOWN, self.update_key_input_vec)
        self.evt_mgr.subscribe(pygame.KEYDOWN, self.play_key_sounds)
        self.evt_mgr.subscribe(pygame.MOUSEBUTTONDOWN, self.play_mouse_sound)


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
