import random
import pygame
from pygame.sprite import Group

from alien import Alien
from ufo import Ufo


class Fleet:
    """A class to manage all alien and ufo sprites."""
    def __init__(self, ai_settings, screen, sprite_sheet, sounds):
        """Initialize the fleet."""
        self.ai_settings = ai_settings
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.sounds = sounds
        self.aliens = Group()
        self.ufos = Group()
        self.alien_bullet_time = 0
        self.spawn_ufo = 0

    def create_fleet(self):
        """Create a full fleet of aliens."""
        row = 4
        self.aliens.empty()
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
                return True

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

    def update_aliens(self, ship, display, bullets):
        """Check if the fleet is at an edge, and then update the positions of all aliens in the fleet."""
        self.check_fleet_edges()
        if display.animate_aliens == self.ai_settings.animate_aliens:
            for alien in self.aliens:
                alien.switch_image()
            display.animate_aliens = 0
        display.animate_aliens += 1
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(ship, self.aliens):
            ship.ship_hit(bullets=bullets, fleet=self, display=display)

        # Shoot bullets from aliens
        if self.alien_bullet_time >= random.randint(500, 1000):
            alien_list = self.aliens.sprites()
            alien_firing = len(alien_list) - 11
            if alien_firing < 0:
                alien_firing = 0
            if len(alien_list) > 0:
                bullets.alien_shoot(alien_list[random.randint(alien_firing, len(alien_list) - 1)])
            self.alien_bullet_time = 0
        self.alien_bullet_time += 1
        # Look for aliens hitting the bottom of the screen.
        if self.check_aliens_bottom():
            ship.ship_hit(bullets=bullets, fleet=self, display=display)

    def create_ufos(self):
        """Create ufos at a random interval."""
        if len(self.ufos) < 1:
            self.sounds.ufo_sound.play(-1)
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
                self.sounds.ufo_sound.stop()
                self.spawn_ufo = 0
