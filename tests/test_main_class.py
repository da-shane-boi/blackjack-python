import unittest
from io import StringIO
from test_base import captured_io
from util import deck as dk
from main import main 
from player import player as ply


class test_main(unittest.TestCase):

    def test_players_init(self):
        # Test that amount of players are added to list
        with captured_io(StringIO('2\nJeff\nBetty')) as (out, err):
            game = main()
            game.players_init()
        output = out.getvalue().strip()
        self.assertEqual(len(game.players), 2)

        # Test that player number is valid integer
        with captured_io(StringIO('test\n3\nBetty\nJeremy\nJeff')) as (out, err):
            game = main()
            game.players_init()
        output = out.getvalue().strip()
        self.assertEqual(len(game.players), 3)

        # Test that username is added and Welcome message is displayed
        with captured_io(StringIO('1\nJeff')) as (out, err):
            game = main()
            game.players_init()
        output = out.getvalue().strip()
        self.assertEqual('How many players are there? What would you like your username to be?\nWelcome, Jeff!', output)

    def test_players_reinit(self):
        # Test that players hands are reinitialised, clearing cards, booleans and score
        with captured_io(StringIO('')) as (out, err):
            game = main()
            player_1 = ply()
            player_1.hand.is_bust = True
            player_1.hand.score = 24
            player_1.hand.current_hand = ['♥J', '♦J', '♥4']
            game.players.append(player_1)
            game.players_reinit()
            player1 = game.players[0]
        self.assertFalse(player1.hand.is_bust)
        self.assertEqual(player1.hand.score, 0)
        self.assertEqual(player1.hand.current_hand, [])

    def test_deal(self):
        # Test 2 cards are given at the start and that 6 cards are taken out of the deck
        with captured_io(StringIO('2\nJeff\nBetty')) as (out, err):
            game = main()
            game.players_init()
            deck = dk()
            deck.shuffle()
            game.deal(deck.cards)
        # output = out.getvalue().strip()
        self.assertEqual(len(game.players[0].hand.current_hand), 2)
        self.assertEqual(len(game.players[1].hand.current_hand), 2)
        self.assertEqual(len(game.dealer.hand.current_hand), 2)
        self.assertEqual(len(deck.cards), 46)

    def test_result(self):
        # Test that player beats dealer
        with captured_io(StringIO('1\nJeff\nstand')) as (out, err):
            game = main()
            game.players_init()
            game.deal(['♠K', '♠J', '♠Q', '♠A'])
            game.players[0].bet(500)
            game.player_turn(game.players[0])
            res = game.result(game.players[0])
        self.assertTrue(res)

        # Test that blackjack beats normal 21 
        with captured_io(StringIO('1\nJeff\nstand')) as (out, err): 
            game = main()
            game.players_init()
            game.deal(['♥A', '♠K', '♠J', '♠Q', '♠A'])
            game.players[0].bet(500)
            game.player_turn(game.players[0])
            res = game.result(game.players[0])
        self.assertTrue(res)

        # Test that split deck beats dealer
        with captured_io(StringIO('1\nJeff\nsplit\nhit\nstand\nhit\nstand')) as (out, err):
            game = main()
            game.players_init()
            game.deal(['♠K', '♠J','♥A', '♠A'])
            game.deck.cards = ['♥Q', '♥8']
            game.players[0].bet(500)
            game.player_turn(game.players[0])
            res = game.result(game.players[0])
        self.assertTrue(res)
        self.assertEqual(game.players[0].pot, 1000)

        # Test that dealer beats player
        with captured_io(StringIO('1\nJeff\nstand')) as (out, err):
            game = main()
            game.players_init()
            game.deal(['♠K', '♠A', '♠J', '♠Q'])
            game.players[0].bet(500)
            game.player_turn(game.players[0])
            res = game.result(game.players[0])
        self.assertFalse(res)

# class test_player_turn(unittest.TestCase):
#     def test_player_turn_stand(self):
#         # Test that player is shown cards and can choose to stand
#         with captured_io(StringIO('1\nJeff\nstand')) as (out, err):
#             game = main()
#             game.players_init()
#             game.deal(['♠K', '♠J','♥7', '♥Q'])
#             game.players[0].bet(500)
#             game.player_turn(game.players[0])
#         output = out.getvalue().strip()
#         self.assertEqual('''Dealer's Hand
# ♠J ##
# Jeff's Hand
# ♥Q ♥7
# Bet: 500
# Hit, Raise, Stand.''', output[-65:])

