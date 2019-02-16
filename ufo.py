from pygame.sprite import Sprite
import pygame


class Ufo(Sprite):
    """A class to represent a single ufo."""

    def __init__(self, ai_settings, screen, sprite_sheet):
        super(Ufo, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load alien image and set its rect attribute
        self.image = sprite_sheet.get_sprite(120, 0, 41, 18)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien right or left."""
        self.x += self.ai_settings.ufo_speed_factor
        self.rect.x = self.x

    def check_edges(self):
        """Kills ufo if it reaches the end of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right + 41:
            self.kill()
            return True
        return False




    def display_points(self, ufo_points):
        """Displays the points the ufo is worth."""
        points_str = "{:,}".format(ufo_points)
        text_color = (230, 230, 230)
        font = pygame.font.SysFont(None, 20)
        points_img = font.render(points_str, True, text_color, self.ai_settings.bg_color)
        points_img_rect = points_img.get_rect()
        points_img_rect.x = self.rect.x
        points_img_rect.y = self.rect.y
        self.screen.blit
