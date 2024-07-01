import tkinter as tk
import matplotlib.pyplot as plt

from Bot import Bot
from Deck import Deck as Deck
from Hand import Hand
from Pile import Pile
from Player import Player


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.deck = Deck()
        self.player = Player('Player')
        self.bot = Bot('Bot')
        self.pile = Pile()
        self.round_count = 0

    def distribute(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player.hand = Hand()
        self.bot.hand = Hand()
        # Distribute 16 cards to each player
        for _ in range(16):
            self.player.add_card(self.deck.draw_card())
            self.bot.add_card(self.deck.draw_card())
        # Order cards in the players hands
        self.player.hand.order()
        self.bot.hand.order()

    def choose_first_player(self):
        # the one with the queen of hearts starts
        # if no one has it, the player starts
        for _, card in self.player.hand.iterrows():
            if card['Rank'] == 'queen' and card['Suit'] == 'hearts':
                # print("You have the Queen of hearts, you start")
                return self.player, self.bot
        for _, card in self.bot.hand.iterrows():
            if card['Rank'] == 'queen' and card['Suit'] == 'hearts':
                # print("Bot has the Queen of hearts, he starts")
                return self.bot, self.player
        # print("No one has the Queen of hearts, you start")
        return self.player, self.bot

    def play_cards(self, player, cards_to_play):
        for _, card in cards_to_play.iterrows():
            if self.pile.card_is_playable(card):
                player.remove_card(card)
                self.pile.add_card(card)
            else:
                print(f"{player.name} cannot play {card['Rank']} of {card['Suit']}")

    def play_game(self):
        self.distribute()
        # WIN CHECK
        passed = False
        current_player, next_player = self.choose_first_player()

        while True:
            if self.pile.game_type == "":
                current_player.has_started = True
                next_player.has_started = False
            if self.player.hand.empty or self.bot.hand.empty:
                self.pile.reset()
                # print("Game over")
                if self.player.hand.empty:
                    print("------Player win------")
                    return "Player"
                else:
                    print("------Bot wins------")
                    return "Bot"

            print(f"\n{current_player.name}'s turn")
            if current_player.can_cut(self.pile):
                cards_to_play = current_player.cut(self.pile)
                print("///////////" + current_player.name + ' CUTS///////////')
                cards_to_play.log()
                self.play_cards(current_player, cards_to_play)
                current_player.count_round_win(self.pile)
                self.pile.reset()
                continue
            else:
                cards_to_play = current_player.choose_cards_to_play(self.pile, passed)

            if cards_to_play is None or cards_to_play.empty:
                if self.pile.is_card_or_nothing() and passed:
                    print(current_player.name + " can't play either, he still wins the round")
                    passed = False
                    current_player.count_round_win(self.pile)
                    self.pile.reset()
                    continue
                elif self.pile.is_card_or_nothing() and current_player.can_play(self.pile):
                    print(current_player.name + " doesn't have a " + self.pile.iloc[-1][
                        "Rank"] + ", he passes")
                    passed = True
                elif current_player.can_play(self.pile):
                    print(current_player.name + " passes")
                    next_player.count_round_win(self.pile)
                    self.pile.reset()
                    current_player, next_player = next_player, current_player
                    continue
                elif not current_player.can_play(self.pile):
                    print(current_player.name + " can't play, " + next_player.name + " wins the round")
                    current_player.log()
                    next_player.count_round_win(self.pile)
                    self.pile.reset()
                    current_player, next_player = next_player, current_player
                    continue
            else:
                if self.pile.game_type == "":
                    self.round_count += 1
                    print(current_player.name + ' started the round')
                    if cards_to_play.shape[0] == 1:
                        current_player.solos_started += 1
                        self.pile.game_type = "solo"
                        print(current_player.name + ' started a solo')
                    elif cards_to_play.shape[0] == 2:
                        current_player.pairs_started += 1
                        self.pile.game_type = "pair"
                        print(current_player.name + ' started a pair')

                print(current_player.name + ' chose to play: ')
                cards_to_play.log()
                self.play_cards(current_player, cards_to_play)
                passed = False

                if self.pile.iloc[-1]['Rank'] == '2':
                    print(current_player.name + ' played a 2, he wins the round')
                    current_player.count_round_win(self.pile)
                    self.pile.reset()
                    continue
                if self.pile.is_card_or_nothing() and not passed:
                    print(self.pile.iloc[-1]['Rank'] + " OR NOTHING !!")
            print(current_player.name, "remaining cards: " + str(current_player.hand.shape[0]))
            current_player, next_player = next_player, current_player

    def simulate(self, n):
        player_wins = 0
        bot_wins = 0
        for _ in range(n):
            if self.play_game() == "Player":
                player_wins += 1
            else:
                bot_wins += 1
        labels = ['Player', 'Bot']
        sizes = [player_wins, bot_wins]
        colors = ['#ff9999', '#66b3ff']

        # Adjusting the figure size
        fig1, ax1 = plt.subplots(figsize=(8, 8))

        # Adjusting the size of the pie chart
        ax1.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85)

        # Draw circle for donut style pie chart
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        # Set a short title
        ax1.set_title(f"Simulation Results\nTotal games: {n}\nTotal rounds: {self.round_count}\n")

        detailed_info = (f"Player's started rounds : {self.player.solos_started}\n"
                         f"Player's started rounds wr : {self.player.started_hands_won}\n"
                         f"Bot's started rounds {self.bot.solos_started + self.bot.pairs_started}\n"
                         f"Bot's started rounds wr : {round((self.bot.started_hands_won / (self.bot.solos_started + self.bot.pairs_started))*100)}%\n"
                         f"Bot's started simple rounds : {self.bot.solos_started}\n"
                         f"Bot's started simple rounds wr : {round((self.bot.solos_started_won/self.bot.solos_started)*100)}%\n"
                         f"Bot's started pair rounds : {self.bot.pairs_started}\n"
                         f"Bot's started pair rounds wr: {round((self.bot.pairs_started_won/self.bot.pairs_started)*100)}%\n")

        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        plt.text(-.45, .2, detailed_info, fontsize=10, verticalalignment='top', bbox=props)

        plt.axis('equal')
        plt.show()


app = App()
app.simulate(150)
