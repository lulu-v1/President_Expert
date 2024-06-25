from Player import Player


class Bot(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def choose_card_to_play(self, pile):
        playable_cards = self.get_playable_cards(pile)
        return playable_cards.iloc[0] if not playable_cards.empty else None
