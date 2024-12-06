from game_logic import reset_game, get_card_value, TRUCO_LEVELS, TRUCO_VALUES

class GameManager:
    def __init__(self):
        self.player_score = 0
        self.opponent_score = 0
        self.current_truco_level = -1
        self.bet_value = 1
        self.truco_requested = False
        self.truco_accepted = False
        self.opponent_always_accept_truco = False
        self.reset_game_state()  # Define o estado inicial da partida

    def reset_game_state(self):
        """
        Reinicia a partida de 3 rodadas (mãos, deck, vira, manilhas, etc.), mantendo a pontuação atual.
        """
        self.state = reset_game()  # Função que cria um novo estado para o baralho e mãos
        self.state['played_cards'] = {'player': None, 'opponent': None}
        self.round_results = []
        self.current_round = 1
        self.truco_requested = False
        self.truco_accepted = False
        self.current_truco_level = -1
        self.bet_value = 1

    def reset_full_game(self):
        """
        Reinicia o jogo completamente, zerando pontuações e estado da partida.
        """
        self.player_score = 0
        self.opponent_score = 0
        self.opponent_always_accept_truco = False
        self.reset_game_state()

    def reset_game(self):
        """
        Se for realmente necessário manter este método, podemos apenas chamá-lo para resetar o estado da partida.
        Caso contrário, pode removê-lo se não houver necessidade.
        """
        self.reset_game_state()

    def play_round(self, player_card, opponent_card, manilhas):
        player_value = get_card_value(player_card, manilhas)
        opponent_value = get_card_value(opponent_card, manilhas)
        if player_value > opponent_value:
            self.round_results.append("Jogador")
            return "Jogador"
        elif player_value < opponent_value:
            self.round_results.append("Oponente")
            return "Oponente"
        else:
            self.round_results.append("Empate")
            return "Empate"
