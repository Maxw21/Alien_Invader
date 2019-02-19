import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from sprite_sheet import SpriteSheet
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from fleet import Fleet
from event_handler import EventHandler
from display import Display
from sounds import Sounds
from bullets import Bullets


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

    # Make the Play and Scores button.
    play_button = Button(screen=screen, msg="Play", order=0)
    score_button = Button(screen=screen, msg="High Scores", order=1)

    # Open high score file
    try:
        high_score_file = open("high_score_file.txt", "r+")
    except FileNotFoundError:
        high_score_file = open("high_score_file.txt", "w+")

    # Make sound manager
    sounds = Sounds()

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings=ai_settings)
    sb = Scoreboard(ai_settings=ai_settings, screen=screen, stats=stats,
                    sprite_sheet=sprite_sheet, high_score_file=high_score_file)

    # Make the game objects.
    ship = Ship(ai_settings=ai_settings, screen=screen, sprite_sheet=sprite_sheet, stats=stats, sb=sb, sounds=sounds)
    explosions = Group()
    barriers = []
    fleet = Fleet(ai_settings=ai_settings, screen=screen, sprite_sheet=sprite_sheet, sounds=sounds)
    bullets = Bullets(ai_settings=ai_settings, screen=screen, sprite_sheet=sprite_sheet, stats=stats, sb=sb,
                      ship=ship, fleet=fleet, barriers=barriers, explosions=explosions, sounds=sounds)

    # Make the event handler
    event_handler = EventHandler(ai_settings=ai_settings, play_button=play_button, score_button=score_button,
                                 stats=stats, sb=sb, ship=ship, bullets=bullets, fleet=fleet, sounds=sounds)

    # Make the display manager
    display = Display(ai_settings=ai_settings, screen=screen, sprite_sheet=sprite_sheet, play_button=play_button,
                      score_button=score_button, stats=stats, sb=sb, ship=ship, bullets=bullets, fleet=fleet,
                      barriers=barriers, explosions=explosions, event_handler=event_handler)

    # Start the main loop for the game.
    while True:
        event_handler.check_events(display=display)

        if stats.game_active:
            ship.update()
            bullets.update_bullets(display=display)
            fleet.update_aliens(ship=ship, display=display, bullets=bullets)
            fleet.update_ufos()

        display.update_screen()


run_game()
