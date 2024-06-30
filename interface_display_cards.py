from PIL import ImageTk, Image
import tkinter as tk
from display_card import draw_card_path, resize_card_image

from PIL import ImageTk, Image
import tkinter as tk
from display_card import draw_card_path, resize_card_image

def display_cards(canvas, deck, selected_card_labels, on_card_click):
    card_data = draw_card_path(deck)  # Ahora recibe una lista de diccionarios con detalles completos
    card_width, card_height = 58, 83  # Tamaño reducido de la carta

    canvas_width = 1024
    spacing = 5  # Espacio pequeño entre las cartas
    total_width = (card_width + spacing) * 16 - spacing
    start_x = (canvas_width - total_width) // 2  # Centrar las cartas

    for i, details in enumerate(card_data):
        pil_image = resize_card_image(details['card_path'], card_width, card_height)
        tk_image = ImageTk.PhotoImage(pil_image)

        # Create a label widget to display the image
        image_label = tk.Label(canvas.master, image=tk_image, borderwidth=2, relief="raised")
        image_label.image = tk_image  # Guarda una referencia a la imagen para evitar su recolección de basura
        image_label.card_detail = {'Rank': details['Rank'], 'Suit': details['Suit']}  # Almacenar detalles de la carta

        x_position = start_x + (i * (card_width + spacing))
        y_position = 768 - card_height - 40  # Posicionar en la parte inferior

        image_label.place(x=x_position, y=y_position)
        image_label.bind("<Button-1>", lambda event, lbl=image_label: on_card_click(event, lbl, selected_card_labels))
def display_bot_cards(canvas, deck):
    card_data = draw_card_path(deck)  # Asumiendo que devuelve una lista de diccionarios con 'card_path', 'Rank', 'Suit'
    card_width, card_height = 58, 83  # Tamaño reducido de la carta

    canvas_width = 1024
    spacing = 5  # Espacio pequeño entre las cartas
    total_width = (card_width + spacing) * 16 - spacing
    start_x = (canvas_width - total_width) // 2  # Centrar las cartas

    for i, details in enumerate(card_data):
        pil_image = resize_card_image(details['card_path'], card_width, card_height)  # Usa 'card_path' correctamente
        tk_image = ImageTk.PhotoImage(pil_image)

        x_position = start_x + (i * (card_width + spacing))
        y_position = 20  # Posicionar en la parte superior

        # Create a label widget to display the image
        image_label = tk.Label(canvas.master, image=tk_image, borderwidth=2, relief="raised")
        image_label.image = tk_image  # Guarda una referencia para evitar la recolección de basura
        image_label.place(x=x_position, y=y_position)




"""
def display_bot_cards(canvas):
    card_width, card_height = 58, 83  # Tamaño reducido de la carta
    card_back_image_path = 'Back_card/back_card.png'
    pil_image = Image.open(card_back_image_path)
    pil_image = pil_image.resize((card_width, card_height), Image.LANCZOS)

    tk_image = ImageTk.PhotoImage(pil_image)

    canvas_width = 1024
    spacing = 5  # Espacio pequeño entre las cartas
    total_width = (card_width + spacing) * 16 - spacing
    start_x = (canvas_width - total_width) // 2  # Centrar las cartas

    for i in range(16):
        x_position = start_x + (i * (card_width + spacing))
        y_position = 20  # Posicionar en la parte superior

        # Create a label widget to display the image
        image_label = tk.Label(canvas.master, image=tk_image, borderwidth=2, relief="raised")
        image_label.image = tk_image
        image_label.original_y = y_position  # Store the original y position
        image_label.place(x=x_position, y=y_position)
"""