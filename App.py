import tkinter as tk
from PIL import ImageTk
from Deck import Deck
from display_card import draw_card_path, resize_card_image
from interface_background import load_and_resize_background
from event_handlers import on_card_click
from interface_display_cards import display_cards

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('President Expert')
        self.geometry("1024x768")  # Tamaño de la ventana

        self.deck = Deck()

        self.canvas_width = 1024
        self.canvas_height = 768

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Load and resize the table image
        self.table_photo, self.table_width, self.table_height = load_and_resize_background('./design/bj_background.png',
                                                                                           self.canvas_width,
                                                                                           self.canvas_height)

        self.canvas.create_image((self.canvas_width - self.table_width) // 2,
                                 (self.canvas_height - self.table_height) // 2, anchor=tk.NW, image=self.table_photo)

        self.selected_card_labels = []  # Para mantener un seguimiento de las cartas seleccionadas
        display_cards(self.canvas, self.deck, self.selected_card_labels, on_card_click)
    def run(self):
        self.mainloop()


app = App()
app.run()
