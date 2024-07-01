import pandas as pd


class Pile(pd.DataFrame):
    def __init__(self):
        pd.DataFrame.__init__(self, columns=['Rank', 'Suit'])
        self.game_type = ""


    def add_card(self, card):
        self.loc[len(self)] = card

    def card_is_playable(self, card):
        custom_order = {'3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8,
                        'jack': 9, 'queen': 10, 'king': 11, 'ace': 12, '2': 13}
        if self.empty:
            return True
        return custom_order[card['Rank']] >= custom_order[self.iloc[-1]['Rank']]

    def log(self):
        return self.to_string(index=False)

    def is_card_or_nothing(self):
        if self.game_type == "pair":
            return False
        if self.shape[0] == 2 and self.iloc[-1]['Rank'] == self.iloc[-2]['Rank'] or self.shape[0] > 2 and self.iloc[-1][
            'Rank'] == self.iloc[-2]['Rank'] != self.iloc[-3]['Rank']:
            return True
        return False

    def reset(self):
        print("Pile reset")
        self.game_type = ""
        self.drop(self.index, inplace=True)
        return
