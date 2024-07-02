import pandas as pd
from Hand import Hand
from Player import Player

# Define custom order for card ranking
custom_order = {'3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8,
                'jack': 9, 'queen': 10, 'king': 11, 'ace': 12, '2': 13}


def get_score(card):
    return custom_order[card['Rank']]


def is_card_high(card):
    return card['Rank'] in ['ace', 'king', 'queen', 'jack']


class Bot(Player):
    def __init__(self, name, log_file='game_log.csv'):
        Player.__init__(self, name)
        self.game_log = pd.DataFrame(columns=['game_type', 'pile', 'hand', 'decision', 'result'])
        self.log_file = log_file
        self.load_game_log()

    def load_game_log(self):
        try:
            self.game_log = pd.read_csv(self.log_file)
        except FileNotFoundError:
            self.game_log = pd.DataFrame(columns=['game_type', 'pile', 'hand', 'decision', 'result'])

    def save_game_log(self):
        filtered_game_log = self.game_log[self.game_log['game_type'].notna()]
        filtered_game_log.to_csv(self.log_file, index=False)

    def log_game_state(self, pile, hand, decision, result):
        if pile.game_type is None:
            return  # Skip logging if game_type is None

        new_log = {
            'game_type': pile.game_type,
            'pile': pile.to_json(),
            'hand': hand.to_json(),
            'decision': decision,
            'result': result
        }
        new_log_df = pd.DataFrame([new_log])
        self.game_log = pd.concat([self.game_log, new_log_df], ignore_index=True)
        self.save_game_log()

    def choose_best_game_type(self, pile):
        playable_solos = self.get_playable_solos(pile)
        playable_pairs = self.get_playable_pairs(pile)
        pair_score = playable_pairs.calculate_score() / 2
        solo_score = playable_solos.calculate_score()
        if self.hand_size <= 8:
            pair_score += 2
        for index, card in playable_pairs.iterrows():
            if is_card_high(card):
                pair_score += .5
        if pair_score > solo_score:
            print("Bot chooses pair")
        return 'pair' if pair_score > solo_score else 'solo'

    def get_card(self, rank):
        for index, card in self.hand.iterrows():
            if card['Rank'] == rank:
                return card

    def get_best_playable_solo(self, pile):
        cards_to_play = Hand()
        playable_cards = self.get_playable_cards(pile)
        playable_solos = self.get_playable_solos(pile)
        if playable_cards.empty:
            print("Lost: No card to play")
            return None
        elif self.hand_size == 1:
            cards_to_play.add_card(playable_cards.iloc[0])
        elif self.hand_size > 1 and self.hand_size - 1 == self.has_n_rank("2"):
            cards_to_play.add_card(self.get_card("2"))
        elif get_score(self.hand.iloc[0]) < self.hand.calculate_score() / self.hand_size / 9:
            cards_to_play.add_card(playable_cards.iloc[-1])
        elif pile.shape[0] != 0 and self.has_n_rank(pile.iloc[-1]) >= 2:
            print("-----" + self.name + " breaks his pair to go or_nothing-----")
            cards_to_play.add_card(playable_cards.iloc[0])
        elif playable_solos.empty:
            print(self.name + " has to break a pair to play")
            if (self.hand_size <= 4 or not is_card_high(playable_cards.iloc[0])
                    or pile.shape[0] > 0 and self.has_n_rank(pile.iloc[-1]) == 3):
                print("--He breaks the pair--")
                cards_to_play.add_card(playable_cards.iloc[0])
            else:
                print("Bot's hand :")
                self.log()
                return None
        elif playable_solos.shape[0] < playable_cards.shape[0] / 2:
            cards_to_play.add_card(playable_cards.iloc[0])
        else:
            cards_to_play.add_card(playable_solos.iloc[0])
        return cards_to_play

    def get_best_playable_pair(self, pile):
        cards_to_play = Hand()
        playable_pairs = self.get_playable_pairs(pile)
        if playable_pairs.shape[0] < 2:
            print("No pair to play")
            return None
        cards_to_play.add_card(playable_pairs.iloc[0])
        cards_to_play.add_card(playable_pairs.iloc[1])
        return cards_to_play

    def choose_cards_to_play(self, pile, passed, next_player):
        cards_to_play = Hand()
        game_type = pile.game_type
        if game_type == "":
            game_type = self.choose_best_game_type(pile)
        if game_type == 'solo':
            if pile.is_card_or_nothing() and self.has_n_rank(pile.iloc[-1]) == 0 and not passed:
                return None
            cards_to_play = self.get_best_playable_solo(pile)
        elif game_type == 'pair':
            cards_to_play = self.get_best_playable_pair(pile)

        if cards_to_play is None or cards_to_play.empty:
            return cards_to_play
        self.log_game_state(pile, self.hand, cards_to_play.to_json() if cards_to_play is not None else None,
                            'win' if self.hand.shape[0] - cards_to_play.shape[0] == 0 else 'loss' if (next_player.can_play(pile) and next_player.hand_size == 1) else 'pass')

        return cards_to_play
