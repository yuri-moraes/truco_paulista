import random
from constants import TRUCO_LEVELS, TRUCO_VALUES, CARD_ORDER, SUIT_ORDER

def create_deck():
    """Cria e retorna um baralho embaralhado."""
    ranks = ['2', '3', '4', '5', '6', '7', 'jack', 'queen', 'king', 'ace']
    suits = ['diamonds', 'hearts', 'clubs', 'spades']
    deck = [f"{suit}_{rank}".lower() for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def determine_manilhas(vira_card):
    """Determina e retorna as manilhas com base na carta virada."""
    ranks = ['4', '5', '6', '7', 'jack', 'queen', 'king', 'ace', '2', '3']
    suit, vira_rank = vira_card.split('_')
    index = ranks.index(vira_rank)
    manilha_rank = ranks[(index + 1) % len(ranks)]
    manilhas = [f"{suit}_{manilha_rank}" for suit in ['diamonds', 'hearts', 'clubs', 'spades']]
    print(f"Vira: {vira_card}, Rank da Vira: {vira_rank}")
    return manilhas

def get_card_value(card, manilhas):
    """Retorna o valor da carta com base nas manilhas."""
    suit, rank = card.split('_')
    print(f"Analisando carta: {card}, Rank: {rank}, Manilhas: {manilhas}")
    if card in manilhas:
        return CARD_ORDER['Manilha'] * 10 + SUIT_ORDER[suit]
    else:
        return CARD_ORDER.get(rank, 0)

def reset_game():
    """Reinicia o jogo e retorna o estado inicial."""
    deck = create_deck()
    player_hand = deck[:3]
    opponent_hand = deck[3:6]
    vira_card = deck[6]
    manilhas = determine_manilhas(vira_card)
    return {
        'deck': deck,
        'player_hand': player_hand,
        'opponent_hand': opponent_hand,
        'vira_card': vira_card,
        'manilhas': manilhas
    }