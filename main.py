import pygame
import sys
import time
import random
import os

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, TRUCO_LEVELS, TRUCO_VALUES, SOUNDS_DIR, CARD_WIDTH, CARD_HEIGHT
from resources import load_cards, load_sounds, load_background, load_back_card
from game_logic import get_card_value
from game_manager import GameManager  # Removida a vírgula aqui
from audio_manager import AudioManager
from ui import UIManager
from utils import draw_text

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Truco Paulista")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # Carregar Recursos
    cards = load_cards()
    sounds = load_sounds()
    background = load_background()
    back_card = load_back_card()

    if background is None or back_card is None:
        print("Erro ao carregar os recursos essenciais. Encerrando o jogo.")
        pygame.quit()
        sys.exit()

    # Instanciar gerenciadores
    game_manager = GameManager()  # Gerenciador do jogo
    audio_manager = AudioManager()  # Gerenciador de áudio
    ui_manager = UIManager(screen, font)  # Gerenciador da UI

    # Estados iniciais
    player_hand = game_manager.state['player_hand']
    opponent_hand = game_manager.state['opponent_hand']
    vira_card = game_manager.state['vira_card']
    manilhas = game_manager.state['manilhas']

    # Música de fundo
    audio_manager.play_background_music()  # Utilizando SOUNDS_DIR internamente no AudioManager

    voce_venceu_image = pygame.image.load(os.path.join("images", "you-win.png")).convert_alpha()
    voce_perdeu_image = pygame.image.load(os.path.join("images", "you-lose.png")).convert_alpha()
    voce_perdeu_image = pygame.transform.scale(voce_perdeu_image, (600,400))

    # Variáveis de volume e botões de áudio
    volume = audio_manager.volume
    is_muted = audio_manager.is_muted

    button_width = 50
    button_height = 50
    padding = 10

    # Carregar ícones para os botões de áudio
    volume_up_icon = pygame.image.load(os.path.join("images", "volume_high_icon.png")).convert_alpha()
    volume_down_icon = pygame.image.load(os.path.join("images", "volume_low_icon.png")).convert_alpha()
    mute_icon = pygame.image.load(os.path.join("images", "mute_icon.png")).convert_alpha()

    # Redimensionar ícones
    volume_up_icon = pygame.transform.scale(volume_up_icon, (button_width, button_height))
    volume_down_icon = pygame.transform.scale(volume_down_icon, (button_width, button_height))
    mute_icon = pygame.transform.scale(mute_icon, (button_width, button_height))

    # Dimensões e posição do painel de pontuação
    panel_width = 180
    panel_height = 80
    panel_x = SCREEN_WIDTH - panel_width - 10
    panel_y = 10

    # Criar uma surface para o painel
    panel_surface = pygame.Surface((panel_width, panel_height))
    panel_surface.fill((160, 82, 45))  # marrom escuro
    # Se quiser transparência (ex. 200 de 255), descomente:
    panel_surface.set_alpha(100)

    screen.blit(panel_surface, (panel_x, panel_y))

    volume_up_button = pygame.Rect(
        SCREEN_WIDTH - button_width - padding, 
        SCREEN_HEIGHT - (3 * button_height) - (3 * padding),
        button_width,
        button_height
    )
    volume_down_button = pygame.Rect(
        SCREEN_WIDTH - button_width - padding,
        SCREEN_HEIGHT - (2 * button_height) - (2 * padding),
        button_width,
        button_height
    )
    mute_button = pygame.Rect(
        SCREEN_WIDTH - button_width - padding,
        SCREEN_HEIGHT - button_height - padding,
        button_width,
        button_height
    )

    # Botão de Truco
    truco_button_rect = pygame.Rect(10, SCREEN_HEIGHT // 2 - 20, 180, 40)

    # Área de jogo para arrastar as cartas
    play_area_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - CARD_WIDTH // 2,
        SCREEN_HEIGHT - 300,
        CARD_WIDTH,
        CARD_HEIGHT
    )

    # Variáveis de jogo
    dragging_card = None
    dragging_pos = None
    player_turn = False  # Oponente começa jogando
    opponent_turn = True
    played_cards = {'player': None, 'opponent': None}
    player_played_cards = []
    round_results = game_manager.round_results
    current_round = game_manager.current_round
    truco_requested = game_manager.truco_requested
    truco_accepted = game_manager.truco_accepted
    truco_message = ""
    current_truco_level = game_manager.current_truco_level
    opponent_always_accept_truco = game_manager.opponent_always_accept_truco

    # Pontos em caso de recusa de Truco
    points_on_refusal = {
        3: 1,
        6: 3,
        9: 6,
        12: 9
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Controles de volume
                if volume_up_button.collidepoint(pos):
                    audio_manager.adjust_volume(+0.1)
                    volume = audio_manager.volume
                    is_muted = audio_manager.is_muted
                elif volume_down_button.collidepoint(pos):
                    audio_manager.adjust_volume(-0.1)
                    volume = audio_manager.volume
                    is_muted = audio_manager.is_muted
                elif mute_button.collidepoint(pos):
                    audio_manager.mute()
                    is_muted = audio_manager.is_muted

                # Botão de Truco
                if truco_button_rect.collidepoint(pos):
                    if not truco_requested:
                        if current_truco_level < len(TRUCO_LEVELS)-1:
                            next_truco_level = current_truco_level + 1
                            requested_level = TRUCO_LEVELS[next_truco_level]
                            requested_value = TRUCO_VALUES[requested_level]

                            truco_requested = True
                            truco_message = f"Você pediu {requested_level.capitalize()}!"
                            print(f"Jogador pediu {requested_level.capitalize()}")

                            # Decisão do Oponente
                            if opponent_always_accept_truco:
                                truco_accepted = True
                                # Atualizar o bet_value no gerenciador do jogo
                                game_manager.bet_value = requested_value
                                print(f"Oponente aceitou o {requested_level.capitalize()}")
                                draw_text(screen, f"Oponente aceitou o {requested_level.capitalize()}!", font, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70))
                                pygame.display.flip()
                                time.sleep(1)
                                truco_requested = False
                                current_truco_level += 1
                                opponent_always_accept_truco = True
                            else:
                                # Oponente decide aleatoriamente
                                if random.choice([True, False]):
                                    truco_accepted = True
                                    game_manager.bet_value = requested_value
                                    print(f"Oponente aceitou o {requested_level.capitalize()}")
                                    draw_text(screen, f"Oponente aceitou o {requested_level.capitalize()}!", font, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70))
                                    pygame.display.flip()
                                    time.sleep(1)
                                    truco_requested = False
                                    current_truco_level += 1
                                    opponent_always_accept_truco = True
                                else:
                                    # Oponente recusou
                                    truco_accepted = False
                                    game_manager.player_score += points_on_refusal.get(requested_value, 1)
                                    print(f"Oponente recusou o {requested_level.capitalize()}")
                                    draw_text(screen, f"Oponente recusou o {requested_level.capitalize()}!", font, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70))
                                    pygame.display.flip()
                                    time.sleep(2)

                                    # Verificar pontuação
                                    if game_manager.player_score >= 12:
                                        screen.blit(voce_venceu_image, (SCREEN_WIDTH // 2 - voce_venceu_image.get_width() // 2,
                                        SCREEN_HEIGHT // 2 - voce_venceu_image.get_height() // 2))

                                        pygame.display.flip()
                                        pygame.mixer.music.stop()
                                        if 'winner-song' in sounds:
                                            if not is_muted:
                                                sounds['winner-song'].play()
                                        else:
                                            print("Erro: Música de vitória 'winner-song' não encontrada.")

                                        time.sleep(5)
                                        if 'winner-song' in sounds:
                                            sounds['winner-song'].stop()

                                        game_manager.reset_full_game()
                                        player_hand = game_manager.state['player_hand']
                                        opponent_hand = game_manager.state['opponent_hand']
                                        vira_card = game_manager.state['vira_card']
                                        manilhas = game_manager.state['manilhas']
                                        round_results = game_manager.round_results
                                        current_round = game_manager.current_round
                                        truco_requested = False
                                        truco_message = ""
                                        truco_accepted = False
                                        current_truco_level = -1
                                        player_played_cards = []
                                        opponent_always_accept_truco = False
                                        audio_manager.play_background_music()
                                        continue
                                    else:
                                        # Reiniciar partida sem zerar pontuação geral
                                        game_manager.reset_game()
                                        player_hand = game_manager.state['player_hand']
                                        opponent_hand = game_manager.state['opponent_hand']
                                        vira_card = game_manager.state['vira_card']
                                        manilhas = game_manager.state['manilhas']
                                        round_results = game_manager.round_results
                                        current_round = game_manager.current_round
                                        truco_requested = False
                                        truco_message = ""
                                        player_played_cards = []
                                        current_truco_level = -1
                                        opponent_always_accept_truco = False
                                        continue
                        else:
                            print("Truco já atingiu o nível máximo.")
                            draw_text(screen, "Truco Máximo!", font, BLACK, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 70))
                            pygame.display.flip()
                            time.sleep(1)
                    # Se truco já foi solicitado, não faz nada
                else:
                    # Clique nas cartas do jogador
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
                    if play_area_rect.collidepoint(pos):
                        played_cards['player'] = dragging_card
                        print(f"Jogador jogou a carta: {played_cards['player']}")
                        player_played_cards.append(dragging_card)
                        player_turn = False
                        opponent_turn = True
                    else:
                        # Retorna a carta para a mão do jogador
                        player_hand.append(dragging_card)
                    dragging_card = None
                    dragging_pos = None

        # Lógica do jogo
        if opponent_turn and played_cards['opponent'] is None:
            if opponent_hand:
                played_cards['opponent'] = opponent_hand.pop(0)
                print(f"Oponente jogou a carta: {played_cards['opponent']}")
                opponent_turn = False
                player_turn = True
            else:
                played_cards['opponent'] = None

        # Determinar vencedor da rodada usando get_card_value
        if played_cards['player'] and played_cards['opponent']:
            player_card_value = get_card_value(played_cards['player'], manilhas)
            opponent_card_value = get_card_value(played_cards['opponent'], manilhas)

            if player_card_value > opponent_card_value:
                round_results.append("Jogador")
                print("Jogador venceu esta rodada")
            elif player_card_value < opponent_card_value:
                round_results.append("Oponente")
                print("Oponente venceu esta rodada")
            else:
                round_results.append("Empate")
                print("Empate nesta rodada")

            played_cards['player'] = None
            played_cards['opponent'] = None
            opponent_turn = True
            player_turn = False
            current_round += 1
            game_manager.current_round = current_round

            # Verificar se a partida (de 3 rodadas) acabou
            if current_round > 3:
                player_rounds_won = round_results.count('Jogador')
                opponent_rounds_won = round_results.count('Oponente')

                # Usa o bet_value atual do game_manager
                if player_rounds_won > opponent_rounds_won:
                    game_manager.player_score += game_manager.bet_value
                elif opponent_rounds_won > player_rounds_won:
                    game_manager.opponent_score += game_manager.bet_value

                # Verifica se alguém chegou em 12 pontos:
                if game_manager.player_score >= 12:
                    screen.blit(voce_venceu_image, (SCREEN_WIDTH // 2 - voce_venceu_image.get_width() // 2, SCREEN_HEIGHT // 2 - voce_venceu_image.get_height() // 2))
                    pygame.display.flip()
                    pygame.mixer.music.stop()
                    if 'winner-song' in sounds:
                        if not is_muted:
                            sounds['winner-song'].play()
                    else:
                        print("Erro: Música de vitória 'winner-song' não encontrada.")

                    time.sleep(5)
                    if 'winner-song' in sounds:
                        sounds['winner-song'].stop()

                    game_manager.reset_full_game()
                    player_hand = game_manager.state['player_hand']
                    opponent_hand = game_manager.state['opponent_hand']
                    vira_card = game_manager.state['vira_card']
                    manilhas = game_manager.state['manilhas']
                    round_results = game_manager.round_results
                    current_round = game_manager.current_round

                    # Sincroniza o estado do truco após o reset
                    truco_requested = game_manager.truco_requested
                    truco_accepted = game_manager.truco_accepted
                    current_truco_level = game_manager.current_truco_level
                    opponent_always_accept_truco = game_manager.opponent_always_accept_truco
                    truco_message = ""

                    player_played_cards = []
                    played_cards = {'player': None, 'opponent': None}
                    audio_manager.play_background_music()
                    continue

                elif game_manager.opponent_score >= 12:
                    screen.blit(voce_perdeu_image, (SCREEN_WIDTH // 2 - voce_perdeu_image.get_width() // 2,  SCREEN_HEIGHT // 2 - voce_perdeu_image.get_height() // 2))

                    pygame.display.flip()
                    pygame.mixer.music.stop()
                    if not is_muted and 'looser-song' in sounds:
                        sounds['looser-song'].play()
                    time.sleep(5)
                    if 'looser-song' in sounds:
                        sounds['looser-song'].stop()

                    game_manager.reset_full_game()
                    player_hand = game_manager.state['player_hand']
                    opponent_hand = game_manager.state['opponent_hand']
                    vira_card = game_manager.state['vira_card']
                    manilhas = game_manager.state['manilhas']
                    round_results = game_manager.round_results
                    current_round = game_manager.current_round

                    truco_requested = game_manager.truco_requested
                    truco_accepted = game_manager.truco_accepted
                    current_truco_level = game_manager.current_truco_level
                    opponent_always_accept_truco = game_manager.opponent_always_accept_truco
                    truco_message = ""

                    player_played_cards = []
                    played_cards = {'player': None, 'opponent': None}
                    audio_manager.play_background_music()
                    continue
                else:
                    # Nenhum dos dois chegou a 12 pontos, então apenas reinicia a partida
                    game_manager.reset_game_state()
                    player_hand = game_manager.state['player_hand']
                    opponent_hand = game_manager.state['opponent_hand']
                    vira_card = game_manager.state['vira_card']
                    manilhas = game_manager.state['manilhas']
                    round_results = game_manager.round_results
                    current_round = game_manager.current_round

                    truco_requested = game_manager.truco_requested
                    truco_accepted = game_manager.truco_accepted
                    current_truco_level = game_manager.current_truco_level
                    opponent_always_accept_truco = game_manager.opponent_always_accept_truco
                    truco_message = ""

                    player_played_cards = []
                    played_cards = {'player': None, 'opponent': None}

                    continue

        # Desenhar a tela
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), play_area_rect, 3 , 5)

        # Desenhar as cartas do jogador
        for i, card in enumerate(player_hand):
            x = SCREEN_WIDTH // 2 - len(player_hand) * 50 + i * 100
            y = SCREEN_HEIGHT - 140
            card_key = card.lower()
            if card_key in cards:
                ui_manager.draw_card(cards[card_key], (x, y))
            else:
                print(f"Carta '{card_key}' não encontrada nas imagens.")

        # Desenhar Cartas do Oponente (viradas)
        for i, card in enumerate(opponent_hand):
            x = SCREEN_WIDTH // 2 - len(opponent_hand) * 50 + i * 100
            y = 20
            ui_manager.draw_card(back_card, (x, y))

        # Carta do oponente jogada
        if played_cards['opponent']:
            card_key = played_cards['opponent'].lower()
            if card_key in cards:
                x = SCREEN_WIDTH // 2 - 40
                y = 160
                ui_manager.draw_card(cards[card_key], (x, y))
            else:
                print(f"Carta '{card_key}' não encontrada nas imagens.")

        # Carta do jogador jogada
        if played_cards['player']:
            card_key = played_cards['player'].lower()
            if card_key in cards:
                play_card_position = (
                    play_area_rect.x + play_area_rect.width // 2 - CARD_WIDTH // 2,
                    play_area_rect.y + play_area_rect.height // 2 - CARD_HEIGHT // 2
                )
                ui_manager.draw_card(cards[card_key], play_card_position)
            else:
                print(f"Carta '{card_key}' não encontrada nas imagens.")

        # Cartas já jogadas pelo jogador (histórico)
        for i, card in enumerate(player_played_cards):
            card_key = card.lower()
            if card_key in cards:
                x = SCREEN_WIDTH // 2 - 40
                y = SCREEN_HEIGHT - 275 - i * 30
                ui_manager.draw_card(cards[card_key], (x, y))
            else:
                print(f"Carta '{card_key}' não encontrada nas imagens.")

        # Carta arrastada
        if dragging_card and dragging_pos:
            card_key = dragging_card.lower()
            if card_key in cards:
                ui_manager.draw_card(cards[card_key], (dragging_pos[0] - 40, dragging_pos[1] - 60))
            else:
                print(f"Carta '{card_key}' não encontrada nas imagens.")

        # Vira
        card_key = vira_card.lower()
        if card_key in cards:
            ui_manager.draw_card(cards[card_key], (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 - 60))
        else:
            print(f"Carta '{card_key}' não encontrada nas imagens.")

        # Desenhar painel de pontuação (após todas as cartas e componentes)
        screen.blit(panel_surface, (panel_x, panel_y))
        opponent_score_text = f"Oponente: {game_manager.opponent_score}"
        player_score_text = f"Jogador: {game_manager.player_score}"
        # Desenhar o texto do oponente em vermelho
        draw_text(screen, opponent_score_text, font, WHITE, (panel_x + 10, panel_y + 10))
        # Desenhar o texto do jogador em verde
        draw_text(screen, player_score_text, font, WHITE, (panel_x + 10, panel_y + 40))

        # Rodada Atual
        ui_manager.draw_text(f"Rodada: {current_round}", (10, 10), BLACK)

        # Resultados das Rodadas
        for i, result in enumerate(round_results):
            ui_manager.draw_text(f"Rodada {i+1}: {result}", (10, 40 + i * 30), BLACK)

        # Botão de Truco
        if current_truco_level < len(TRUCO_LEVELS)-1:
            next_request = TRUCO_LEVELS[current_truco_level +1]
            button_label = f"Pedir {next_request.capitalize()}"
        else:
            button_label = "Truco Máximo"
        ui_manager.draw_button(truco_button_rect, button_label, (0,128,0), WHITE)

        # Botões de volume (com ícones)
        pygame.draw.rect(screen, (0, 255, 0), volume_up_button, 0, 10)
        pygame.draw.rect(screen, (255, 255, 0), volume_down_button, 0, 10)
        pygame.draw.rect(screen, (255, 0, 0), mute_button, 0, 10)

        volume_up_icon_rect = volume_up_icon.get_rect(center=volume_up_button.center)
        volume_down_icon_rect = volume_down_icon.get_rect(center=volume_down_button.center)
        mute_icon_rect = mute_icon.get_rect(center=mute_button.center)

        screen.blit(volume_up_icon, volume_up_icon_rect)
        screen.blit(volume_down_icon, volume_down_icon_rect)
        screen.blit(mute_icon, mute_icon_rect)
        

        # Mensagem de Truco
        if truco_requested:
            ui_manager.draw_text(truco_message, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100), BLACK)
            if truco_accepted:
                ui_manager.draw_text("Oponente aceitou o Truco!", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70), BLACK)
            else:
                ui_manager.draw_text("Oponente recusou o Truco!", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 70), BLACK)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()