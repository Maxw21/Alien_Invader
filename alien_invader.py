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
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick(60)
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invader")

    # Import sprite sheet
    sprite_sheet = SpriteSheet(file_name='images/spritesheet.png')

    # Make the Play button.
    play_button = Button(screen=screen, msg="Play", order=0)
    score_button = Button(screen=screen, msg="High Scores", order=1)

    # Open high score file
    try:
        high_score_file = open("high_score_file.txt", "r+")
    except FileNotFoundError:
        high_score_file = open("high_score_file.txt", "w+")


    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings=ai_settings)
    sb = Scoreboard(ai_settings=ai_settings, screen=screen, stats=stats, sprite_sheet=sprite_sheet)

    # Make a ship, a group of bullets, a group of aliens, and a group of ufos.
    ship = Ship(ai_settings=ai_settings, screen=screen, sprite_sheet=sprite_sheet)
    bullets = Group()
    alien_bullets = Group()
    aliens = Group()
    ufos = Group()
    barriers = []
    explosions = Group()

    # Create the fleet of aliens.
    game_manager = GameManager(ai_settings=ai_settings, screen=screen, sprite_sheet=sprite_sheet,
                               play_button=play_button, score_button=score_button, stats=stats,
                               sb=sb, ship=ship, bullets=bullets, aliens=aliens, ufos=ufos,
                               barriers=barriers, explosions=explosions, alien_bullets=alien_bullets,
                               high_score_file=high_score_file)

    game_manager.create_fleet()

    # Start the main loop for the game.
    while True:
        game_manager.check_events()

        if stats.game_active:
            ship.update()
            game_manager.update_bullets()
            game_manager.update_aliens()
            game_manager.update_ufos()

        game_manager.update_screen()


run_game()
