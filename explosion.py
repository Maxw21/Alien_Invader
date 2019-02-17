from pygame.sprite import Sprite


class Explosion(Sprite):
    """A class to represent an explosion sprite."""

    def __init__(self, screen, sprite_sheet, rect):
        """Initialize the explosion at the alien location."""
        super(Explosion, self).__init__()
        self.screen = screen
        self.rect = rect
        self.animation_counter = 0
        self.animation_timer = 0
        self.image_animation = []
        self.image = sprite_sheet.get_sprite(0, 124, 54, 50)
        self.image_animation.append(sprite_sheet.get_sprite(55, 124, 54, 50))
        self.image_animation.append(sprite_sheet.get_sprite(110, 124, 54, 50))
        self.image_animation.append(sprite_sheet.get_sprite(165, 124, 54, 50))

    def blitme(self):
        """Draw the explosion to the screen."""
        self.screen.blit(self.image, self.rect)

    def animation_switch(self):
        """Switch the image to animate the sprite."""
        self.image = self.image_animation[self.animation_counter]
        self.animation_timer = 0
        self.animation_counter += 1
        if self.animation_counter > 2:
            self.kill()

    def update_timer(self):
        """Update timer to slow animation."""
        self.animation_timer += 1
