import pygame

def draw_text(screen, text, font, color, position):
    """Desenha texto na tela."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)