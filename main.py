import pygame
import os
import sys
import random
import time

# Inicialização do Pygame
pygame.init()

# Configuração da Tela
SCREEN_WIDTH = 1240
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Truco Paulista")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Carregar o Fundo
background = pygame.image.load("background-img.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Diretórios das Imagens e Sons
IMAGES_DIR = "images"
SOUNDS_DIR = "sounds"

# Hierarquia das Cartas
CARD_ORDER = {
    '4': 1,
    '5': 2,
    '6': 3,
    '7': 4,
    'queen': 5,
    'jack': 6,
    'king': 7,
    'ace': 8,
    '2': 9,
    '3': 10,
    'Manilha': 11
}

# Sequência dos Naipes para Manilhas
SUIT_ORDER = {
    'clubs': 4,
    'hearts': 3,
    'spades': 2,
    'diamonds': 1
}

# Níveis de Truco
TRUCO_LEVELS = ['truco', 'seis', 'nove', 'doze']
TRUCO_VALUES = {'truco':3, 'seis':6, 'nove':9, 'doze':12}

# Carregar Cartas
def load_cards():
    cards = {}
    for file_name in os.listdir(IMAGES_DIR):
        if file_name.endswith(".png"):
            card_name = file_name.split(".")[0]
            card_name = card_name.lower()
            try:
                image = pygame.image.load(os.path.join(IMAGES_DIR, file_name))
                cards[card_name] = pygame.transform.scale(image, (80, 120))
            except pygame.error as e:
                print(f"Erro ao carregar a imagem '{file_name}': {e}")
    return cards

# Carregar Sons
def load_sounds():
    sounds = {}
    for file_name in os.listdir(SOUNDS_DIR):
        if file_name.endswith(".mp3") or file_name.endswith(".wav"):
            sound_name = file_name.split(".")[0]
            try:
                sounds[sound_name] = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, file_name))
            except pygame.error as e:
                print(f"Erro ao carregar o som '{file_name}': {e}")
    return sounds

# Criar Baralho
def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', 'jack', 'queen', 'king', 'ace']
    suits = ['diamonds', 'hearts', 'clubs', 'spades']
    deck = [f"{suit}_{rank}".lower() for suit in suits for rank in ranks]
    return deck

# Determinar Manilhas
def determine_manilhas(vira_card):
    ranks = ['4', '5', '6', '7', 'jack', 'queen', 'king', 'ace', '2', '3']
    suit, vira_rank = vira_card.split('_')
    index = ranks.index(vira_rank)
    manilha_rank = ranks[(index + 1) % len(ranks)]
    manilhas = [f"{suit}_{manilha_rank}" for suit in ['diamonds', 'hearts', 'clubs', 'spades']]
    print(f"Vira: {vira_card}, Rank da Vira: {vira_rank}")
    return manilhas

# Função para Obter o Valor da Carta
def get_card_value(card, manilhas):
    suit, rank = card.split('_')
    print(f"Analisando carta: {card}, Rank: {rank}, Manilhas: {manilhas}")
    if card in manilhas:
        return CARD_ORDER['Manilha'] * 10 + SUIT_ORDER[suit]
    else:
        return CARD_ORDER[rank]

# Função para Reiniciar o Jogo
def reset_game():
    global deck, player_hand, opponent_hand, vira_card, manilhas
    deck = create_deck()
    random.shuffle(deck)
    player_hand = deck[:3]
    opponent_hand = deck[3:6]
    vira_card = deck[6]
    manilhas = determine_manilhas(vira_card)

