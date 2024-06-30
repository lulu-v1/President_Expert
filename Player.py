import pandas as pd
from Hand import Hand

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def add_card(self, card):
        self.hand.add_card(card)

    def remove_card(self, playedCard):
        for index, card in self.hand.cards.iterrows():
            if playedCard['Rank'] == card['Rank'] and playedCard['Suit'] == card['Suit']:
                self.hand.drop(index, inplace=True)

    def log(self):
        print(f"{self.name}")
        print(self.hand.log())

    def get_playable_cards(self, pile):
        playable_cards = Hand()
        for index, card in self.hand.cards.iterrows():
            if pile.card_is_playable(card):
                playable_cards.add_card(card)
        return playable_cards
