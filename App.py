import tkinter as tk
from PIL import ImageTk
from Deck import Deck
from display_card import draw_card_path, resize_card_image
from interface_background import load_and_resize_background
from event_handlers import on_card_click
from interface_display_cards import display_cards

from Bot import Bot
from Deck import Deck as Deck
from Pile import Pile
from Player import Player


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('President Expert')
        self.geometry("1024x768")  # Tamaño de la ventana

        self.deck = Deck()
        self.player = Player('You')
        self.bot = Bot('Bot')
        self.pile = Pile()

        self.canvas_width = 1024
        self.canvas_height = 768
    def distribute(self):
        self.deck = Deck()
        self.deck.shuffle()
        # Distribute 16 cards to each player
        for _ in range(16):
            self.player.add_card(self.deck.draw_card())
            self.bot.add_card(self.deck.draw_card())
        # Order cards in the players hands
        self.player.hand.order()
        self.bot.hand.order()

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
    def choose_first_player(self):
        # the one with the queen of hearts starts
        # if no one has it, the player starts
        for _, card in self.player.hand.iterrows():
            if card['Rank'] == 'queen' and card['Suit'] == 'hearts':
                print("You have the Queen of hearts, you start")
                return "p"
        for _, card in self.bot.hand.iterrows():
            if card['Rank'] == 'queen' and card['Suit'] == 'hearts':
                print("Bot has the Queen of hearts, he starts")
                return "b"
        print("No one has the Queen of hearts, you start")
        return "p"

        # Load and resize the table image
        self.table_photo, self.table_width, self.table_height = load_and_resize_background('./design/bj_background.png',
                                                                                           self.canvas_width,
                                                                                           self.canvas_height)
    def play_card(self, player, card):
        if self.pile.card_is_playable(card):
            print(f"{player.name} played {card['Rank']} of {card['Suit']}")
            # Remove the card from player's hand
            player.remove_card(card)
            self.pile.add_card(card)
        else:
            print(f"{player.name} cannot play {card['Rank']} of {card['Suit']}")
        return

        self.canvas.create_image((self.canvas_width - self.table_width) // 2,
                                 (self.canvas_height - self.table_height) // 2, anchor=tk.NW, image=self.table_photo)
    def start_game(self):
        self.distribute()
        turn = self.choose_first_player()
        # turn = "p"
        while True:
            if turn == "p":
                if self.player.get_playable_cards(self.pile).empty:
                    print("Player cannot play, Bot wins this hand")
                    turn = "b"
                    self.pile.reset()
                    continue
                else:
                    card_to_play = self.player.get_playable_cards(self.pile).iloc[0]
                    self.play_card(self.player, card_to_play)
                if self.bot.get_playable_cards(self.pile).empty:
                    print("Bot cannot play, You win this hand")
                    self.pile.reset()
                else:
                    card_to_play = self.bot.choose_card_to_play(self.pile)
                    self.play_card(self.bot, card_to_play)
            else:
                if self.bot.get_playable_cards(self.pile).empty:
                    print("Bot cannot play, You win this hand")
                    self.pile.reset()
                    turn = "p"
                    continue
                else:
                    card_to_play = self.bot.choose_card_to_play(self.pile)
                    self.play_card(self.bot,card_to_play)
                if self.player.get_playable_cards(self.pile).empty:
                    print("Player cannot play, Bot wins this hand")
                    self.pile.reset()
                else:
                    card_to_play = self.player.get_playable_cards(self.pile).iloc[0]
                    self.play_card(self.player, card_to_play)

        self.selected_card_labels = []  # Para mantener un seguimiento de las cartas seleccionadas
        display_cards(self.canvas, self.deck, self.selected_card_labels, on_card_click)
    def run(self):
        self.mainloop()
            if self.player.hand.empty or self.bot.hand.empty:
                print("Game over")
                if self.player.hand.empty:
                    print("------You win------")
                else:
                    print("------Bot wins------")
                self.player.log()
                self.bot.log()
                break


app = App()
app.start_game()
# app.distribute()
# app.player.log()
# print(app.player.hand.iloc[1]['Rank'])
# print(app.player.get_playable_cards(app.pile))
app.run()
