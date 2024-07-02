import pandas as pd

from Hand import Hand


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.solos_won = 0
        self.pairs_won = 0
        self.solos_started = 0
        self.pairs_started = 0
        self.solos_started_won = 0
        self.pairs_started_won = 0
        self.started_hands_won = 0
        self.has_started = False

    @property
    def hand_size(self):
        return self.hand.shape[0]

    def count_round_win(self, pile):
        if self.has_started:
            self.started_hands_won += 1
            if pile.game_type == 'solo':
                self.solos_started_won += 1
            elif pile.game_type == 'pair':
                self.pairs_started_won += 1
        if pile.game_type == 'solo':
            self.solos_won += 1
        elif pile.game_type == 'pair':
            self.pairs_won += 1

    def has_n_rank(self, card):
        count = 0
        if isinstance(card, str):
            for index, c in self.hand.iterrows():
                if c['Rank'] == "2":
                    count += 1
        else:
            for index, c in self.hand.iterrows():
                if c['Rank'] == card['Rank']:
                    count += 1
        return count

    def add_card(self, card):
        self.hand.add_card(card)

    def remove_card(self, played_card):
        for index, card in self.hand.iterrows():
            if played_card['Rank'] == card['Rank'] and played_card['Suit'] == card['Suit']:
                self.hand.drop(index, inplace=True)

    def log(self):
        print(f"{self.name}")
        print(self.hand.log())

    def can_play(self, pile):
        for index, card in self.hand.iterrows():
            if pile.card_is_playable(card):
                return True
        return False

    def get_playable_cards(self, pile):
        playable_cards = Hand()  # Assuming Hand is a class for holding cards
        for index, card in self.hand.iterrows():
            if pile.card_is_playable(card):  # Assuming card_is_playable is a method in the pile class
                playable_cards.add_card(card)
        return playable_cards

    def get_playable_solos(self, pile):
        playable_solos = Hand()
        card_counts = self.hand['Rank'].value_counts()  # Count the occurrences of each rank

        for index, card in self.hand.iterrows():
            if pile.card_is_playable(card) and card_counts[card['Rank']] == 1:
                playable_solos.add_card(card)

        return playable_solos

    def get_playable_pairs(self, pile):
        playable_pairs = Hand()
        playable_cards = []

        # Collect all playable cards
        for index, card in self.hand.iterrows():
            if pile.card_is_playable(card):
                playable_cards.append(card)

        # Find pairs in the collected playable cards
        i = 0
        while i < len(playable_cards) - 1:
            card1 = playable_cards[i]
            card2 = playable_cards[i + 1]
            if card1['Rank'] == card2['Rank']:  # Assuming 'rank' is a column in your DataFrame
                playable_pairs.add_card(card1)
                playable_pairs.add_card(card2)
                i += 2  # Move to the next pair
            else:
                i += 1

        if playable_pairs.shape[0] % 2 != 0:
            print("Error: Odd number of cards in playable pairs")
        return playable_pairs

    def choose_best_game_type(self, pile):
        return 'solo'

    def get_best_playable_solo(self, pile):
        playable_solos = self.get_playable_cards(pile)
        if playable_solos.empty:
            print("Lost: No card to play")
            return None
        cards_to_play = Hand()
        cards_to_play.add_card(playable_solos.iloc[0])
        return cards_to_play

    def get_best_playable_pair(self, pile):
        playable_pairs = self.get_playable_pairs(pile)
        if playable_pairs.shape[0] < 2:
            print("Lost: No pair to play")
            return None
        cards_to_play = Hand()
        cards_to_play.add_card(playable_pairs.iloc[0])
        cards_to_play.add_card(playable_pairs.iloc[1])
        return cards_to_play

    def can_cut(self, pile):
        pile_size = pile.shape[0]
        if pile_size == 0:
            return False
        if pile_size > 2 and pile.iloc[-1]['Rank'] == pile.iloc[-2]['Rank'] == pile.iloc[-3]['Rank']:
            return self.has_n_rank(pile.iloc[-1]) == 1
        elif pile_size > 1 and pile.iloc[-1]['Rank'] == pile.iloc[-2]['Rank']:
            return self.has_n_rank(pile.iloc[-1]) == 2
        return self.has_n_rank(pile.iloc[-1]) == 3

    def cut(self, pile):
        cards_to_play = Hand()
        for index, card in self.hand.iterrows():
            if card['Rank'] == pile.iloc[-1]['Rank']:
                cards_to_play.add_card(card)
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
        return cards_to_play
