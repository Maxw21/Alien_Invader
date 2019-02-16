from pygame.sprite import Sprite


class BarrierPixel(Sprite):
    """A class to represent a pixel of a barrier."""
    def __init__(self, screen, sprite_sheet, x, y, column):
        """Initialize the barrier pixel and set its starting position"""
        super(BarrierPixel, self).__init__()
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.image = sprite_sheet.get_sprite(x, y, 5, 4)
        self.rect = self.image.get_rect()
        self.rect.x = x + 250 * column
        self.rect.y = y + 600

    def blitme(self):
        """Draw the barrier pixel at its current location."""
        self.screen.blit(self.image, self.rect)
