
class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 2000
        self.bullet_height = 15
        self.bullet_color = 255, 255, 255
        self.bullets_allowed = 3

        # Alien settings
        self.animate_aliens = 300
        self.number_aliens_x = 11
        self.number_rows = 5
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10

        # Ufo settings
        self.ufo_speed_factor = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1

        # Initailize dynamic settings
        self.fleet_direction =1
        self.ufo_points = 50
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = .25
        self.ufo_speed_factor = .25

        # fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # UFO Scoring
        self.ufo_points = 50
        self.score_scale = 1

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.ufo_speed_factor *= self.speedup_scale
        if self.score_scale != 1:
            self.score_scale *= 1.5
        else:
            self.score_scale = 1.5