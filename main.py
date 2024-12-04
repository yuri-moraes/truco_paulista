# main.py

import pygame
import sys
import time
import random
import os

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, TRUCO_LEVELS, TRUCO_VALUES, SOUNDS_DIR, CARD_WIDTH, CARD_HEIGHT
from resources import load_cards, load_sounds, load_background, load_back_card
from game_logic import reset_game, get_card_value
from utils import draw_text

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Truco Paulista")
    
    # Carregar Recursos
    cards = load_cards()
    sounds = load_sounds()
    background = load_background()
    back_card = load_back_card()
    
    if background is None or back_card is None:
        print("Erro ao carregar os recursos essenciais. Encerrando o jogo.")
        pygame.quit()
        sys.exit()
    
    
    # Variáveis do Jogo
    game_state = reset_game()
    deck = game_state['deck']
    player_hand = game_state['player_hand']
    opponent_hand = game_state['opponent_hand']
    vira_card = game_state['vira_card']
    manilhas = game_state['manilhas']
    
    # Pontuação
    player_score = 0
    opponent_score = 0
    bet_value = 1
    truco_requested = False
    truco_message = ""
    truco_accepted = False
    current_truco_level = -1  # -1 significa que não há truco ainda
    opponent_always_accept_truco = False  # Flag adicionada
    
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

    # Inicialização de música
    pygame.mixer.music.load(os.path.join(SOUNDS_DIR, "background-music.wav"))
    pygame.mixer.music.play(-1)
    volume = 0.5  # Volume inicial (50%)
    pygame.mixer.music.set_volume(volume)
    
    # Botões de controle de volume
     # Tamanho dos botões
    button_width = 50
    button_height = 50
    padding = 10  # Espaçamento entre os botões
    
    # Posicionar botões no canto inferior direito
    volume_up_button = pygame.Rect(
        SCREEN_WIDTH - button_width - padding,  # Posição x
        SCREEN_HEIGHT - (3 * button_height) - (3 * padding),  # Posição y
        button_width,
        button_height
    )
    volume_down_button = pygame.Rect(
        SCREEN_WIDTH - button_width - padding,  # Posição x
        SCREEN_HEIGHT - (2 * button_height) - (2 * padding),  # Posição y
        button_width,
        button_height
    )
    mute_button = pygame.Rect(
        SCREEN_WIDTH - button_width - padding,  # Posição x
        SCREEN_HEIGHT - button_height - padding,  # Posição y
        button_width,
        button_height
    )
    is_muted = False

    play_area_rect = pygame.Rect(
                        SCREEN_WIDTH // 2 - CARD_WIDTH // 2,  # Centraliza horizontalmente
                        SCREEN_HEIGHT - 325,  # Ajusta a altura (200px acima do rodapé)
                        CARD_WIDTH,
                        CARD_HEIGHT
                    )
    
    # Fonte
    font = pygame.font.SysFont(None, 36)
    
    # Botão de Truco
    truco_button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2 - 20, 140, 40)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Aumentar volume
                if volume_up_button.collidepoint(pos):
                    if volume < 1.0:
                        volume = min(1.0, volume + 0.1)
                        pygame.mixer.music.set_volume(volume)
                        is_muted = False
                
                # Diminuir volume
                elif volume_down_button.collidepoint(pos):
                    if volume > 0.0:
                        volume = max(0.0, volume - 0.1)
                        pygame.mixer.music.set_volume(volume)
                        if volume == 0.0:
                            is_muted = True
                
                # Mutar/desmutar
                elif mute_button.collidepoint(pos):
                    if is_muted:
                        pygame.mixer.music.set_volume(volume)  # Retorna ao volume anterior
                        is_muted = False
                    else:
                        pygame.mixer.music.set_volume(0.0)
                        is_muted = True
                if truco_button_rect.collidepoint(pos):
                    if not truco_requested:
                        if current_truco_level < len(TRUCO_LEVELS)-1:
                            next_truco_level = current_truco_level + 1
                            requested_level = TRUCO_LEVELS[next_truco_level]
                            requested_value = TRUCO_VALUES[requested_level]
                            
                            # Solicitar o Truco
                            truco_requested = True
                            truco_message = f"Você pediu {requested_level.capitalize()}!"
                            print(f"Jogador pediu {requested_level.capitalize()}")
                            
                            # Decidir se o oponente aceita ou recusa
                            if opponent_always_accept_truco:
                                truco_accepted = True
                                bet_value = requested_value
                                print(f"Oponente aceitou o {requested_level.capitalize()}")
                                # Mostrar mensagem de aceitação
                                accepted_text = f"Oponente aceitou o {requested_level.capitalize()}!"
                                draw_text(screen, accepted_text, font, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70))
                                pygame.display.flip()
                                time.sleep(1)  # Pausa breve para mostrar a mensagem
                                truco_requested = False  # Pronto para solicitar o próximo truco
                                current_truco_level += 1  # Incrementar o nível após aceitação
                                opponent_always_accept_truco = True  # Manter a flag como True
                            else:
                                # Oponente decide aleatoriamente aceitar ou recusar
                                if random.choice([True, False]):
                                    truco_accepted = True
                                    bet_value = requested_value
                                    print(f"Oponente aceitou o {requested_level.capitalize()}")
                                    # Mostrar mensagem de aceitação
                                    accepted_text = f"Oponente aceitou o {requested_level.capitalize()}!"
                                    draw_text(screen, accepted_text, font, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70))
                                    pygame.display.flip()
                                    time.sleep(1)  # Pausa breve para mostrar a mensagem
                                    truco_requested = False  # Pronto para solicitar o próximo truco
                                    current_truco_level += 1  # Incrementar o nível após aceitação
                                    opponent_always_accept_truco = True  # Agora o oponente sempre aceitará Truco
                                else:
                                    truco_accepted = False
                                    bet_value = requested_value
                                    player_score += bet_value  # Jogador ganha pontos
                                    print(f"Oponente recusou o {requested_level.capitalize()}")
                                    
                                    # Exibir mensagem de recusa
                                    declined_text = f"Oponente recusou o {requested_level.capitalize()}!"
                                    draw_text(screen, declined_text, font, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70))
                                    pygame.display.flip()
                                    time.sleep(2)
                                    
                                    # Verificar se o jogador já atingiu ou excedeu 12 pontos
                                    if player_score >= 12:
                                        # Jogador venceu o jogo
                                        victory_text = "VOCÊ VENCEU!"
                                        draw_text(screen, victory_text, font, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
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
                                        game_state = reset_game()
                                        deck = game_state['deck']
                                        player_hand = game_state['player_hand']
                                        opponent_hand = game_state['opponent_hand']
                                        vira_card = game_state['vira_card']
                                        manilhas = game_state['manilhas']
                                        round_results = []
                                        current_round = 1
                                        bet_value = 1
                                        truco_requested = False
                                        truco_message = ""
                                        truco_accepted = False
                                        current_truco_level = -1  # Resetar nível de truco
                                        player_played_cards = []
                                        opponent_always_accept_truco = False  # Resetar a flag
                                        # Reiniciar música de fundo
                                        try:
                                            pygame.mixer.music.load(os.path.join(SOUNDS_DIR, "background-music.wav"))
                                            pygame.mixer.music.play(-1)
                                        except pygame.error as e:
                                            print(f"Erro ao carregar a música de fundo: {e}")
                                        continue  # Pular o resto do loop
                                    else:
                                        # Reiniciar a partida
                                        game_state = reset_game()
                                        deck = game_state['deck']
                                        player_hand = game_state['player_hand']
                                        opponent_hand = game_state['opponent_hand']
                                        vira_card = game_state['vira_card']
                                        manilhas = game_state['manilhas']
                                        round_results = []
                                        current_round = 1
                                        bet_value = 1
                                        truco_requested = False
                                        truco_message = ""
                                        player_played_cards = []
                                        current_truco_level = -1  # Resetar nível de truco
                                        opponent_always_accept_truco = False  # Resetar a flag
                                        continue  # Pular o resto do loop
                        else:
                            print("Truco já atingiu o nível máximo.")
                            # Opcional: mostrar mensagem que Truco está no nível máximo
                            truco_max_text = "Truco Máximo!"
                            draw_text(screen, truco_max_text, font, BLACK, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 70))
                            pygame.display.flip()
                            time.sleep(1)
                else:
                    # Detectar clique nas cartas do jogador
                    if player_turn:
                        for i, card in enumerate(player_hand):
                            x = SCREEN_WIDTH // 2 - len(player_hand) * 50 + i * 100
                            y = SCREEN_HEIGHT - 140
                            card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
                            if card_rect.collidepoint(pos):
                                dragging_card = card
                                dragging_pos = pos
                                player_hand.pop(i)
                                break
            
            elif event.type == pygame.MOUSEMOTION:
                if dragging_card:
                    dragging_pos = event.pos
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_card:
                    pos = pygame.mouse.get_pos()
                    # Verifica se a carta está na área de jogo
                    if play_area_rect.collidepoint(pos):
                        # Centraliza a carta na borda
                        played_cards['player'] = dragging_card
                        print(f"Jogador jogou a carta: {played_cards['player']}")
                        player_played_cards.append(dragging_card)
                        # Posiciona no centro da área delimitada pela borda
                        play_card_position = (
                            play_area_rect.x + play_area_rect.width // 2 - CARD_WIDTH // 2,
                            play_area_rect.y + play_area_rect.height // 2 - CARD_HEIGHT // 2
                        )
                        player_turn = False
                        opponent_turn = True
                    else:
                        # Se não estiver na área, retorna a carta para a mão do jogador
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
                        victory_text = "VOCÊ VENCEU!"
                        draw_text(screen, victory_text, font, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
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
                        game_state = reset_game()
                        deck = game_state['deck']
                        player_hand = game_state['player_hand']
                        opponent_hand = game_state['opponent_hand']
                        vira_card = game_state['vira_card']
                        manilhas = game_state['manilhas']
                        round_results = []
                        current_round = 1
                        bet_value = 1
                        truco_requested = False
                        truco_message = ""
                        truco_accepted = False
                        current_truco_level = -1
                        player_played_cards = []
                        opponent_always_accept_truco = False  # Resetar a flag
                        # Reiniciar música de fundo
                        try:
                            pygame.mixer.music.load(os.path.join(SOUNDS_DIR, "background-music.wav"))
                            pygame.mixer.music.play(-1)
                        except pygame.error as e:
                            print(f"Erro ao carregar a música de fundo: {e}")
                        continue
        
                    elif opponent_score >= 12:
                        # Jogador perdeu o jogo
                        defeat_text = "VOCÊ PERDEU!"
                        draw_text(screen, defeat_text, font, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
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
                        game_state = reset_game()
                        deck = game_state['deck']
                        player_hand = game_state['player_hand']
                        opponent_hand = game_state['opponent_hand']
                        vira_card = game_state['vira_card']
                        manilhas = game_state['manilhas']
                        round_results = []
                        current_round = 1
                        bet_value = 1
                        truco_requested = False
                        truco_message = ""
                        truco_accepted = False
                        current_truco_level = -1
                        player_played_cards = []
                        opponent_always_accept_truco = False  # Resetar a flag
                        # Reiniciar música de fundo
                        try:
                            pygame.mixer.music.load(os.path.join(SOUNDS_DIR, "background-music.wav"))
                            pygame.mixer.music.play(-1)
                        except pygame.error as e:
                            print(f"Erro ao carregar a música de fundo: {e}")
                        continue
        
                    # Resetar para a próxima partida
                    game_state = reset_game()
                    deck = game_state['deck']
                    player_hand = game_state['player_hand']
                    opponent_hand = game_state['opponent_hand']
                    vira_card = game_state['vira_card']
                    manilhas = game_state['manilhas']
                    round_results = []
                    current_round = 1
                    bet_value = 1
                    truco_requested = False
                    truco_message = ""
                    truco_accepted = False
                    current_truco_level = -1  # Resetar nível de truco
                    player_played_cards = []
                    opponent_always_accept_truco = False  # Resetar a flag
        
        # Desenhar a Tela
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        # Desenhar a área de jogo com borda, se definida
        if 'play_area_rect' in locals():
            pygame.draw.rect(screen, (0, 0, 0), play_area_rect, 3)
        else:
            print("Erro: Área de jogo não foi definida corretamente.")

    
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
        
        # Desenhar Carta Jogada pelo Jogador no Local Centralizado
        if played_cards['player']:
            card_key = played_cards['player'].lower()
            if card_key in cards:
                screen.blit(cards[card_key], play_card_position)
            else:
                print(f"Carta '{card_key}' não encontrada nas imagens.")

    
        # Desenhar Cartas Jogadas pelo Jogador acima das Cartas dele
        for i, card in enumerate(player_played_cards):
            card_key = card.lower()
            if card_key in cards:
                x = SCREEN_WIDTH // 2 - 40
                y = SCREEN_HEIGHT - 300 - i * 30  # Posição acima das cartas do jogador, com sobreposição
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
        player_score_text = f"Jogador: {player_score}"
        opponent_score_text = f"Oponente: {opponent_score}"
        draw_text(screen, player_score_text, font, BLACK, (50, SCREEN_HEIGHT - 50))
        draw_text(screen, opponent_score_text, font, BLACK, (SCREEN_WIDTH - 200, 50))
    
        # Exibir Rodada Atual
        round_text = f"Rodada: {current_round}"
        draw_text(screen, round_text, font, BLACK, (10, 10))
    
        # Exibir Resultados das Rodadas
        for i, result in enumerate(round_results):
            result_surface = f"Rodada {i+1}: {result}"
            draw_text(screen, result_surface, font, BLACK, (10, 40 + i * 30))
    
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

         # Botões
        pygame.draw.rect(screen, (0, 255, 0), volume_up_button)  # Aumentar volume
        pygame.draw.rect(screen, (255, 255, 0), volume_down_button)  # Diminuir volume
        pygame.draw.rect(screen, (255, 0, 0), mute_button)  # Mutar som
        
        # Ícones de controle de volume (opcional, pode usar imagens)
        font = pygame.font.SysFont(None, 36)
        draw_text(screen, "+", font, BLACK, volume_up_button.center)
        draw_text(screen, "-", font, BLACK, volume_down_button.center)
        draw_text(screen, "M", font, BLACK, mute_button.center)
    
        # Exibir Mensagem de Truco (se houver)
        if truco_requested:
            message_surface = truco_message
            draw_text(screen, message_surface, font, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))
            if truco_accepted:
                accepted_text = "Oponente aceitou o Truco!"
                draw_text(screen, accepted_text, font, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70))
            else:
                declined_text = "Oponente recusou o Truco!"
                draw_text(screen, declined_text, font, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70))
    
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
