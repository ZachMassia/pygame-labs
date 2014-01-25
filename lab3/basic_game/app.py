import sys
import pygame
from .event import EventManager


class App(object):
    """Responsible for setting up the window and handling events."""

    def __init__(self, cfg, game):
        self.game = game
        self.running = False

        pygame.init()
        pygame.display.set_mode(cfg['SCR_SIZE'], cfg['SCR_FLAGS'])
        pygame.display.set_caption(cfg['SCR_CAP'])

        self.evt_mgr = self.init_event_mgr()
        self.register_events()

        if cfg['LOGGING'] == 'True':
            self.init_logger(cfg)
            self.evt_mgr.logging_enabled = True
            self.game.logging_enabled = True

        self.clock = pygame.time.Clock()

        self.game.scr_surf = pygame.display.get_surface()
        self.game.build()

    def run(self):
        """Kicks off the game loop."""
        self.running = True

        while self.running:
            self.clock.tick(60)  # Limit to 60FPS

            self.evt_mgr.dispatch(pygame.event.get())

            self.game.update(self.clock.get_time())

            self.game.scr_surf.fill((0, 0, 0))
            self.game.draw()
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def on_keydown(self, evt):
        """Handle basic keydown events."""
        if evt.key == pygame.K_ESCAPE:
            self.shutdown(evt)

    def init_event_mgr(self):
        """Return the event manager and inject it into the game object."""
        evt_mgr = EventManager()
        self.game.evt_mgr = evt_mgr
        return evt_mgr

    def init_logger(self, cfg):
        """Configure the logging module."""
        import logging
        logging.basicConfig(filename=cfg['LOG_FILE'],
                            level=cfg['LOG_LEVEL'],
                            format='%(levelname)s:\t%(message)s')

    def register_events(self):
        """Register a few base event handlers."""
        self.evt_mgr.subscribe(pygame.QUIT, self.shutdown)
        self.evt_mgr.subscribe(pygame.KEYDOWN, self.on_keydown)

    def shutdown(self, evt):
        """Performs any cleanup operations and stop the game loop."""
        self.running = False

        if self.game.logging_enabled:
            import logging
            logging.info('{}\n'.format('-' * 75))
