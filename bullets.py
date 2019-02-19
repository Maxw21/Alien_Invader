import random
import pygame
from pygame.sprite import Group

from bullet import Bullet
from alien_bullet import AlienBullet
from explosion import Explosion


class Bullets:
    """A class to handle all bullets."""
    def __init__(self, ai_settings, screen, sprite_sheet, stats, sb,
                 ship, fleet, barriers, explosions, sounds):
        """Initialize instance attributes."""
        self.ai_settings = ai_settings
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.stats = stats
        self.sb = sb
        self.ship = ship
        self.fleet = fleet
        self.barriers = barriers
        self.explosions = explosions
        self.sounds = sounds
        self.bullets = Group()
        self.alien_bullets = Group()
        self.last_alien_amount = 55

        # Interactions Needed
        # ship_hit()
        # create_barriers

    def fire_bullet(self):
        """Fire a bullet if limit not reached yet."""
        bullet_offset = 0
        # Create a new bullet and add it to the bullets group.
        if len(self.bullets) < self.ai_settings.bullets_allowed:
            self.sounds.ship_bullet_sound.play()
            for _ in range(3):
                new_bullet = Bullet(ai_settings=self.ai_settings, screen=self.screen,
                                    ship=self.ship, bullet_y=bullet_offset)
                self.bullets.add(new_bullet)
                bullet_offset += 55

    def alien_shoot(self, alien):
        """Create a bullet from an alien."""
        self.sounds.alien_bullet_sound.play()
        new_bullet = AlienBullet(screen=self.screen, sprite_sheet=self.sprite_sheet, x=alien.rect.x,
                                 y=alien.rect.y, version=random.randint(0, 1))
        self.alien_bullets.add(new_bullet)

    def update_bullets(self, display):
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

        self.check_bullet_alien_collisions(display=display)
        self.check_bullet_ship_collisions(display=display)
        self.check_bullet_barrier_collisions(display=display)

    def check_bullet_alien_collisions(self, display):
        """Respond to bullet-alien collisions."""
        # Remove any bullets, aliens, and ufos that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.fleet.aliens, True, True)
        ufo_collisions = pygame.sprite.groupcollide(self.bullets, self.fleet.ufos, True, True)
        if collisions or ufo_collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    self.sounds.alien_destroy_sound.play()
                    explosion = Explosion(screen=self.screen, sprite_sheet=self.sprite_sheet, rect=alien.rect)
                    explosion.blitme()
                    self.explosions.add(explosion)
                    self.stats.score += (alien.points * self.ai_settings.score_scale)
                self.sb.prep_score()
            for ufos in ufo_collisions.values():
                for ufo in ufos:
                    self.sounds.ufo_sound.stop()
                    self.sounds.alien_destroy_sound.play()
                    ufo_points = random.randrange(40, 200, 10)
                    display.draw_ufo_points(ufo_points, ufo)
                    self.stats.score += ufo_points
                self.sb.prep_score()
            self.sb.check_high_score()
        if (len(self.fleet.aliens) == 40 or len(self.fleet.aliens) == 25 or len(self.fleet.aliens) == 10)\
                and self.last_alien_amount != len(self.fleet.aliens):
            # Speed up tempo of background music here
            self.sounds.background_music.stop()
            self.sounds.speed_up_bg_music()
            self.last_alien_amount = len(self.fleet.aliens)
            self.sounds.background_music.play(-1)
            print(self.sounds.background_music_counter)
        if len(self.fleet.aliens) == 0 and len(self.fleet.ufos) == 0:
            # If the entire fleet is destroyed, increase the difficulty and start a new level.
            self.bullets.empty()
            self.ai_settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
            self.fleet.create_fleet()
            self.sounds.background_music.stop()
            self.sounds.background_music = self.sounds.background_track[0]
            self.sounds.background_music.play(-1)
            self.sounds.background_music_counter = 1
            display.create_barriers()

    def check_bullet_ship_collisions(self, display):
        """Respond to bullet-ship collisions."""
        collisions = pygame.sprite.spritecollide(self.ship, self.alien_bullets, True)
        if collisions:
            self.ship.ship_hit(bullets=self, fleet=self.fleet, display=display)

    def check_bullet_barrier_collisions(self, display):
        """Respond to bullet-barrier collisions."""
        for barrier in display.barriers:
            pygame.sprite.groupcollide(self.bullets, barrier.barrier, True, True)
            pygame.sprite.groupcollide(self.alien_bullets, barrier.barrier, True, True)
