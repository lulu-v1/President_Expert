from PIL import ImageTk
import tkinter as tk
from display_card import draw_card_path, resize_card_image

def display_cards(canvas, deck, selected_card_labels, on_card_click):
    card_paths = draw_card_path(deck)
    card_width, card_height = 58, 83  # Tamaño reducido de la carta

    canvas_width = 1024
    spacing = 5  # Espacio pequeño entre las cartas
    total_width = (card_width + spacing) * 16 - spacing
    start_x = (canvas_width - total_width) // 2  # Centrar las cartas

    for i, card_path in enumerate(card_paths):
        pil_image = resize_card_image(card_path, card_width, card_height)

        # Convert the PIL image to a format that Tkinter can display
        tk_image = ImageTk.PhotoImage(pil_image)

        x_position = start_x + (i * (card_width + spacing))
        y_position = 768 - card_height - 40  # Posicionar en la parte inferior

        # Create a label widget to display the image
        image_label = tk.Label(canvas.master, image=tk_image, borderwidth=2, relief="raised")
        image_label.image = tk_image
        image_label.original_y = y_position  # Store the original y position
        image_label.place(x=x_position, y=y_position)
        image_label.bind("<Button-1>", lambda event, lbl=image_label: on_card_click(event, lbl, selected_card_labels))
