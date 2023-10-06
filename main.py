from player import player as ply
from util import deck as dk
from util import dealer as dlr
import os
import random

class main():
    def __init__(self) -> None:
        self.rounds = 0
        self.players = []
        self.dealer = dlr()
        self.deck = dk()
        self.play = True
    
    def players_init(self):
        player_count = input('How many players are there? ')
        while not player_count.isdigit():
            player_count = input('Please input valid integer. ')
        for i in range(int(player_count)):
            self.players.append(ply())
            self.players[i].get_username()
            print(f"Welcome, {self.players[i].username}!")
    
    def players_reinit(self):
        for player in self.players:
            player.hand = ply.hand_class()
            player.pot = 0
            player.is_split = False
        self.dealer.hand = ply.hand_class()
        
    def deal(self, deck=None):
        if deck == None: deck = self.deck.cards
        for player in self.players:
            [player.hand.hit(deck) for i in range(2)]
            print(player.username)
            player.hand.show_hand()
        [self.dealer.hand.hit(deck) for i in range(2)]
        self.dealer.show_start()

    def player_turn(self, player):
        print(f"Dealer's Hand\n{self.dealer.hand.current_hand[0]} ##\n{player.username}'s Hand\n{' '.join(player.hand.current_hand)}\nBet: {player.pot}\nCash: {player.cash}")
        turn = True
        while turn:
            match input('Hit, Raise, Stand.\n').lower().strip():
                case 'exit':
                    self.players.remove(player)
                    break
                case 'hit':
                    player.hand.hit(self.deck.cards)
                    if player.hand.is_bust: 
                        print(f"{' '.join(player.hand.current_hand)} - bust")
                        break
                    player.hand.show_hand()

                case 'raise':
                    player.raise_bet()
                    print(f"Raising bet to {player.pot}.")

                case 'stand':
                    player.hand.stand()
                    break

                case 'split':
                    player.split_hand()
                    if player.is_split:
                        def show_hand(hand1, hand2, bet=''):print(f"Hand 1\n{' '.join(player.hand[0].current_hand)}{hand1}\nHand 2\n{' '.join(player.hand[1].current_hand)}{hand2}{bet}")
                        hand1, hand2 = '',''

                        show_hand(hand1, hand2, bet=f"\nBet: {player.pot}")

                        for hand in player.hand:
                            hand_index = player.hand.index(hand)
                            while True:
                                match input(f"Hit or Stand for Hand {hand_index+1}.\n").lower().strip():
                                    case 'hit':
                                        player.hand[hand_index].hit(self.deck.cards)
                                        if player.hand[0].is_bust: hand1 = ' - bust'
                                        if player.hand[1].is_bust: hand2 = ' - bust'
                                        show_hand(hand1, hand2)
                                        if player.hand[hand_index].is_bust: 
                                            if hand_index == 1: turn = False
                                            break
                                        

                                    case 'stand':
                                        player.hand[hand_index].stand()
                                        if hand_index == 1: turn = False
                                        break

    def player_remove(self, player):
        print(f"{player.username} has run out of money!!\nPlease Leave.")
        self.players.remove(player)
        input("Plead and Cry nobody cares.\n")


    def game(self):
        self.players_init()
        while len(self.players) > 0:
            for player in self.players:
                os.system("clear")

                bet = input(f"How much would you like to bet {player.username}?\nYou have {player.cash}\n")
                while int(bet) > player.cash:
                    bet = input(f"Max bet of {player.cash} allowed.\nHow much would you like to bet?\n")
                else:
                    player.bet(int(bet)) 
                
            self.deck = dk()
            self.deal()

            for player in self.players:
                os.system("clear")
                self.player_turn(player)
                input()

            for player in self.players:
                os.system("clear")
                self.handle_result(self.result(player), player)
                contin = input("Continue? Y/n").strip().lower()
                if contin and contin[0] == 'n':
                    self.players.remove(player)
            
            [self.player_remove(player) if player.cash == 0 else None for player in self.players]

            self.players_reinit()

    def show_hand(self, player):
        if not player.is_split:    
            bus = ''
            if player.hand.is_bust:
                bus = ' - bust'
            print(f"{player.username}'s hand\n{' '.join(player.hand.current_hand)}{bus}")
        elif player.is_split:
            for i in range(2):
                if player.hand[i].is_bust:
                    bus = ' - bust'
                else: bus = ''
                print(f"{player.username}'s hand{i+1}\n{' '.join(player.hand[i].current_hand)}{bus}")

            
    
    def result(self, player):
        beat_dealer = False
        self.dealer.max_score(self.deck.cards)
        if player.is_split:
            for i in range(2):
                if player.hand[i].score >= self.dealer.hand.score and not self.dealer.hand.is_blackjack and not player.hand[i].is_bust or player.hand[i].is_blackjack or self.dealer.hand.is_bust:
                    beat_dealer = True
        else:

            if player.hand.score >= self.dealer.hand.score and not player.hand.is_bust and not self.dealer.hand.is_blackjack or player.hand.is_blackjack or self.dealer.hand.is_bust:
                beat_dealer = True
        return beat_dealer

    def handle_result(self, res, player):
        insults = ["has no b*tches.", "has no game.", "might as well just spectate.", "is here to get schooled.", "should've stayed home.", "gets got."]
        self.show_hand(self.dealer)
        self.show_hand(player)
        if res: 
            player.cash += player.pot * 2
            print(f"{player.username} beats dealer.")
        else:
            print(f"{player.username} {insults[random.randint(0, len(insults)-1)]}")


if __name__ == '__main__':
    game = main()
    game.game()