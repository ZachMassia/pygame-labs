#!/usr/bin/env python
import sys
import pygame
from time import clock
from .event import EventManager

class App(object):
    """Responsible for setting up the window and handling events."""

    def __init__(self, cfg, game):
        self.game = game
        self.running = False

        pygame.init()
        pygame.display.set_mode(cfg['SCR_SIZE'], cfg['SCR_FLAGS'])
        pygame.display.set_caption(cfg['SCR_CAP'])

        # Setup Event Manager
        self.evt_mgr = EventManager()
        self.register_events()
        self.game.evt_mgr = self.evt_mgr

        self.clock = pygame.time.Clock()

        self.game.SCR_SURF = pygame.display.get_surface()
        self.game.build()

    def register_events(self):
        """Register a few base event handlers."""
        self.evt_mgr.subscribe(pygame.QUIT,    self.shutdown)
        self.evt_mgr.subscribe(pygame.KEYDOWN, self.on_keydown)

    def run(self):
        """Kicks off the game loop"""
        self.running = True

        while self.running:
            self.clock.tick(60) # Limit to 60FPS
            self.evt_mgr.dispatch(pygame.event.get())

            self.game.update(self.clock.get_time())

            self.game.SCR_SURF.fill((0, 0, 0))
            self.game.draw()
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def shutdown(self, evt):
        """Performs any cleanup operations and stop the game loop."""
        self.running = False

    def on_keydown(self, evt):
        """Handle basic keydown events."""
        if evt.key == pygame.K_ESCAPE:
            self.shutdown(evt)


if __name__ == '__main__':
    app = App({
        'SCR_SIZE'  : (640, 480),
        'SCR_CAP'   : 'Pygame and Python 3 Test',
        'SCR_FLAGS' : pygame.HWSURFACE | pygame.DOUBLEBUF
    })
    app.run()
