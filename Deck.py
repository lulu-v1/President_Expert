import pandas as pd


class Deck(pd.DataFrame):
    def __init__(self):
        # Generate the deck as a DataFrame with 'Rank' and 'Suit' columns
        cards = [(rank, suit) for suit in ['hearts', 'diamonds', 'clubs', 'spades']
                 for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']]
        pd.DataFrame.__init__(self, cards, columns=['Rank', 'Suit'])

    @property
    def is_empty(self):
        return self.empty

    def draw_card(self):
        if self.is_empty:
            return "No more cards in the deck"
        card = self.iloc[0]
        self.drop(self.index[0], inplace=True)
        self.reset_index(drop=True, inplace=True)
        return card

    def draw_cards(self, num_cards):
        drawn_cards = []
        for _ in range(num_cards):
            card = self.draw_card()
            drawn_cards.append(card)
        return pd.DataFrame(drawn_cards)

    def display(self):
        print(self)
        return
