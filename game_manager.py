import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


class GameManager:
    """Manages all game objects and interactions between them."""
    # Initialize Game Manager with all game objects.
    def __init__(self, ai_settings, screen, sprite_sheet, play_button, stats, sb, ship, bullets, aliens, ufos):
        self.ai_settings = ai_settings
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.play_button = play_button
        self.stats = stats
        self.sb = sb
        self.ship = ship
        self.bullets = bullets
        self.aliens = aliens
        self.ufos = ufos
        self.animate_aliens = 0

    def check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_key_down_events(event)
            elif event.type == pygame.KEYUP:
                self.check_key_up_events(event=event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(mouse_x=mouse_x, mouse_y=mouse_y)

    def check_key_down_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def check_key_up_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def check_play_button(self, mouse_x, mouse_y):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.ai_settings.initialize_dynamic_settings()

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
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self.create_fleet()
            self.ship.center_ship()

    def fire_bullet(self):
        """Fire a bullet if limit not reached yet."""
        bullet_offset = 0
        # Create a new bullet and add it to the bullets group.
        if len(self.bullets) < self.ai_settings.bullets_allowed:
            for _ in range(3):
                new_bullet = Bullet(ai_settings=self.ai_settings, screen=self.screen,
                                    ship=self.ship, bullet_y=bullet_offset)
                self.bullets.add(new_bullet)
                bullet_offset += 55

    def update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()

    def check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        ufo_collisions = pygame.sprite.groupcollide(self.bullets, self.ufos, True, True)
        if collisions or ufo_collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    explosion_image = self.sprite_sheet.get_sprite(200, 102, 54, 50)
                    self.screen.blit(explosion_image, alien.rect)
                    self.stats.score += (alien.points * self.ai_settings.score_scale)

                self.sb.prep_score()
            for ufos in ufo_collisions.values():
                self.stats.score += self.stats.ufo_points
                self.sb.prep_score()
            self.check_high_score()

        if len(self.aliens) == 0 and len(self.ufos) == 0:
            # If the entire fleet is destroyed, start a new level.
            self.bullets.empty()
            self.ai_settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

            self.create_fleet()

    def ship_hit(self):
        """Respond to ship being hit by alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Update scoreboard.
            self.sb.prep_ships()

            # Empty the list of aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self.create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def update_screen(self):
        """Update images on the screen and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.ai_settings.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Redraw all bullets behind ship and aliens.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def update_aliens(self):
        """Check if the fleet is at an edge, and then update the positions of all aliens in the fleet."""
        self.check_fleet_edges()
        if self.animate_aliens == self.ai_settings.animate_aliens:
            for alien in self.aliens:
                alien.switch_image()
            self.animate_aliens = 0
        self.animate_aliens += 1
        self.aliens.update()
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self.check_aliens_bottom()

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.sb.prep_high_score()


    '''Might remove everything under into fleet class'''
    def create_fleet(self):
        """Create a full fleet of aliens."""
        row = 4

        # Create the fleet of aliens.
        for row_number in range(self.ai_settings.number_rows):
            for alien_number in range(self.ai_settings.number_aliens_x):
                self.create_alien(alien_number, row_number, row)
            row -= 1

    def get_number_aliens_x(self, alien_width):
        """Determine the number of aliens that fit in a row."""
        available_space_x = self.ai_settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

    def get_number_rows(self, ship_height, alien_height):
        """Determine the number of rows of aliens that fit on the screen."""
        available_space_y = (self.ai_settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (2 * alien_height))
        return number_rows

    def create_alien(self, alien_number, row_number, row):
        """Create an alien and place it in the row."""
        alien = Alien(ai_settings=self.ai_settings, screen=self.screen, sprite_sheet=self.sprite_sheet, row=row)
        # alien_width = alien.rect.width
        alien_width = 50
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self.ship_hit()
                break

    def check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.ai_settings.fleet_drop_speed
        self.ai_settings.fleet_direction *= -1
