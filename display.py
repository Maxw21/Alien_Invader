import pygame
import random

from alien import Alien
from barrier import Barrier


class Display:
    """A class to manage all screen displaying."""
    def __init__(self, ai_settings, screen, sprite_sheet, play_button, score_button, stats, sb,
                 ship, bullets, fleet, barriers, explosions, event_handler):
        """Initialize all game objects the screen displays."""
        self.ai_settings = ai_settings
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.play_button = play_button
        self.score_button = score_button
        self.stats = stats
        self.sb = sb
        self.ship = ship
        self.bullets = bullets
        self.fleet = fleet
        self.barriers = barriers
        self.explosions = explosions
        self.event_handler = event_handler

        # Logic check attributes
        self.ufo_points_img = None
        self.ufo_points_img_rect = None
        self.create_title = False
        self.ufo_destroy = False
        self.animate_aliens = 0
        self.ufo_points_animate = 0
        self.start_aliens = []

    def update_screen(self):
        """Update images on the screen and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        if self.stats.game_active:
            self.screen.fill(self.ai_settings.bg_color)
            self.ship.blitme()
            self.fleet.aliens.draw(self.screen)
            self.fleet.ufos.draw(self.screen)
            self.explosions.draw(self.screen)

            # Animate explosions
            if len(self.explosions) > 0:
                explosion_list = self.explosions.sprites()
                for explosion in explosion_list:
                    explosion.update_timer()
                    if explosion.animation_timer == 25:
                        explosion.animation_switch()

            # Display UFO points
            if self.ufo_destroy:
                self.screen.blit(self.ufo_points_img, self.ufo_points_img_rect)
                self.ufo_points_animate += 1
                if self.ufo_points_animate >= 100:
                    self.ufo_destroy = False
                    self.ufo_points_animate = 0

            # Draw the barriers
            for barrier in self.barriers:
                barrier.draw_barrier()

            # Redraw all bullets behind ship and aliens.
            for bullet in self.bullets.bullets.sprites():
                bullet.draw_bullet()
            for bullet in self.bullets.alien_bullets.sprites():
                bullet.blitme()
            # Draw the score information.
            self.sb.show_score()

            # Create ufos at random intervals
            if self.fleet.spawn_ufo >= random.randint(4000, 11000):
                self.fleet.create_ufos()
                self.fleet.spawn_ufo = 0
            else:
                self.fleet.spawn_ufo += 1
        else:
            if self.event_handler.displaying_scores:
                self.draw_high_scores()
            else:
                self.draw_start_screen()
                if self.create_title:
                    for i in range(len(self.start_aliens)):
                        self.start_aliens[i].blitme()
                        if self.animate_aliens == self.ai_settings.animate_aliens:
                            for j in range(len(self.start_aliens)):
                                self.start_aliens[j].switch_image()
                            self.animate_aliens = 0
                        self.animate_aliens += 1
                else:
                    self.create_title_aliens()
            self.draw_title()
            # Draw the play button and high score button if the game is inactive.
            self.play_button.draw_button()
            self.score_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def draw_high_scores(self):
        """Draw the high scores on the high score page"""
        self.sb.high_scores.sort(reverse=True)
        self.screen.fill((180, 180, 180))
        self.score_button.prep_msg("Return")
        font_color_black = (0, 0, 0)
        font_color_blue = (0, 0, 255)
        font = pygame.font.SysFont(None, 50)
        title_img = font.render("High Scores", True, font_color_blue)
        title_img_rect = pygame.Rect(0, 0, 200, 50)
        title_img_rect.center = self.screen.get_rect().center
        title_img_rect.y -= 180
        self.screen.blit(title_img, title_img_rect)
        offset = -120
        max_score = len(self.sb.high_scores)
        if max_score > 10:
            max_score = 10
        for i in range(0, max_score):
            score_image = font.render(str(self.sb.high_scores[i]), True, font_color_black)
            score_image_rect = pygame.Rect(0, 0, 200, 50)
            score_image_rect.center = self.screen.get_rect().center
            score_image_rect.y += offset
            score_image_rect.x += 20
            self.screen.blit(score_image, score_image_rect)
            offset += 40

    def draw_title(self):
        """Draw the space invader title"""
        font_red = (255, 0, 0)
        font_green = (0, 255, 0)
        font = pygame.font.SysFont(None, 100)
        logo_img_top = font.render("Space", True, font_red)
        logo_top_rect = pygame.Rect(0, 0, 200, 50)
        logo_top_rect.center = self.screen.get_rect().center
        logo_top_rect.y -= 360
        logo_top_rect.x -= 10
        logo_img_bot = font.render("Invaders", True, font_green)
        logo_bot_rect = pygame.Rect(0, 0, 200, 50)
        logo_bot_rect.center = self.screen.get_rect().center
        logo_bot_rect.y -= 260
        logo_bot_rect.x -= 50
        self.screen.blit(logo_img_top, logo_top_rect)
        self.screen.blit(logo_img_bot, logo_bot_rect)

    def draw_start_screen(self):
        """Draws the start screen."""
        self.screen.fill(self.ai_settings.bg_color)
        self.score_button.prep_msg("High Scores")
        font_color = (230, 230, 230)
        font = pygame.font.SysFont(None, 50)
        alien_a_points = font.render("=      10", True, font_color)
        alien_a_points_rect = pygame.Rect(0, 0, 200, 50)
        alien_a_points_rect.center = self.screen.get_rect().center
        alien_a_points_rect.y -= 145
        alien_a_points_rect.x += 80
        self.screen.blit(alien_a_points, alien_a_points_rect)
        alien_b_points = font.render("=      20", True, font_color)
        alien_b_points_rect = pygame.Rect(0, 0, 200, 50)
        alien_b_points_rect.center = self.screen.get_rect().center
        alien_b_points_rect.y -= 75
        alien_b_points_rect.x += 80
        self.screen.blit(alien_b_points, alien_b_points_rect)
        alien_c_points = font.render("=      40", True, font_color)
        alien_c_points_rect = pygame.Rect(0, 0, 200, 50)
        alien_c_points_rect.center = self.screen.get_rect().center
        alien_c_points_rect.y -= 5
        alien_c_points_rect.x += 80
        self.screen.blit(alien_c_points, alien_c_points_rect)
        ufo = self.sprite_sheet.get_sprite(120, 0, 41, 18)
        ufo_rect = ufo.get_rect()
        ufo_rect.center = self.screen.get_rect().center
        ufo_rect.y += 60
        ufo_rect.x -= 100
        ufo_points = font.render("=     ???", True, font_color)
        ufo_points_rect = pygame.Rect(0, 0, 200, 50)
        ufo_points_rect.center = self.screen.get_rect().center
        ufo_points_rect.y += 65
        ufo_points_rect.x += 80
        self.screen.blit(ufo, ufo_rect)
        self.screen.blit(ufo_points, ufo_points_rect)

    def create_title_aliens(self):
        """Create the aliens that are on the title screen."""
        for i in range(0, 5, 2):
            alien = Alien(ai_settings=self.ai_settings, screen=self.screen, sprite_sheet=self.sprite_sheet, row=i)
            alien.rect.center = self.screen.get_rect().center
            alien.rect.y -= 150 - (i * 35)
            alien.rect.x -= 100
            self.start_aliens.append(alien)
        self.create_title = True

    def create_barriers(self):
        self.barriers = []
        for i in range(0, 4):
            barrier = Barrier(screen=self.screen, sprite_sheet=self.sprite_sheet, column=i)
            barrier.create_barrier()
            barrier.draw_barrier()
            self.barriers.append(barrier)

    def draw_ufo_points(self, points, ufo):
        """Draw the points on the screen when a ufo is destroyed."""
        points_str = "+ {:,}".format(points)
        text_color = (230, 230, 230)
        font = pygame.font.SysFont(None, 30)
        self.ufo_points_img = font.render(points_str, True, text_color, self.ai_settings.bg_color)
        self.ufo_points_img_rect = self.ufo_points_img.get_rect()
        self.ufo_points_img_rect.x = ufo.rect.x
        self.ufo_points_img_rect.y = ufo.rect.y
        self.screen.blit(self.ufo_points_img, self.ufo_points_img_rect)
        self.ufo_destroy = True
