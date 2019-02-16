from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen, sprite_sheet, row=0):
        """Initialize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute.
        if row == 4:
            self.image = sprite_sheet.get_sprite(162, 0, 31, 31)
            self.image_b = sprite_sheet.get_sprite(194, 0, 31, 31)
            self.points = 40
        elif row == 3:
            self.image = sprite_sheet.get_sprite(0, 84, 43, 31)
            self.image_b = sprite_sheet.get_sprite(44, 84, 43, 31)
            self.points = 20
        elif row == 2:
            self.image = sprite_sheet.get_sprite(44, 84, 43, 31)
            self.image_b = sprite_sheet.get_sprite(0, 84, 43, 31)
            self.points = 20
        elif row == 1:
            self.image = sprite_sheet.get_sprite(88, 84, 46, 31)
            self.image_b = sprite_sheet.get_sprite(136, 84, 46, 31)
            self.points = 10
        else:
            self.image = sprite_sheet.get_sprite(136, 84, 46, 31)
            self.image_b = sprite_sheet.get_sprite(88, 84, 46, 31)
            self.points = 10

        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def switch_image(self):
        """Switch the image for animations."""
        self.image, self.image_b = self.image_b, self.image
