import pygame


class SpriteSheet(object):
    """Load a sprite sheet for image implementation."""

    def __init__(self, file_name):
        self.spriteSheet = pygame.image.load(file_name).convert()

    # Parameters are based on the sprite sheet dimensions.
    def get_sprite(self, x, y, width, height):
        """Split the sprite sheet into individual sprites."""
        sprite = pygame.Surface([width, height])  # .convert()
        sprite.blit(self.spriteSheet, (0, 0), (x, y, width, height))
        return sprite
