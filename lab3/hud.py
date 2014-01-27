import pygame


class HUD(object):
    """Draws score output to a single surface."""

    def __init__(self, font_size, width, line_space=0.5):
        self.bg_colour = (255, 0, 255)
        self.cars = list()
        self.pos = pygame.Rect(0, 0, width, font_size)
        self.line_space = line_space

        # Load the default font.
        self.font = pygame.font.Font(None, int(font_size))

        # Create a surface twice the font height.
        self.hud_surf = pygame.Surface((width, (font_size * 2) + line_space))
        self.hud_surf.set_colorkey(self.bg_colour)

    def update_hud_surf(self):
        """Redraw the HUD. Called if scores change."""
        # Clear the surface
        self.hud_surf.fill(self.bg_colour)

        # Redraw the text
        for i, car in enumerate(self.cars):
            text = '{} {}'.format(car.name.split('_')[0], car.score)
            text_surf = self.font.render(text, False, (0, 0, 0), self.bg_colour)
            y = (i * self.font.get_height() + self.line_space)
            self.hud_surf.blit(text_surf, (0, y))

    def register_cars(self, cars):
        """Register cars and add score change event handler"""
        self.cars.extend(cars)
        for car in cars:
            car.on_score_change = self.update_hud_surf

        # Redraw HUD.
        self.update_hud_surf()

    def draw(self, target):
        """Blit the HUD surface to target surface."""
        target.blit(self.hud_surf, self.pos)