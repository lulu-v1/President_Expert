import pandas as pd

from Hand import Hand


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def add_card(self, card):
        self.hand.add_card(card)

    def remove_card(self, playedCard):
        for index, card in self.hand.iterrows():
            if playedCard['Rank'] == card['Rank'] and playedCard['Suit'] == card['Suit']:
                self.hand.drop(index, inplace=True)

    def log(self):
        print(f"{self.name}")
        print(self.hand.log())

    def get_playable_cards(self, pile):
        playable_cards = Hand()  # Assuming Hand is a class for holding cards
        for index, card in self.hand.iterrows():
            if pile.card_is_playable(card):  # Assuming card_is_playable is a method in the pile class
                playable_cards.add_card(card)
        return playable_cards
