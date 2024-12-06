import pygame
import os
from constants import SOUNDS_DIR

class AudioManager:
    def __init__(self):
        self.volume = 0.5
        self.is_muted = False
        pygame.mixer.music.set_volume(self.volume)
    
    def play_background_music(self, file_name="background-music.wav"):
        pygame.mixer.music.load(os.path.join(SOUNDS_DIR, file_name))
        pygame.mixer.music.play(-1)
    
    def adjust_volume(self, change):
        self.volume = max(0, min(1, self.volume + change))
        pygame.mixer.music.set_volume(self.volume)
    
    def mute(self):
        if self.is_muted:
            pygame.mixer.music.set_volume(self.volume)
        else:
            pygame.mixer.music.set_volume(0)
        self.is_muted = not self.is_muted
