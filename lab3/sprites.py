import pygame


class Car(pygame.sprite.Sprite):
    """Car sprite."""

    def __init__(self, name, img_surf):
        # Parent class constructor must be called.
        super(Car, self).__init__()

        self.name = name
        self.image = img_surf
        self.rect = self.image.get_rect()
        self.vel = pygame.math.Vector2(0, 0)

        self.score = 0

    def update(self, dt):
        """Update the cars position."""
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt

    def __str__(self):
        return self.name


class FinishLine(pygame.sprite.Sprite):
    """Basic white line sprite."""

    def __init__(self, name, screen_surf, width, percent_towards_right):
        # Parent class constructor must be called.
        super(FinishLine, self).__init__()
        self.name = name

        scr_size = screen_surf.get_size()

        # Create a surface and fill it white.
        self.image = pygame.Surface((scr_size[0] * width, scr_size[1]))
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = scr_size[0] * percent_towards_right
