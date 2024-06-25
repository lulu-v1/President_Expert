import pandas as pd


class Hand(pd.DataFrame):
    def __init__(self):
        pd.DataFrame.__init__(self, columns=['Rank', 'Suit'])

    @property
    def is_empty(self):
        return self.empty

    def order(self):
        # Define custom order for ranks
        custom_order = {'3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8,
                        'jack': 9, 'queen': 10, 'king': 11, 'ace': 12, '2': 13}
        # Apply custom sorting order
        self['Rank'] = pd.Categorical(self['Rank'], categories=custom_order.keys(), ordered=True)
        self.sort_values(by='Rank', inplace=True)
        return

    def add_card(self, card):
        self.loc[len(self)] = card

    def log(self):
        print(self.to_string(index=False))