#     def test_player_turn_hit(self):
#         # Test that player can hit
#         with captured_io(StringIO('1\nJeff\nhit\nstand')) as (out, err):
#             game = main()
#             game.players_init()
#             game.deal(['♠K', '♠J','♥7', '♥Q'])
#             game.deck.cards = ['♣2']
#             game.players[0].bet(500)
#             game.player_turn(game.players[0])
#         output = out.getvalue().strip()
#         self.assertEqual(game.players[0].hand.current_hand, ['♥Q', '♥7', '♣2'])
#         self.assertEqual('''Dealer's Hand
# ♠J ##
# Jeff's Hand
# ♥Q ♥7
# Bet: 500
# Hit, Raise, Stand.
# ♥Q ♥7 ♣2
# Hit, Raise, Stand.''', output[-93:])

#     def test_player_turn_raise(self):
#         # Test that player can raise
#         with captured_io(StringIO('1\nJeff\nraise\n500\nstand')) as (out, err):
#             game = main()
#             game.players_init()
#             game.deal(['♠K', '♠J','♥7', '♥Q'])
#             game.deck.cards = ['♣2']
#             game.players[0].bet(500)
#             game.player_turn(game.players[0])
#         output = out.getvalue().strip()
#         self.assertEqual(game.players[0].pot, 1000)
#         self.assertEqual('''Dealer's Hand
# ♠J ##
# Jeff's Hand
# ♥Q ♥7
# Bet: 500
# Hit, Raise, Stand.
# How much would you like to raise?
# Current bet is 500.
# Raising bet to 1000.
# Hit, Raise, Stand.''', output[-159:])

#     def test_player_turn_bust(self):

#         # Test that bust is handled correctly 
#         with captured_io(StringIO('1\nJeff\nhit')) as (out, err):
#             game = main()
#             game.players_init()
#             game.deal(['♠K', '♠J','♥7', '♥Q'])
#             game.deck.cards = ['♣J']
#             game.players[0].bet(500)
#             game.player_turn(game.players[0])
#         output = out.getvalue().strip()
#         self.assertEqual('''Dealer's Hand
# ♠J ##
# Jeff's Hand
# ♥Q ♥7
# Bet: 500
# Hit, Raise, Stand.
# ♥Q ♥7 ♣J - bust''', output[-81:])
#         self.assertTrue(game.players[0].hand.is_bust)

#     def test_player_turn_split(self):
        
#         # Test split functionality within player_turn
#         with captured_io(StringIO('1\nJeff\nsplit\nhit\nstand\nhit\nstand')) as (out, err):
#             game = main()
#             game.players_init()
#             game.deal(['♠K', '♠J','♥A', '♠A'])
#             game.players[0].bet(500)
#             game.deck.cards = ['♠9', '♦8']
#             game.player_turn(game.players[0])
#         output = out.getvalue().strip()
#         self.assertEqual('''Dealer's Hand
# ♠J ##
# Jeff's Hand
# ♠A ♥A
# Bet: 500
# Hit, Raise, Stand.
# Hand 1
# ♠A
# Hand 2
# ♥A
# Bet: 1000
# Hit or Stand for Hand 1.
# Hand 1
# ♠A ♦8
# Hand 2
# ♥A
# Hit or Stand for Hand 1.
# Hit or Stand for Hand 2.
# Hand 1
# ♠A ♦8
# Hand 2
# ♥A ♠9
# Hit or Stand for Hand 2.''', output[-244:])
#         self.assertEqual(game.players[0].pot, 1000)

#     def test_player_turn_split_bust(self):
#         # Test split functionality with hand 1 bust
#         with captured_io(StringIO('1\nJeff\nsplit\nhit\nhit\nhit\nhit\nstand')) as (out, err):
#             game = main()
#             game.players_init()
#             game.deal(['♠K', '♠J','♥A', '♠A'])
#             game.players[0].bet(500)
#             game.deck.cards = ['♦J', '♥K', '♠Q', '♦8']
#             game.player_turn(game.players[0])
#         output = out.getvalue().strip()
#         self.assertEqual('''Dealer's Hand
# ♠J ##
# Jeff's Hand
# ♠A ♥A
# Bet: 500
# Hit, Raise, Stand.
# Hand 1
# ♠A
# Hand 2
# ♥A
# Bet: 1000
# Hit or Stand for Hand 1.
# Hand 1
# ♠A ♦8
# Hand 2
# ♥A
# Hit or Stand for Hand 1.
# Hand 1
# ♠A ♦8 ♠Q
# Hand 2
# ♥A
# Hit or Stand for Hand 1.
# Hand 1
# ♠A ♦8 ♠Q ♥K - bust
# Hand 2
# ♥A
# Hit or Stand for Hand 2.
# Hand 1
# ♠A ♦8 ♠Q ♥K - bust
# Hand 2
# ♥A ♦J
# Hit or Stand for Hand 2.''', output[-344:])
#         self.assertEqual(game.players[0].pot, 1000)
#         self.assertTrue(game.players[0].hand[0].is_bust)
