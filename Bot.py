import pandas as pd
from colorama import Fore

from Hand import Hand
from Player import Player

custom_order = {'3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8,
                'jack': 9, 'queen': 10, 'king': 11, 'ace': 12, '2': 13}


def get_score(card):
    return custom_order[card['Rank']]


class Bot(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def choose_best_game_type(self, pile):
        playable_cards = self.get_playable_cards(pile)
        playable_solos = self.get_playable_solos(pile)
        playable_pairs = self.get_playable_pairs(pile)
        pair_score = playable_pairs.calculate_score() / 2
        solo_score = playable_solos.calculate_score()
        if self.hand_size <= 8:
            pair_score += 2
        for index, card in playable_pairs.iterrows():
            if self.is_card_high(card):
                pair_score += .5
        print(Fore.GREEN + "Hand:\n" + self.hand.to_string(index=False))
        print(Fore.CYAN + "Solos:\n" + playable_solos.to_string(index=False))
        print(Fore.BLUE + 'Pairs:\n' + playable_pairs.to_string(index=False))
        print(Fore.RED + "Pair score: ", pair_score, " vs solo score: ", solo_score)
        print(Fore.RESET)
        if pair_score > solo_score:
            print("Bot chooses pair")
        return 'pair' if pair_score > solo_score else 'solo'

    def is_card_high(self, card):
        if card['Rank'] == 'ace' or card['Rank'] == 'king' or card['Rank'] == 'queen' or card['Rank'] == 'jack':
            return True
        return False

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
            # Breaking a pair to create an or_nothing situation, cause he can cut if the player completes the three of a kind
            cards_to_play.add_card(playable_cards.iloc[0])
        elif playable_solos.empty:
            print(self.name + " has to break a pair to play")
            if (self.hand_size <= 4 or not self.is_card_high(playable_cards.iloc[0])
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

    def choose_cards_to_play(self, pile, passed):
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
