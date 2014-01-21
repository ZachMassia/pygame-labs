#!/usr/bin/env python
import sys
import pygame
from pygame.math import Vector2
from basic_game.app import App
from mario import Mario


class Game(object):

    # Class constants:
    KEY = 0
    MOUSE = 1
    JOY = 2

    def __init__(self):
        self.evt_mgr = None   # Injected by App
        self.scr_surf = None  # Injected by App

        self.sounds = list()
        self.mario_img = None
        self.marios = list()

        self.input_vec = Vector2()
        self.joystick = None
        self.joy_vec = Vector2()

    def update(self, dt):
        """Update the game logic."""
        self.marios[Game.KEY].set_dir(self.input_vec)
        self.marios[Game.JOY].set_dir(self.joy_vec)

        # Get the unit vector pointing to the mouse from mouse mario's
        # current location.
        new_dir = Vector2(pygame.mouse.get_pos()) - self.marios[Game.MOUSE].pos

        # Keep Mario from moving when the mouse stops.
        dead_zone = 10
        if new_dir.length() > dead_zone:
            self.marios[Game.MOUSE].set_dir(new_dir)
        else:
            self.marios[Game.MOUSE].set_dir(Vector2(0, 0))

        for i, mario in enumerate(self.marios):
            hit_scr_edge = self.clamp_to_screen(mario)
            if hit_scr_edge:
                self.safely_play_sound(i)
            mario.update(dt)

        # Reset input vec.
        self.input_vec = pygame.math.Vector2()

    def draw(self):
        """Blit surfaces to the display surface."""
        for m in self.marios:
            m.draw(self.scr_surf)

    def build(self):
        """Called before the game loop starts and after pygame is initialized."""
        self.setup_event_handlers()
        self.load_mario_img()
        self.load_sounds()

        top_left = Vector2(5, 5)
        top_right = Vector2(self.scr_surf.get_width() - self.mario_img.get_width() - 5, 5)
        bottom_left = Vector2(5, self.scr_surf.get_height() - self.mario_img.get_height() - 5)

        try:
            self.marios.extend([
                Mario("key", self.mario_img, top_left),
                Mario("mouse", self.mario_img, top_right),
                Mario("joy", self.mario_img, bottom_left)
            ])
        except ValueError:
            print("Couldn't create marios")
            sys.exit(-1)

        for m in self.marios:
            # Register each Mario with the other two.
            others = [o for o in self.marios if o != m]
            m.enemies.extend(others)
            # Add the collision callback.
            m.on_collision = self.handle_collisions

        # Use key repeat
        pygame.key.set_repeat(250, 25)

        # Connect joystick if available
        pygame.joystick.init()
        if pygame.joystick.get_count() >= 1:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def handle_collisions(self, mario):
        """Fire off a sound based on the mario who was hit."""
        # TODO: Timer to prevent spamming a sound
        if mario.name == 'key':
            self.safely_play_sound(0)
        elif mario.name == 'mouse':
            self.safely_play_sound(1)
        elif mario.name == 'joy':
            self.safely_play_sound(2)

    def clamp_to_screen(self, mario):
        """Limits the vector to the screen bounds.

        Returns true when mario was outside the screen.

        """
        def clamp(x, minimum, maximum):
            """Clamp a single value to a range."""
            return max(minimum, min(x, maximum))

        scr = Vector2(self.scr_surf.get_size())
        new_pos = Vector2(
            clamp(mario.pos.x, 0, scr.x),
            clamp(mario.pos.y, 0, scr.y)
        )

        # Check if any change was made
        if new_pos == mario.pos:
            return False
        else:
            mario.pos = new_pos
            return True

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

    def update_joy_input_vec(self, evt):
        """Update the joystick input vector on axis movement."""
        X = 0
        Y = 1
        if evt.axis == X:
            self.joy_vec.x = evt.value
        elif evt.axis == Y:
            self.joy_vec.y = evt.value

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

    def play_joy_sound(self, evt):
        """Play sounds for joystick buttons."""
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
        self.evt_mgr.subscribe_list([
            (pygame.KEYDOWN, self.update_key_input_vec),
            (pygame.KEYDOWN, self.play_key_sounds),
            (pygame.MOUSEBUTTONDOWN, self.play_mouse_sound),
            (pygame.JOYBUTTONDOWN, self.play_joy_sound),
            (pygame.JOYAXISMOTION, self.update_joy_input_vec)
        ])


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
