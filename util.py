import random
from player import player as ply

class deck():
    def __init__(self):
        self.suits = ['♥', '♠', '♣', '♦']
        self.card_nums = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = self.build()
        self.shuffle()

    def build(self):
        return [f"{suit}{card}" for card in self.card_nums for suit in self.suits]

    def shuffle(self):
        random.shuffle(self.cards)


class dealer():
    def __init__(self):
        self.hand = ply.hand_class()
        self.username = "Dealer"
        self.is_split = False

    def max_score(self, deck):
        # self.hand.calculate_score()
        while self.hand.score <= 16 and not self.hand.is_bust:
            self.hand.hit(deck)

    def show_start(self):
        print(f"{self.hand.current_hand[0]} ##")