import pygame
import os
from constants import IMAGES_DIR, SOUNDS_DIR, SCREEN_WIDTH, SCREEN_HEIGHT, CARD_WIDTH, CARD_HEIGHT

def load_cards():
    """Carrega todas as imagens das cartas e retorna um dicionário."""
    cards = {}
    for file_name in os.listdir(IMAGES_DIR):
        if file_name.endswith(".png"):
            card_name = file_name.split(".")[0].lower()
            try:
                image = pygame.image.load(os.path.join(IMAGES_DIR, file_name))
                cards[card_name] = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
            except pygame.error as e:
                print(f"Erro ao carregar a imagem '{file_name}': {e}")
    return cards

def load_sounds():
    """Carrega todos os sons e retorna um dicionário."""
    sounds = {}
    for file_name in os.listdir(SOUNDS_DIR):
        if file_name.endswith(".mp3") or file_name.endswith(".wav"):
            sound_name = file_name.split(".")[0]
            try:
                sounds[sound_name] = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, file_name))
            except pygame.error as e:
                print(f"Erro ao carregar o som '{file_name}': {e}")
    return sounds

def load_background():
    """Carrega a imagem de fundo."""
    background_path = os.path.join(IMAGES_DIR, "background-img.jpg")
    try:
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        return background
    except pygame.error as e:
        print(f"Erro ao carregar o fundo '{background_path}': {e}")
        return None

def load_back_card():
    """Carrega a imagem da carta virada para o oponente."""
    back_card_path = os.path.join(IMAGES_DIR, "background-removebg-preview.png")
    try:
        back_card = pygame.image.load(back_card_path)
        back_card = pygame.transform.scale(back_card, (CARD_WIDTH, CARD_HEIGHT))
        return back_card
    except pygame.error as e:
        print(f"Erro ao carregar a carta de fundo '{back_card_path}': {e}")
        return None
