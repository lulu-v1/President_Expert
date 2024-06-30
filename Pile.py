import pandas as pd

class Pile(pd.DataFrame):
    def __init__(self):
        # Inicializar como DataFrame vacío con columnas 'Rank' y 'Suit'
        super().__init__(columns=['Rank', 'Suit'])

    def add_card(self, card):
        # Agregar una carta como una nueva fila al DataFrame
        self.loc[len(self)] = card

    def card_is_playable(self, card):
        # Determinar si una carta es jugable comparándola con la última carta de la pila
        custom_order = {'3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8,
                        'jack': 9, 'queen': 10, 'king': 11, 'ace': 12, '2': 13}
        if self.empty:
            return True  # Si la pila está vacía, cualquier carta es jugable
        return custom_order[card['Rank']] >= custom_order[self.iloc[-1]['Rank']]

    def reset(self):
        # Limpiar la pila completamente
        self.drop(self.index, inplace=True)