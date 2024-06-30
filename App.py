import tkinter as tk
from PIL import Image, ImageTk

from Bot import Bot
from Deck import Deck
from Pile import Pile
from Player import Player
from interface_background import load_and_resize_background
from interface_display_cards import display_cards, display_bot_cards


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
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Load and resize the table image
        self.table_photo, self.table_width, self.table_height = load_and_resize_background(
            './design/bj_background.png', self.canvas_width, self.canvas_height)

        self.canvas.create_image((self.canvas_width - self.table_width) // 2,
                                 (self.canvas_height - self.table_height) // 2, anchor=tk.NW, image=self.table_photo)

        self.selected_card_labels = []  # Para mantener un seguimiento de las cartas seleccionadas
        display_cards(self.canvas, self.deck, self.selected_card_labels, self.on_card_click)
        display_bot_cards(self.canvas, self.deck)

        # Posición estimada del mazo (centrado en la parte inferior del canvas)
        mazo_x = self.canvas_width / 2
        mazo_y = self.canvas_height - 100  # 100 píxeles por encima del borde inferior

        # Agregar botón de "Jugar" por encima del mazo
        self.play_button = tk.Button(self.canvas, text="Jugar", command=self.play_selected_cards)
        self.play_button.place(x=mazo_x - 40, y=mazo_y - 60)  #

    def on_card_click(self, event, card_label, selected_card_labels, max_select=2):
        card_detail = card_label.card_detail  # Assuming card labels have card detail attribute
        # Count how many cards of the same rank are selected
        count_same_rank = sum(1 for lbl in selected_card_labels if lbl.card_detail['Rank'] == card_detail['Rank'])
        if card_label in selected_card_labels:
            selected_card_labels.remove(card_label)
            card_label.config(relief="raised")  # Deselect
        elif len(selected_card_labels) < max_select and count_same_rank < 2:
            selected_card_labels.append(card_label)
            card_label.config(relief="sunken")  # Select

    def play_selected_cards(self):
        if not self.selected_card_labels:
            print("No cards selected.")
            return
        last_card = self.pile.iloc[-1] if not self.pile.empty else None
        for label in self.selected_card_labels:
            card = label.card_detail
            if last_card is None or self.pile.card_is_playable(card):
                self.pile.add_card(card)
                self.player.remove_card(card)
                label.place_forget()  # Remove card from canvas
                print(f"Played {card['Rank']} of {card['Suit']}")
            else:
                print(f"Cannot play {card['Rank']} of {card['Suit']}")
        self.selected_card_labels.clear()
        self.update_pile_display()  # Redraw the pile


    def choose_first_player(self):
        # El jugador con la reina de corazones empieza
        for _, card in self.player.hand.cards.iterrows():
            if card['Rank'] == 'queen' and card['Suit'] == 'hearts':
                print("You have the Queen of hearts, you start")
                return "p"
        for _, card in self.bot.hand.cards.iterrows():
            if card['Rank'] == 'queen' and card['Suit'] == 'hearts':
                print("Bot has the Queen of hearts, he starts")
                return "b"
        print("No one has the Queen of hearts, you start")
        return "p"

    def update_pile_display(self):
        self.canvas.delete("pile")  # Limpiar las cartas anteriores
        player_card, bot_card = self.pile.get_last_cards()

        pile_x, pile_y = self.canvas_width // 2, self.canvas_height // 2

        # Mostrar la última carta del jugador
        if player_card:
            player_card_image = Image.open(f"cards/{player_card['Rank']}_of_{player_card['Suit']}.png")
            player_card_image = player_card_image.resize((58, 83), Image.Resampling.LANCZOS)
            player_card_tk_image = ImageTk.PhotoImage(player_card_image)
            self.canvas.create_image(pile_x - 30, pile_y, image=player_card_tk_image, anchor="center", tags="pile")

        # Mostrar la última carta del bot
        if bot_card:
            bot_card_image = Image.open(f"cards/{bot_card['Rank']}_of_{bot_card['Suit']}.png")
            bot_card_image = bot_card_image.resize((58, 83), Image.Resampling.LANCZOS)
            bot_card_tk_image = ImageTk.PhotoImage(bot_card_image)
            self.canvas.create_image(pile_x + 30, pile_y, image=bot_card_tk_image, anchor="center", tags="pile")

        # Mantener referencias para evitar la recolección de basura
        self.canvas.images.extend([player_card_tk_image, bot_card_tk_image])

    def play_card(self, player, card):
        # Jugar la carta y actualizar la pila
        self.pile.update_cards(player.last_played_card, self.bot.last_played_card)
        self.update_pile_display()

    def display_pile_card(self, card, x, y, index):
        card_image_path = f"cards/{card['Rank']}_of_{card['Suit']}.png"
        pil_image = Image.open(card_image_path)
        pil_image = pil_image.resize((58, 83), Image.ANTIALIAS)  # Resizing the card image
        tk_image = ImageTk.PhotoImage(pil_image)

        # Create a canvas image object
        image_id = self.canvas.create_image(x + index * 2, y, image=tk_image, anchor=tk.CENTER, tags="pile")
        self.canvas.image = tk_image  # Keep a reference to avoid garbage collection

    def distribute(self):
        self.deck.shuffle()
        # Distribute 16 cards to each player
        for _ in range(16):
            self.player.add_card(self.deck.draw_card())
            self.bot.add_card(self.deck.draw_card())
        # Order cards in the players hands
        self.player.hand.order()
        self.bot.hand.order()

    def start_game(self):
        self.distribute()
        turn = self.choose_first_player()
        while True:
            if turn == "p":
                if self.player.get_playable_cards(self.pile).is_empty:
                    print("Player cannot play, Bot wins this hand")
                    turn = "b"
                    self.pile.reset()
                    continue
                else:
                    card_to_play = self.player.get_playable_cards(self.pile).iloc[0]
                    self.play_card(self.player, card_to_play)
                if self.bot.get_playable_cards(self.pile).is_empty:
                    print("Bot cannot play, You win this hand")
                    self.pile.reset()
                else:
                    card_to_play = self.bot.choose_card_to_play(self.pile)
                    self.play_card(self.bot, card_to_play)
            else:
                if self.bot.get_playable_cards(self.pile).is_empty:
                    print("Bot cannot play, You win this hand")
                    self.pile.reset()
                    turn = "p"
                    continue
                else:
                    card_to_play = self.bot.choose_card_to_play(self.pile)
                    self.play_card(self.bot, card_to_play)
                if self.player.get_playable_cards(self.pile).is_empty:
                    print("Player cannot play, Bot wins this hand")
                    self.pile.reset()
                else:
                    card_to_play = self.player.get_playable_cards(self.pile).iloc[0]
                    self.play_card(self.player, card_to_play)

    def run(self):
        self.mainloop()


app = App()
app.run()
