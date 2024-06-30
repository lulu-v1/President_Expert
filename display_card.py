from Deck import Deck
from PIL import Image

suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

def draw_card_path(deck):
    drawn_cards = [deck.draw_card() for _ in range(16)]
    drawn_cards.sort(key=lambda card: ranks.index(card['Rank']))  # Ordenar cartas
    card_details = []
    for card in drawn_cards:
        rank = card['Rank']
        suit = card['Suit']
        image_path = f"cards/{rank}_of_{suit}.png"
        card_details.append({'card_path': image_path, 'Rank': rank, 'Suit': suit})
    return card_details
def resize_card_image(card_path, card_width, card_height):
    pil_image = Image.open(card_path)
    pil_image = pil_image.resize((card_width, card_height), Image.LANCZOS)  # Redimensionar imagen
    return pil_image
