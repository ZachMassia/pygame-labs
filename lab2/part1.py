#!/usr/bin/env python
import pygame
from basic_game.app import App


class Game(object):

    def __init__(self):
        self.evt_mgr = None   # Injected by App
        self.scr_surf = None  # Injected by App

        self.sounds = list()
        self.mario_img = None

        self.input_vec = pygame.math.Vector2()
        self.key_mario_pos = pygame.math.Vector2()
        self.mouse_mario_pos = pygame.math.Vector2()

    def update(self, dt):
        """Update the game logic."""
        self.key_mario_pos += self.input_vec * dt
        self.mouse_mario_pos = pygame.mouse.get_pos()

        # Reset input vec.
        self.input_vec = pygame.math.Vector2()

    def draw(self):
        """Blit surfaces to the display surface."""
        # Keyboard Mario
        self.scr_surf.blit(self.mario_img, (self.key_mario_pos.x,
                                            self.key_mario_pos.y))
        # Mouse Mario
        self.scr_surf.blit(self.mario_img, self.mouse_mario_pos)

    def build(self):
        """Called before the game loop starts and after pygame is initialized."""
        self.setup_event_handlers()
        self.load_mario_img()
        self.load_sounds()

        # Use key repeat
        pygame.key.set_repeat(250, 25)

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

        if self.input_vec.length() > 0 and not self.input_vec.is_normalized():
            self.input_vec.normalize_ip()

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
        for i in range(0, 4):
            try:
                sound = pygame.mixer.Sound(file='sound{}.ogg'.format(i))
                self.sounds.append(sound)
            except pygame.error:
                # TODO: Should this cause the game to shutdown?
                continue

    def setup_event_handlers(self):
        """Register methods with specific Pygame events."""
        self.evt_mgr.subscribe(pygame.KEYDOWN, self.move_key_mario)
        self.evt_mgr.subscribe(pygame.KEYDOWN, self.play_key_sounds)
        self.evt_mgr.subscribe(pygame.MOUSEBUTTONDOWN, self.play_mouse_sound)
3

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
