import pandas as pd


class Deck:
    def __init__(self):
        self.suits = ['hearts', 'diamonds', 'clubs', 'spades']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        self.deck = pd.DataFrame([(rank, suit) for suit in self.suits for rank in self.ranks], columns=['Rank', 'Suit'])
        self.deck = self.deck.sample(frac=1).reset_index(drop=True)
    @property
    def empty(self):
        return self.deck.empty

    def draw_card(self):
        if self.empty:
            return "No more cards in the deck"
        card = self.deck.iloc[0]
        self.deck = self.deck.iloc[1:].reset_index(drop=True)
        return card

    def draw_cards(self, num_cards):
        drawn_cards = []
        for _ in range(num_cards):
            card = self.draw_card()
            drawn_cards.append(card)
        return pd.DataFrame(drawn_cards)

    def display(self):
        print(self.deck)
        return
