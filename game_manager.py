import sys
from time import sleep
import random

import pygame

from barrier import Barrier
from bullet import Bullet
from alien import Alien
from explosion import Explosion
from alien_bullet import AlienBullet
from ufo import Ufo


class GameManager:
    """Manages all game objects and interactions between them."""
    # Initialize Game Manager with all game objects.
    def __init__(self, ai_settings, screen, sprite_sheet, play_button, score_button,
                 stats, sb, ship, bullets, aliens, ufos, barriers, explosions,
                 alien_bullets, high_score_file):
        self.ai_settings = ai_settings
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.play_button = play_button
        self.score_button = score_button
        self.stats = stats
        self.sb = sb
        self.ship = ship
        self.bullets = bullets
        self.aliens = aliens
        self.ufos = ufos
        self.barriers = barriers
        self.explosions = explosions
        self.alien_bullets = alien_bullets
        self.high_score_file = high_score_file
        self.high_scores = []
        self.spawn_ufo = 0
        self.ufo_points_img = None
        self.ufo_points_img_rect = None
        self.ufo_points_animate = 0
        self.ufo_destroy = False
        self.animate_aliens = 0
        self.alien_bullet_time = 0
        self.displaying_scores = False
        self.alien_bullet_sound = pygame.mixer.Sound('sounds/alien_bullet_sound.wav')
        self.alien_destroy_sound = pygame.mixer.Sound('sounds/alien_destroy_sound.wav')
        self.ship_bullet_sound = pygame.mixer.Sound('sounds/ship_bullet_sound.wav')
        self.ship_destroy_sound = pygame.mixer.Sound('sounds/ship_destroy_sound.wav')
        self.alien_destroy_sound = pygame.mixer.Sound('sounds/alien_destroy_sound.wav')
        self.ufo_sound = pygame.mixer.Sound('sounds/ufo_sound.wav')
        for line in high_score_file:
            self.high_scores.append(int(line))
        self.high_score_file.close()
        if len(self.high_scores) > 0:
            self.stats.high_score = self.high_scores[0]
            self.sb.prep_high_score()

    def check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_high_scores()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_key_down_events(event)
            elif event.type == pygame.KEYUP:
                self.check_key_up_events(event=event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(mouse_x=mouse_x, mouse_y=mouse_y)
                self.check_score_button(mouse_x=mouse_x, mouse_y=mouse_y)

    def check_key_down_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_q:
            if self.stats.game_active:
                self.save_high_scores()
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
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self.create_fleet()
            self.create_barriers()
            self.ship.center_ship()

            # Play the background Music
            pygame.mixer.music.load('sounds/background_music.wav')
            pygame.mixer.music.play(-1)

    def check_score_button(self, mouse_x, mouse_y):
        """Display high scores."""
        button_clicked = self.score_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.stats.game_active:
            # Clear the screen, display high scores
            self.displaying_scores = not self.displaying_scores

    def fire_bullet(self):
        """Fire a bullet if limit not reached yet."""
        bullet_offset = 0
        # Create a new bullet and add it to the bullets group.
        if len(self.bullets) < self.ai_settings.bullets_allowed:
            self.ship_bullet_sound.play()
            for _ in range(3):
                new_bullet = Bullet(ai_settings=self.ai_settings, screen=self.screen,
                                    ship=self.ship, bullet_y=bullet_offset)
                self.bullets.add(new_bullet)
                bullet_offset += 55

    def update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        self.alien_bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.screen.get_rect().bottom:
                self.alien_bullets.remove(bullet)

        self.check_bullet_alien_collisions()
        self.check_bullet_ship_collisions()
        self.check_bullet_barrier_collisions()

    def check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        ufo_collisions = pygame.sprite.groupcollide(self.bullets, self.ufos, True, True)
        if collisions or ufo_collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    self.alien_destroy_sound.play()
                    explosion = Explosion(screen=self.screen, sprite_sheet=self.sprite_sheet, rect=alien.rect)
                    explosion.blitme()
                    self.explosions.add(explosion)
                    self.stats.score += (alien.points * self.ai_settings.score_scale)
                self.sb.prep_score()
            for ufos in ufo_collisions.values():
                for ufo in ufos:
                    self.ufo_sound.stop()
                    self.alien_destroy_sound.play()
                    ufo_points = random.randrange(40, 200, 10)
                    points_str = "+ {:,}".format(ufo_points)
                    text_color = (230, 230, 230)
                    font = pygame.font.SysFont(None, 30)
                    self.ufo_points_img = font.render(points_str, True, text_color, self.ai_settings.bg_color)
                    self.ufo_points_img_rect = self.ufo_points_img.get_rect()
                    self.ufo_points_img_rect.x = ufo.rect.x
                    self.ufo_points_img_rect.y = ufo.rect.y
                    self.screen.blit(self.ufo_points_img, self.ufo_points_img_rect)
                    self.ufo_destroy = True
                self.stats.score += ufo_points
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
            self.create_barriers()

    def check_bullet_ship_collisions(self):
        """Respond to bullet-ship collisions."""
        collisions = pygame.sprite.spritecollide(self.ship, self.alien_bullets, True)
        if collisions:
            self.ship_hit()

    def check_bullet_barrier_collisions(self):
        """Respond to bullet-barrier collisions."""
        for barrier in self.barriers:
            pygame.sprite.groupcollide(self.bullets, barrier.barrier, True, True)
            pygame.sprite.groupcollide(self.alien_bullets, barrier.barrier, True, True)

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

            # Play ship destroy sound
            self.ship_destroy_sound.play()

            # Create a new fleet and center the ship.
            self.create_fleet()
            self.ship.center_ship()

            # Pause
            #pygame.time.wait(500)
            for i in range(0, 10):
                self.ship.destroy_animation()
                self.update_screen()
                sleep(0.2)
            #sleep(0.5)

        else:
            pygame.mixer.music.stop()
            self.ufo_sound.stop()
            self.save_high_scores()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def draw_start_screen(self):
        """Draws the start screen."""
        self.screen.fill(self.ai_settings.bg_color)
        self.score_button.prep_msg("High Scores")
        font_color = (230, 230, 230)
        font = pygame.font.SysFont(None, 50)
        alien_a = self.sprite_sheet.get_sprite(162, 0, 31, 31)
        alien_a_rect = alien_a.get_rect()
        alien_a_rect.center = self.screen.get_rect().center
        alien_a_rect.y -= 150
        alien_a_rect.x -= 100
        alien_a_points = font.render("=      40", True, font_color)
        alien_a_points_rect = pygame.Rect(0, 0, 200, 50)
        alien_a_points_rect.center = self.screen.get_rect().center
        alien_a_points_rect.y -= 145
        alien_a_points_rect.x += 80
        alien_b = self.sprite_sheet.get_sprite(0, 84, 43, 31)
        alien_b_rect = alien_b.get_rect()
        alien_b_rect.center = self.screen.get_rect().center
        alien_b_rect.y -= 80
        alien_b_rect.x -= 100
        alien_b_points = font.render("=      20", True, font_color)
        alien_b_points_rect = pygame.Rect(0, 0, 200, 50)
        alien_b_points_rect.center = self.screen.get_rect().center
        alien_b_points_rect.y -= 75
        alien_b_points_rect.x += 80
        alien_c = self.sprite_sheet.get_sprite(88, 84, 46, 31)
        alien_c_rect = alien_c.get_rect()
        alien_c_rect.center = self.screen.get_rect().center
        alien_c_rect.y -= 10
        alien_c_rect.x -= 100
        alien_c_points = font.render("=      10", True, font_color)
        alien_c_points_rect = pygame.Rect(0, 0, 200, 50)
        alien_c_points_rect.center = self.screen.get_rect().center
        alien_c_points_rect.y -= 5
        alien_c_points_rect.x += 80
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
        self.screen.blit(alien_a, alien_a_rect)
        self.screen.blit(alien_a_points, alien_a_points_rect)
        self.screen.blit(alien_b, alien_b_rect)
        self.screen.blit(alien_b_points, alien_b_points_rect)
        self.screen.blit(alien_c, alien_c_rect)
        self.screen.blit(alien_c_points, alien_c_points_rect)
        self.screen.blit(ufo, ufo_rect)
        self.screen.blit(ufo_points, ufo_points_rect)

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

    def draw_high_scores(self):
        """Draw the high scores on the high score page"""
        self.high_scores.sort(reverse=True)
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
        max_score = len(self.high_scores)
        if max_score > 10:
            max_score = 10
        for i in range(0, max_score):
            score_image = font.render(str(self.high_scores[i]), True, font_color_black)
            score_image_rect = pygame.Rect(0, 0, 200, 50)
            score_image_rect.center = self.screen.get_rect().center
            score_image_rect.y += offset
            score_image_rect.x += 20
            self.screen.blit(score_image, score_image_rect)
            offset += 40

    def save_high_scores(self):
        """Save the high scores before closing and in between games."""
        self.high_scores.append(self.stats.score)
        self.high_scores.sort(reverse=True)
        if len(self.high_scores) > 0:
            self.stats.high_score = self.high_scores[0]
            self.sb.prep_high_score()
        max_score = len(self.high_scores)
        self.high_score_file = open("high_score_file.txt", "w")
        if max_score > 10:
            max_score = 10
        for i in range(0, max_score):
            self.high_score_file.write(str(self.high_scores[i]) + "\n")
        self.high_score_file.close()

    def update_screen(self):
        """Update images on the screen and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        if self.stats.game_active:
            self.screen.fill(self.ai_settings.bg_color)
            self.ship.blitme()
            self.aliens.draw(self.screen)
            self.ufos.draw(self.screen)
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
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            for bullet in self.alien_bullets.sprites():
                bullet.blitme()
            # Draw the score information.
            self.sb.show_score()

            # Create ufos at random intervals
            if self.spawn_ufo >= random.randint(4000, 11000):
                self.create_ufos()
                self.spawn_ufo = 0
            else:
                self.spawn_ufo += 1
        else:
            if self.displaying_scores:
                self.draw_high_scores()
            else:
                self.draw_start_screen()
            self.draw_title()
            # Draw the play button and high score button if the game is inactive.
            self.play_button.draw_button()
            self.score_button.draw_button()

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

        # Shoot bullets from aliens
        #print("check time: " + str(self.alien_bullet_time))
        if self.alien_bullet_time >= random.randint(500, 1000):
            # print('call shoot method')
            alien_list = self.aliens.sprites()
            alien_firing = len(alien_list) - 11
            alien_firing
            if alien_firing < 0:
                alien_firing = 0
            if len(alien_list) > 0:
                self.alien_shoot(alien_list[random.randint(alien_firing, len(alien_list) - 1)])
            self.alien_bullet_time = 0
        self.alien_bullet_time += 1
        # Look for aliens hitting the bottom of the screen.
        self.check_aliens_bottom()

    def alien_shoot(self, alien):
        """Create a bullet from an alien."""
        self.alien_bullet_sound.play()
        new_bullet = AlienBullet(screen=self.screen, sprite_sheet=self.sprite_sheet, x=alien.rect.x,
                                 y=alien.rect.y, version=random.randint(0, 1))
        self.alien_bullets.add(new_bullet)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.sb.prep_high_score()

    def create_barriers(self):
        self.barriers = []
        for i in range(0, 4):
            barrier = Barrier(screen=self.screen, sprite_sheet=self.sprite_sheet, column=i)
            barrier.create_barrier()
            barrier.draw_barrier()
            self.barriers.append(barrier)


    '''Might remove everything under into fleet class'''
    def create_fleet(self):
        """Create a full fleet of aliens."""
        row = 4
        # Create the fleet of aliens.
        for row_number in range(self.ai_settings.number_rows):
            for alien_number in range(self.ai_settings.number_aliens_x):
                self.create_alien(alien_number, row_number, row)
            row -= 1

    def create_alien(self, alien_number, row_number, row):
        """Create an alien and place it in the row."""
        alien = Alien(ai_settings=self.ai_settings, screen=self.screen, sprite_sheet=self.sprite_sheet, row=row)
        # alien_width = alien.rect.width
        alien_width = 50
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = 100 + alien.rect.height + 2 * alien.rect.height * row_number
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

    def create_ufos(self):
        """Create ufos at a random interval."""
        if len(self.ufos) < 1:
            self.ufo_sound.play(-1)
            ufo = Ufo(ai_settings=self.ai_settings, screen=self.screen, sprite_sheet=self.sprite_sheet)
            ufo.rect.x = 50
            ufo.rect.y = 60
            self.ufos.add(ufo)

    def update_ufos(self):
        """Check if ufo is at the edge, de-spawn ufo if it is."""
        self.check_ufo_edges()
        self.ufos.update()

    def check_ufo_edges(self):
        """Check if ufo reached the edge of the screen."""
        for ufo in self.ufos.sprites():
            if ufo.check_edges():
                self.ufo_sound.stop()
                self.spawn_ufo = 0
