import sys
import pygame


class EventHandler:
    """A class to handle all events from user input."""
    def __init__(self, ai_settings, play_button, score_button, stats, sb, ship, bullets, fleet, sounds):
        """Initialize instance attributes."""
        self.ai_settings = ai_settings
        self.play_button = play_button
        self.score_button = score_button
        self.stats = stats
        self.sb = sb
        self.ship = ship
        self.bullets = bullets
        self.fleet = fleet
        self.sounds = sounds
        self.displaying_scores = False

    def check_events(self, display):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sb.save_high_scores()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_key_down_events(event)
            elif event.type == pygame.KEYUP:
                self.check_key_up_events(event=event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(mouse_x=mouse_x, mouse_y=mouse_y, display=display)
                self.check_score_button(mouse_x=mouse_x, mouse_y=mouse_y)

    def check_key_down_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.bullets.fire_bullet()
        elif event.key == pygame.K_q:
            if self.stats.game_active:
                self.sb.save_high_scores()
            sys.exit()

    def check_key_up_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def check_play_button(self, mouse_x, mouse_y, display):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.ai_settings.initialize_dynamic_settings()

            # Turn off high score menu
            self.displaying_scores = False

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Reset the scoreboard images.
            self.sb.prep_score()
            self.sb.prep_high_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Empty the list of aliens and bullets.
            self.fleet.aliens.empty()
            self.bullets.bullets.empty()

            # Create a new fleet and center the ship.
            self.fleet.create_fleet()
            display.create_barriers()
            self.ship.center_ship()

            # Play the background Music
            # pygame.mixer.music.load('sounds/background_music.wav')
            # pygame.mixer.music.play(-1)
            self.sounds.background_music.play(-1)

    def check_score_button(self, mouse_x, mouse_y):
        """Display high scores."""
        button_clicked = self.score_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.stats.game_active:
            # Clear the screen, display high scores
            self.displaying_scores = not self.displaying_scores
