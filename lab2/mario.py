import pygame
from pygame.math import Vector2


class Mario(object):
    """Bundles together some basic character functionality."""

    def __init__(self, name, surf, pos=Vector2()):
        if not surf:
            raise ValueError('no surface')

        self.name = name
        self.surf = surf
        self.pos = pos
        self.dir = Vector2()
        self.rect = pygame.Rect(self.pos, self.surf.get_size())

        #self.enemies = dict()  # {str: Rect}
        self.enemies = list()
        self.on_collision = lambda x: None

    def check_collisions(self):
        """Check for any collisions and call the collision handler."""
        i = self.rect.collidelist(self.enemies)
        if i != -1:
            self.on_collision(self.enemies[i])

    def update(self, dt):
        """Perform any logic updates here."""
        self.pos += self.dir * dt

        # Update the rect
        self.rect.left = self.pos.x
        self.rect.top = self.pos.y

        self.check_collisions()

    def draw(self, dest_surf):
        """Blit Mario to the destination surface"""
        dest_surf.blit(self.surf, self.pos_to_tuple())

    def set_dir(self, new_dir):
        # Normalize incoming dir if needed
        if new_dir.length() > 0 and not new_dir.is_normalized():
            self.dir = new_dir.normalize()
        else:
            self.dir = new_dir

    def pos_to_tuple(self):
        """Return position as a (x,y) tuple."""
        return self.pos.x, self.pos.y
