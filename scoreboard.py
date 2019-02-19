import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_settings, screen, stats, sprite_sheet, high_score_file):
        """Initialize score keeping attributes."""
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.high_score_file = high_score_file
        self.high_scores = []
        self.score_image = None
        self.score_rect = None
        self.high_score_image = None
        self.high_score_rect = None
        self.level_image = None
        self.level_rect = None
        self.ships = None

        # Font settings for scoring information.
        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.load_high_scores()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw scores and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Draw ships
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(ai_settings=self.ai_settings, screen=self.screen, sprite_sheet=self.sprite_sheet)
            ship.rect.x = 10 + ship_number * ship.rect.width + ship_number * 5
            ship.rect.y = 10
            self.ships.add(ship)

    def load_high_scores(self):
        """Load the high scores from disk."""
        for line in self.high_score_file:
            self.high_scores.append(int(line))
        self.high_score_file.close()
        if len(self.high_scores) > 0:
            self.stats.high_score = self.high_scores[0]
            self.prep_high_score()

    def save_high_scores(self):
        """Save the high scores before closing and in between games."""
        self.high_scores.append(self.stats.score)
        self.high_scores.sort(reverse=True)
        if len(self.high_scores) > 0:
            self.stats.high_score = self.high_scores[0]
            self.prep_high_score()
        max_score = len(self.high_scores)
        self.high_score_file = open("high_score_file.txt", "w")
        if max_score > 10:
            max_score = 10
        for i in range(0, max_score):
            if self.high_scores[i] > 0:
                self.high_score_file.write(str(int(self.high_scores[i])) + "\n")
        self.high_score_file.close()

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
