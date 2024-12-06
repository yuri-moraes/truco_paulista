import pygame
from utils import draw_text

class UIManager:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
    
    def draw_card(self, card_image, position):
        self.screen.blit(card_image, position)
    
    def draw_text(self, text, position, color=(0, 0, 0)):
        draw_text(self.screen, text, self.font, color, position)
    
    def draw_button(self, rect, text, color=(0, 128, 0), text_color=(255, 255, 255)):
        pygame.draw.rect(self.screen, color, rect)
        text_surface = self.font.render(text, True, text_color)
        self.screen.blit(text_surface, text_surface.get_rect(center=rect.center))
