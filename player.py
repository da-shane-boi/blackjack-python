class player:
    def __init__(self):
        self.hand = self.hand_class()
        self.cash = 30000
        self.is_split = False
        self.pot = 0

    class hand_class:
        def __init__(self):
            self.current_hand = []
            self.score = 0
            self.is_bust = False
            self.is_blackjack = False

        def show_hand(self):
            print(" ".join(self.current_hand))

        def stand(self):
            self.calculate_score()
            self.check_bust()

        def hit(self, deck):
            self.current_hand.append(deck.pop())
            self.calculate_score()
            self.check_bust()

        def calculate_score(self):
            score = 0
            hand = self.sort_hand(self.current_hand)
            self.check_blackjack(hand)
            for card in hand:
                num = card
                if num == "A": num = "11" if score <= 10 else "1"
                score += int(num)
            self.score = score

        def sort_hand(self, unsorted_hand):
            hand = ["10" if card[1:] in "KQJ" else card[1:] for card in unsorted_hand]
            hand.sort()
            return hand

        def check_bust(self):
            if self.score > 21: self.is_bust = True

        def check_blackjack(self, sorted_hand):
            if len(sorted_hand) == 2: self.is_blackjack = True if sorted_hand[0] == "10"and "A" in sorted_hand[1] else False
                # if sorted_hand[0] == "10"and "A" in sorted_hand[1]:
                #     self.is_blackjack = True 
                
            
    def get_username(self):
        self.username = input("What would you like your username to be?\n")

    def bet(self, bet):
        self.pot += bet
        self.cash -= bet
        self.last_bet = bet
        

    def raise_bet(self):
        amount = input(f"How much would you like to raise?\nCurrent bet is {self.pot}.\n")
        while not amount.isdigit():
            amount = input(f"Please input a valid amount\nCurrent bet is {self.pot}.\n")
        amount = int(amount)
        # if self.is_split: amount *= 2 if not self.hand[0].is_bust and not self.hand[1].is_bust else 1

        self.last_bet += amount
        self.cash -= self.last_bet
        self.pot += amount
        self.last_bet = self.last_bet

    def split_hand(self):
        if self.hand.current_hand[0][1] == self.hand.current_hand[1][1]:
            self.bet(self.last_bet)
            self.is_split = True
            cards = self.hand.current_hand
            self.hand = [self.hand_class(), self.hand_class()]
            self.hand[0].current_hand.append(cards[0])
            self.hand[1].current_hand.append(cards[1])