# Função Principal
def main():
    clock = pygame.time.Clock()
    running = True

    # Carregar Recursos
    cards = load_cards()
    sounds = load_sounds()
    back_card = pygame.image.load(os.path.join(IMAGES_DIR, "blank_card.png"))
    back_card = pygame.transform.scale(back_card, (80, 120))

    # Tocar Música de Fundo
    try:
        pygame.mixer.music.load(os.path.join(SOUNDS_DIR, "background-music.wav"))
    except pygame.error as e:
        print(f"Erro ao carregar a música de fundo: {e}")
    else:
        pygame.mixer.music.play(-1)  # -1 para tocar em loop

    # Variáveis do Jogo
    global deck, player_hand, opponent_hand, vira_card, manilhas
    deck = create_deck()
    random.shuffle(deck)

    # Distribuir Cartas
    player_hand = deck[:3]
    opponent_hand = deck[3:6]
    vira_card = deck[6]
    manilhas = determine_manilhas(vira_card)

    # Pontuação
    player_score = 0
    opponent_score = 0
    bet_value = 1
    truco_requested = False
    truco_message = ""
    truco_accepted = False
    current_truco_level = -1  # -1 significa que não há truco ainda

    # Variáveis para arrastar
    dragging_card = None
    dragging_pos = None

    # Variáveis da Rodada
    player_turn = False  # Oponente começa jogando
    opponent_turn = True
    played_cards = {'player': None, 'opponent': None}
    player_played_cards = []  # Lista de cartas jogadas pelo jogador
    round_results = []
    current_round = 1

    # Fonte
    font = pygame.font.SysFont(None, 36)

    # Botão de Truco
    truco_button_rect = pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 40)

    # Loop do Jogo
    while running:
        # Processamento de Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Detectar clique em uma carta ou no botão de Truco
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if truco_button_rect.collidepoint(pos):
                    if not truco_requested:
                        if current_truco_level < len(TRUCO_LEVELS)-1:
                            # Solicitar o próximo nível de Truco
                            current_truco_level +=1
                            requested_level = TRUCO_LEVELS[current_truco_level]
                            truco_requested = True
                            truco_message = f"Você pediu {requested_level.capitalize()}!"
                            print(f"Jogador pediu {requested_level.capitalize()}")

                            # Oponente aceita ou recusa aleatoriamente
                            if random.choice([True, False]):
                                truco_accepted = True
                                bet_value = TRUCO_VALUES[requested_level]
                                print(f"Oponente aceitou o {requested_level.capitalize()}")
                                # Mostrar mensagem de aceitação
                                accepted_text = font.render(f"Oponente aceitou o {requested_level.capitalize()}!", True, BLACK)
                                screen.blit(accepted_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70))
                                pygame.display.flip()
                                time.sleep(1)  # Pausa breve para mostrar a mensagem
                                truco_requested = False  # Pronto para solicitar o próximo truco
                            else:
                                truco_accepted = False
                                bet_value = TRUCO_VALUES[requested_level]
                                player_score += bet_value  # Jogador ganha pontos
                                print(f"Oponente recusou o {requested_level.capitalize()}")
                                # Exibir mensagem de recusa
                                declined_text = font.render(f"Oponente recusou o {requested_level.capitalize()}!", True, BLACK)
                                screen.blit(declined_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70))
                                pygame.display.flip()
                                time.sleep(2)
                                # Reiniciar a partida
                                reset_game()
                                round_results = []
                                current_round = 1
                                bet_value = 1
                                truco_requested = False
                                truco_message = ""
                                player_played_cards = []
                                current_truco_level = -1  # Resetar nível de truco
                                continue  # Pular o resto do loop
                        else:
                            print("Já atingiu o nível máximo de Truco")
                            # Opcional: mostrar mensagem que truco está no nível máximo
                            truco_max_text = font.render("Truco Máximo!", True, BLACK)
                            screen.blit(truco_max_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 70))
                            pygame.display.flip()
                            time.sleep(1)
                    else:
                        print("Truco já foi pedido")
                else:
                    # Detectar clique nas cartas do jogador
                    if player_turn:
                        for i, card in enumerate(player_hand):
                            x = SCREEN_WIDTH // 2 - len(player_hand) * 50 + i * 100
                            y = SCREEN_HEIGHT - 140
                            card_rect = pygame.Rect(x, y, 80, 120)
                            if card_rect.collidepoint(pos):
                                dragging_card = card
                                dragging_pos = pos
                                player_hand.pop(i)
                                break

            # Atualizar posição da carta durante o arraste
            elif event.type == pygame.MOUSEMOTION and dragging_card:
                dragging_pos = event.pos

            # Soltar a carta na área designada
            elif event.type == pygame.MOUSEBUTTONUP and dragging_card:
                pos = event.pos
                play_area_rect = pygame.Rect(SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT - 260, 80, 120)
                if play_area_rect.collidepoint(pos):  # Verifica se está na área de jogo
                    played_cards['player'] = dragging_card
                    print(f"Jogador jogou a carta: {played_cards['player']}")
                    player_played_cards.append(dragging_card)
                    player_turn = False
                    opponent_turn = True
                else:  # Se não for na área correta, retorna a carta para a mão
                    player_hand.append(dragging_card)
                dragging_card = None
                dragging_pos = None

        # Lógica do Jogo

        # Oponente joga automaticamente se for o turno dele
        if opponent_turn and played_cards['opponent'] is None:
            if opponent_hand:
                played_cards['opponent'] = opponent_hand.pop(0)
                print(f"Oponente jogou a carta: {played_cards['opponent']}")
                opponent_turn = False
                player_turn = True  # Agora é a vez do jogador
            else:
                played_cards['opponent'] = None

        # Determinar quem vence a rodada
        if played_cards['player'] and played_cards['opponent']:
            # Ambos jogaram suas cartas, determinar o vencedor
            player_card_value = get_card_value(played_cards['player'], manilhas)
            opponent_card_value = get_card_value(played_cards['opponent'], manilhas)
            if player_card_value > opponent_card_value:
                round_results.append('Jogador')
                print("Jogador venceu esta rodada")
            elif player_card_value < opponent_card_value:
                round_results.append('Oponente')
                print("Oponente venceu esta rodada")
            else:
                round_results.append('Empate')
                print("Empate nesta rodada")

            # Resetar variáveis para a próxima rodada
            played_cards['player'] = None
            played_cards['opponent'] = None
            opponent_turn = True
            player_turn = False

            # Incrementar rodada atual
            current_round += 1

            # Verificar se o jogo acabou
            if current_round > 3:
                # Jogo acabou, determinar o vencedor
                player_rounds_won = round_results.count('Jogador')
                opponent_rounds_won = round_results.count('Oponente')

                if player_rounds_won > opponent_rounds_won:
                    player_score += bet_value
                    print(f"Jogador venceu a partida e ganhou {bet_value} pontos")
                elif player_rounds_won < opponent_rounds_won:
                    opponent_score += bet_value
                    print(f"Oponente venceu a partida e ganhou {bet_value} pontos")
                else:
                    print("Partida empatada")

                # Verificar se alguém atingiu 12 pontos
                if player_score >= 12:
                    # Jogador venceu o jogo
                    victory_text = font.render("VOCÊ VENCEU!", True, BLACK)
                    screen.blit(victory_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
                    pygame.display.flip()
                    # Tocar música de vitória
                    pygame.mixer.music.stop()
                    if 'winner-song' in sounds:
                        sounds['winner-song'].play()
                    else:
                        print("Erro: Música de vitória 'winner-song' não encontrada.")
                    time.sleep(5)
                    # Parar música de vitória
                    if 'winner-song' in sounds:
                        sounds['winner-song'].stop()
                    # Reiniciar o jogo
                    player_score = 0
                    opponent_score = 0
                    reset_game()
                    round_results = []
                    current_round = 1
                    bet_value = 1
                    truco_requested = False
                    truco_message = ""
                    truco_accepted = False
                    current_truco_level = -1
                    player_played_cards = []
                    # Reiniciar música de fundo
                    try:
                        pygame.mixer.music.load(os.path.join(SOUNDS_DIR, "background-music.wav"))
                    except pygame.error as e:
                        print(f"Erro ao carregar a música de fundo: {e}")
                    else:
                        pygame.mixer.music.play(-1)
                    continue

                elif opponent_score >= 12:
                    # Jogador perdeu o jogo
                    defeat_text = font.render("VOCÊ PERDEU!", True, BLACK)
                    screen.blit(defeat_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
                    pygame.display.flip()
                    # Tocar música de derrota
                    pygame.mixer.music.stop()
                    if 'looser-song' in sounds:
                        sounds['looser-song'].play()
                    else:
                        print("Erro: Música de derrota 'looser-song' não encontrada.")
                    time.sleep(5)
                    # Parar música de derrota
                    if 'looser-song' in sounds:
                        sounds['looser-song'].stop()
                    # Reiniciar o jogo
                    player_score = 0
                    opponent_score = 0
                    reset_game()
                    round_results = []
                    current_round = 1
                    bet_value = 1
                    truco_requested = False
                    truco_message = ""
                    truco_accepted = False
                    current_truco_level = -1
                    player_played_cards = []
                    # Reiniciar música de fundo
                    try:
                        pygame.mixer.music.load(os.path.join(SOUNDS_DIR, "background-music.wav"))
                    except pygame.error as e:
                        print(f"Erro ao carregar a música de fundo: {e}")
                    else:
                        pygame.mixer.music.play(-1)
                    continue

                # Resetar para a próxima partida
                reset_game()
                round_results = []
                current_round = 1
                bet_value = 1
                truco_requested = False
                truco_message = ""
                truco_accepted = False
                current_truco_level = -1
                player_played_cards = []

        # Desenhar a Tela
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        # Desenhar Mãos do Jogador
        for i, card in enumerate(player_hand):
            x = SCREEN_WIDTH // 2 - len(player_hand) * 50 + i * 100
            y = SCREEN_HEIGHT - 140
            card_key = card.lower()
            if card_key in cards:
                screen.blit(cards[card_key], (x, y))
            else:
                print(f"Carta '{card_key}' não encontrada nas imagens.")

        # Desenhar Cartas do Oponente Viradas
        for i, card in enumerate(opponent_hand):
            x = SCREEN_WIDTH // 2 - len(opponent_hand) * 50 + i * 100
            y = 20
            screen.blit(back_card, (x, y))

        # Desenhar Carta Jogada pelo Oponente abaixo das Cartas Ocultas
        if played_cards['opponent']:
            card_key = played_cards['opponent'].lower()
            if card_key in cards:
                x = SCREEN_WIDTH // 2 - 40
                y = 160  # Posição abaixo das cartas ocultas
                screen.blit(cards[card_key], (x, y))
            else:
                print(f"Carta '{card_key}' não encontrada nas imagens.")

        # Desenhar Cartas Jogadas pelo Jogador acima das Cartas dele
        for i, card in enumerate(player_played_cards):
            card_key = card.lower()
            if card_key in cards:
                x = SCREEN_WIDTH // 2 - 40
                y = SCREEN_HEIGHT - 260 - i * 30  # Posição acima das cartas do jogador, com sobreposição
                screen.blit(cards[card_key], (x, y))
            else:
                print(f"Carta '{card_key}' não encontrada nas imagens.")

        # Desenhar Carta Arrastada (se houver)
        if dragging_card and dragging_pos:
            card_key = dragging_card.lower()
            if card_key in cards:
                screen.blit(cards[card_key], (dragging_pos[0] - 40, dragging_pos[1] - 60))
            else:
                print(f"Carta '{card_key}' não encontrada nas imagens.")

        # Desenhar Vira
        card_key = vira_card.lower()
        if card_key in cards:
            screen.blit(cards[card_key], (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 - 60))
        else:
            print(f"Carta '{card_key}' não encontrada nas imagens.")

        # Desenhar Pontuação
        player_score_text = font.render(f"Jogador: {player_score}", True, BLACK)
        opponent_score_text = font.render(f"Oponente: {opponent_score}", True, BLACK)
        screen.blit(player_score_text, (50, SCREEN_HEIGHT - 50))
        screen.blit(opponent_score_text, (SCREEN_WIDTH - 200, 50))

        # Exibir Rodada Atual
        round_text = font.render(f"Rodada: {current_round}", True, BLACK)
        screen.blit(round_text, (10, 10))

        # Exibir Resultados das Rodadas
        for i, result in enumerate(round_results):
            result_surface = font.render(f"Rodada {i+1}: {result}", True, BLACK)
            screen.blit(result_surface, (10, 40 + i * 30))

        # Determinar o Próximo Rótulo do Botão
        if current_truco_level < len(TRUCO_LEVELS)-1:
            next_request = TRUCO_LEVELS[current_truco_level +1]
            button_label = f"Pedir {next_request.capitalize()}"
        else:
            button_label = "Truco Máximo"

        # Desenhar Botão de Truco
        pygame.draw.rect(screen, (0, 128, 0), truco_button_rect)
        truco_text = font.render(button_label, True, WHITE)
        text_rect = truco_text.get_rect(center=truco_button_rect.center)
        screen.blit(truco_text, text_rect)

        # Exibir Mensagem de Truco (se houver)
        if truco_requested:
            message_surface = font.render(truco_message, True, BLACK)
            screen.blit(message_surface, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))
            if truco_accepted:
                accepted_text = font.render("Oponente aceitou o Truco!", True, BLACK)
                screen.blit(accepted_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70))
            else:
                declined_text = font.render("Oponente recusou o Truco!", True, BLACK)
                screen.blit(declined_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
