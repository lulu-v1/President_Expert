def on_card_click(event, card_label, selected_card_labels):
    if card_label in selected_card_labels:
        # Deselect the card if it's already selected
        card_label.place_configure(y=card_label.original_y)
        card_label.config(borderwidth=1, relief="raised", highlightthickness=0)
        selected_card_labels.remove(card_label)
    else:
        # Highlight the selected card
        selected_card_labels.append(card_label)
        card_label.place_configure(y=card_label.original_y - 10)  # Move the card up slightly
        card_label.config(borderwidth=1, relief="solid", highlightbackground="black", highlightcolor="black", highlightthickness=2)
