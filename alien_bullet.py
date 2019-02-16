import pygame
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    """A class to manage alien bullets."""
    def __init__(self, screen, sprite_sheet, x, y, version):
        """Create a bullet at the aliens current position"""
        super(AlienBullet, self).__init__()
        self.screen = screen
        if version == 0:
            self.image = sprite_sheet.get_sprite(0, 0, 15, 19)
            self.image_b = sprite_sheet.get_sprite(16, 0, 15, 19)
            self.image_c = sprite_sheet.get_sprite(32, 0, 15, 19)
            self.image_d = sprite_sheet.get_sprite(48, 0, 15, 19)
            self.rect = self.image.get_rect()
            self.rect.x = x + 25
            self.rect.y = y + 50
            self.y = float(self.rect.y)
            self.speed = 1.5
        else:
            self.image = sprite_sheet.get_sprite(64, 0, 14, 23)
            self.image_b = sprite_sheet.get_sprite(78, 0, 14, 23)
            self.image_c = sprite_sheet.get_sprite(92, 0, 14, 23)
            self.image_d = sprite_sheet.get_sprite(106, 0, 14, 23)
            self.rect = self.image.get_rect()
            self.rect.x = x + 25
            self.rect.y = y + 50
            self.y = float(self.rect.y)
            self.speed = 1

    def update(self):
        """Move the bullet down the screen."""
        self.y += self.speed
        self.rect.y = self.y
        if pygame.time.get_ticks() % 20 == 0:
            self.switch_image()

    def blitme(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)

    def switch_image(self):
        """Switch the image for animations."""
        self.image, self.image_b, self.image_c, self.image_d = self.image_b, self.image_c, self.image_d, self.image
