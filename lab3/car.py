import pygame


class Car(pygame.sprite.Sprite):
    """TODO: Add class desc."""

    def __init__(self, img_surf):
        # Parent class constructor must be called.
        super(Car, self).__init__()

        self.image = img_surf
        self.rect = self.image.get_rect()
        self.vel = pygame.math.Vector2(0, 0)

    def update(self, dt):
        """TODO: Write docstring."""
        # Update position.
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt