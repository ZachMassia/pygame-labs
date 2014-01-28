import pygame


class HUD(object):
    """Draws score output to a single surface."""

    def __init__(self, target, font_size, width, line_space=0.5,
                 flash_size=(500, 100)):
        self.target = target
        self.bg_colour = (255, 0, 255)
        self.cars = list()
        self.pos = pygame.Rect(0, 0, width, font_size)
        self.line_space = line_space

        # Load the default font.
        self.font = pygame.font.Font(None, int(font_size))
        self.flash_font = pygame.font.Font(None, int(font_size) * 2)

        # Create a surface twice the font height.
        self.hud_surf = pygame.Surface((width, (font_size * 2) + line_space))
        self.hud_surf.set_colorkey(self.bg_colour)

        # TODO: Move flash to own class?
        self.flash_start_time = 0
        self.flash_duration = 0
        self.flash_pos = (0, 0)
        self.flash_surf = pygame.Surface(flash_size)

    def flash(self, msg, duration):
        """Flash a message center screen for a set amount of time."""
        self.flash_duration = duration
        self.flash_start_time = pygame.time.get_ticks()

        # Render the new message to the surface.
        self.flash_surf = \
            self.flash_font.render(msg, False, (0, 0, 0), self.bg_colour)
        self.flash_surf.set_colorkey(self.bg_colour)

        # Recalculate position
        tx, ty = self.target.get_size()
        sx, sy = self.flash_surf.get_size()
        self.flash_pos = (
            (tx / 2) - (sx / 2),
            (ty / 2) - (sy / 2)
        )

    def update_hud_surf(self):
        """Redraw the HUD. Called if scores change."""
        # Clear the surface
        self.hud_surf.fill(self.bg_colour)

        # Redraw the text
        for i, car in enumerate(self.cars):
            text = '{} {}'.format(car.name.split('_')[0], car.score)
            text_surf = \
                self.font.render(text, False, (0, 0, 0), self.bg_colour)
            y = (i * self.font.get_height()) + self.line_space
            self.hud_surf.blit(text_surf, (0, y))

    def register_cars(self, cars):
        """Register cars and add score change event handler"""
        self.cars.extend(cars)
        for car in cars:
            car.on_score_change = self.update_hud_surf

        # Redraw HUD.
        self.update_hud_surf()

    def draw(self):
        """Blit the HUD surface to target surface."""
        self.target.blit(self.hud_surf, self.pos)

        now = pygame.time.get_ticks()
        if (now - self.flash_start_time) < self.flash_duration:
            self.target.blit(self.flash_surf, self.flash_pos)
