import tkinter as tk
from PIL import Image, ImageTk
from Deck import Deck as Deck

suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.deck = Deck()

    def draw_card_path(self):
        drawn_cards, self.deck = self.deck.draw_cards(1)
        card = drawn_cards.iloc[0]
        rank = card['Rank']
        suit = card['Suit']
        image_path = f"cards/{rank}_of_{suit}.png"
        return image_path

    def display_card(self):
        # Load the image using PIL
        pil_image = Image.open(self.draw_card_path())

        # Convert the PIL image to a format that Tkinter can display
        tk_image = ImageTk.PhotoImage(pil_image)

        # Create a label widget to display the image
        image_label = tk.Label(self, image=tk_image)
        image_label.pack()

    def run(self):
        self.draw_card_path()


app = App()
app.mainloop()
app.deck.display()
