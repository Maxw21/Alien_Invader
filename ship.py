from time import sleep
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen, sprite_sheet, stats=None, sb=None, sounds=None):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.stats = stats
        self.sb = sb
        self.sounds = sounds

        # Load the ship image and get its rect.
        self.image = sprite_sheet.get_sprite(88, 58, 43, 25)
        self.death_image = []
        self.death_image.append(sprite_sheet.get_sprite(44, 32, 43, 25))
        self.death_image.append(sprite_sheet.get_sprite(44, 58, 43, 25))
        self.death_image.append(sprite_sheet.get_sprite(0, 32, 43, 25))
        self.death_image.append(sprite_sheet.get_sprite(88, 32, 43, 25))
        self.death_image.append(sprite_sheet.get_sprite(132, 32, 43, 25))
        self.death_image.append(sprite_sheet.get_sprite(0, 58, 43, 25))
        self.death_image.append(sprite_sheet.get_sprite(176, 58, 43, 25))
        self.death_image.append(sprite_sheet.get_sprite(176, 32, 43, 25))
        self.death_image.append(sprite_sheet.get_sprite(132, 58, 43, 25))
        self.death_image.append(self.image)
        self.death_anim_counter = 0
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on the movement flags."""
        # Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center

    def ship_hit(self, bullets, fleet, display):
        """Respond to ship being hit by alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Update scoreboard.
            self.sb.prep_ships()

            # Empty the list of aliens and bullets.
            fleet.aliens.empty()
            bullets.bullets.empty()

            # Play ship destroy sound
            self.sounds.ship_destroy_sound.play()

            # Create a new fleet and center the ship.
            fleet.create_fleet()
            self.center_ship()

            # Restart background music
            self.sounds.background_music.stop()
            self.sounds.background_music = self.sounds.background_track[0]
            self.sounds.background_music.play(-1)
            self.sounds.background_music_counter = 1

            # Display ship destroy animation
            for i in range(0, 10):
                self.destroy_animation()
                display.update_screen()
                sleep(0.2)

        else:
            self.sounds.background_music_speed_up.stop()
            self.sounds.ufo_sound.stop()
            self.sb.save_high_scores()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx

    def destroy_animation(self):
        """Play animation on death."""
        self.image = self.death_image[self.death_anim_counter]
        self.death_anim_counter += 1
        if self.death_anim_counter >= 10:
            self.death_anim_counter = 0
