import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from sprite_sheet import SpriteSheet
from scoreboard import Scoreboard
from button import Button
from ship import Ship

from game_manager import GameManager


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Import sprite sheet
    sprite_sheet = SpriteSheet(file_name='images/spritesheet.png')

    # Make the Play button.
    play_button = Button(screen=screen, msg="Play")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings=ai_settings)
    sb = Scoreboard(ai_settings=ai_settings, screen=screen, stats=stats, sprite_sheet=sprite_sheet)

    # Make a ship, a group of bullets, a group of aliens, and a group of ufos.
    ship = Ship(ai_settings=ai_settings, screen=screen, sprite_sheet=sprite_sheet)
    bullets = Group()
    aliens = Group()
    ufos = Group()

    # Create the fleet of aliens.
    game_manager = GameManager(ai_settings=ai_settings, screen=screen,
                               sprite_sheet=sprite_sheet, play_button=play_button,
                               stats=stats, sb=sb, ship=ship, bullets=bullets,
                               aliens=aliens, ufos=ufos)

    game_manager.create_fleet()

    # Start the main loop for the game.
    while True:
        game_manager.check_events()

        if stats.game_active:
            ship.update()
            game_manager.update_bullets()
            game_manager.update_aliens()

        game_manager.update_screen()


run_game()
