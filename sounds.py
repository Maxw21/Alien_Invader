import pygame


class Sounds:
    """A class to hold the sound files"""
    def __init__(self):
        self.background_music_counter = 1
        self.alien_bullet_sound = pygame.mixer.Sound('sounds/alien_bullet_sound.wav')
        self.alien_destroy_sound = pygame.mixer.Sound('sounds/alien_destroy_sound.wav')
        self.ship_bullet_sound = pygame.mixer.Sound('sounds/ship_bullet_sound.wav')
        self.ship_destroy_sound = pygame.mixer.Sound('sounds/ship_destroy_sound.wav')
        self.alien_destroy_sound = pygame.mixer.Sound('sounds/alien_destroy_sound.wav')
        self.ufo_sound = pygame.mixer.Sound('sounds/ufo_sound.wav')
        self.background_music = pygame.mixer.Sound('sounds/background_music.wav')
        self.background_track = []
        self.background_track.append(self.background_music)
        self.background_track.append(pygame.mixer.Sound('sounds/background_2.wav'))
        self.background_track.append(pygame.mixer.Sound('sounds/background_3.wav'))
        self.background_track.append(pygame.mixer.Sound('sounds/background_4.wav'))

    def speed_up_bg_music(self):
        """"Speed up the background."""
        self.background_music = self.background_track[self.background_music_counter]
        self.background_music_counter += 1
        if self.background_music_counter > 3:
            self.background_music_counter = 1
