from Deck import Deck
from PIL import Image
import pandas as pd

suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

def draw_card_path(deck):
    drawn_cards = deck.draw_cards(16)
    drawn_cards = drawn_cards.sort_values(by='Rank', key=lambda x: x.map(lambda rank: ranks.index(rank)))  # Ordenar cartas
    card_paths = []
    for _, card in drawn_cards.iterrows():
        rank = card['Rank']
        suit = card['Suit']
        image_path = f"cards/{rank}_of_{suit}.png"
        card_paths.append(image_path)
    return card_paths

def resize_card_image(card_path, card_width, card_height):
    pil_image = Image.open(card_path)
    pil_image = pil_image.resize((card_width, card_height), Image.LANCZOS)  # Redimensionar imagen
    return pil_image
