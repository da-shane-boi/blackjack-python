import unittest
from io import StringIO
from test_base import captured_io
from player import player as ply

class test_player(unittest.TestCase):

    def test_show_hand(self):
        # Test that show_hand prints hand
        with captured_io(StringIO('Jeff')) as (out, err):
            player_1 = ply()
            player_1.hand.current_hand = ['♥A', '♠6']
            player_1.hand.show_hand()
        output = out.getvalue().strip()
        self.assertEqual('♥A ♠6', output[-5::])

        with captured_io(StringIO('Jeff')) as (out, err):
            player_2 = ply()
            player_2.hand.current_hand = ['♥A', '♠6', '♠2']
            player_2.hand.show_hand()
        output = out.getvalue().strip()
        self.assertEqual('♥A ♠6 ♠2', output[-8::])

    def test_score(self):
        # Test blackjack
        with captured_io(StringIO('Jeff')) as (out, err):
            player_1 = ply()
            player_1.hand.current_hand = ['♥A', '♣J']
            player_1.hand.stand()
        self.assertEqual(player_1.hand.score, 21)
        self.assertFalse(player_1.hand.is_bust)
        self.assertTrue(player_1.hand.is_blackjack)

        # Test random score
        with captured_io(StringIO('Jeff')) as (out, err):
            player_2 = ply()
            player_2.hand.current_hand = ['♥6', '♠J']
            player_2.hand.stand()
        self.assertEqual(player_2.hand.score, 16)
        self.assertFalse(player_2.hand.is_bust)

        # Test bust
        with captured_io(StringIO('Jeff')) as (out, err):
            player_3 = ply()
            player_3.hand.current_hand = ['♥6', '♠J']
            player_3.hand.hit(['♥Q'])
        self.assertEqual(player_3.hand.current_hand, ['♥6', '♠J', '♥Q'])
        self.assertTrue(player_3.hand.is_bust)

    def test_hit(self):

        # Test that hit adds card to hand
        with captured_io(StringIO('Jeff')) as (out, err):
            player_1 = ply()
            player_1.hand.current_hand = ['♥A', '♠6']
            player_1.hand.hit(['♠Q'])
            player_1.hand.show_hand()
        output = out.getvalue().strip()
        self.assertEqual('♥A ♠6 ♠Q', output[-8::])
        self.assertEqual(player_1.hand.current_hand, ['♥A', '♠6', '♠Q'])

        # Test that score is added and not bust
        with captured_io(StringIO('Jeff')) as (out, err):
            player_2 = ply()
            player_2.hand.current_hand = ['♥A', '♠6']
            player_2.hand.hit(['♥6'])
        self.assertEqual(['♥A', '♠6', '♥6'], player_2.hand.current_hand)
        self.assertEqual(player_2.hand.score, 13)
        self.assertFalse(player_2.hand.is_bust)


        # # Test that score is added and bust
        with captured_io(StringIO('Jeff')) as (out, err):
            player_3 = ply()
            player_3.hand.current_hand = ['♠Q', '♠6']
            player_3.hand.hit(['♣J'])
        self.assertEqual(['♠Q', '♠6', '♣J'], player_3.hand.current_hand)
        self.assertEqual(player_3.hand.score, 26)
        self.assertTrue(player_3.hand.is_bust)

    def test_split(self):

        # Test split 
        with captured_io(StringIO('Jeff')) as (out, err):
            player_1 = ply()
            player_1.bet(500)
            player_1.hand.current_hand = ['♠A', '♥A']
            player_1.split_hand()
        self.assertEqual(['♠A'], player_1.hand[0].current_hand)
        self.assertEqual(['♥A'], player_1.hand[1].current_hand)
        self.assertTrue(player_1.is_split)
        
        # Test can't split
        with captured_io(StringIO('Jeff')) as (out, err):
            player_2 = ply()
            player_2.hand.current_hand = ['♥6', '♥A']
            player_2.split_hand()
        self.assertEqual(['♥6', '♥A'], player_2.hand.current_hand)
        self.assertFalse(player_2.is_split)

        with captured_io(StringIO('Jeff')) as (out, err):
            player_3 = ply()
        player_3.bet(500)
        player_3.hand.current_hand = ['♠A', '♥A']
        player_3.split_hand()
        player_3.hand[0].hit(['♥J'])
        player_3.hand[1].hit(['♠6'])
        
        # Test hit and score on split hands individually
        self.assertEqual(player_3.hand[0].current_hand, ['♠A', '♥J'])
        self.assertEqual(player_3.hand[0].score, 21)
        self.assertEqual(player_3.hand[1].current_hand, ['♥A', '♠6'])
        self.assertEqual(player_3.hand[1].score, 17)

        # Test bust on one hand 
        player_3.hand[1].hit(['♥Q'])
        player_3.hand[1].hit(['♥K'])
        self.assertFalse(player_3.hand[0].is_bust)
        self.assertTrue(player_3.hand[1].is_bust)

    def test_bet(self):

        # Test that bet subtracts from cash
        with captured_io(StringIO('Jeff')) as (out, err):
            player_1 = ply()
        player_1.bet(500)
        self.assertEqual(player_1.cash, 29500)
        self.assertEqual(player_1.pot, 500)

        # Test that if bet but then split, adds money for last deck too 
        with captured_io(StringIO('Jeff')) as (out, err):
            player_2 = ply()
        player_2.hand.current_hand = ['♥A', '♠A']
        player_2.bet(500)
        player_2.split_hand()
        self.assertEqual(player_2.cash, 29000)
        self.assertEqual(player_2.pot, 1000)
    
    def test_raise_bet(self):

        # Test that raise increases bet, subtracts from cash and adds to pot
        with captured_io(StringIO('Jeff\n500\n')) as (out, err):
            player_1 = ply()
            bet = 500
            player_1.bet(bet)
            player_1.raise_bet()
        self.assertEqual(player_1.pot, 1000)
        self.assertEqual(player_1.last_bet, 1000)
        self.assertEqual(player_1.cash, 28500)

    def test_check_balckjack(self):

        # Test that blackjack is detected with Jack then Ace
        with captured_io(StringIO()) as (out, err):
            player = ply()
            player.hand.current_hand = ['♠J', '♦A']
            sort_hand = player.hand.sort_hand(player.hand.current_hand)
            player.hand.check_blackjack(sort_hand)
        self.assertTrue(player.hand.is_blackjack)

        # Test that blackjack is not detected
        with captured_io(StringIO()) as (out, err):
            player = ply()
            player.hand.current_hand = ['♣J', '♠Q']
            sort_hand = player.hand.sort_hand(player.hand.current_hand)
            player.hand.check_blackjack(sort_hand)
        self.assertFalse(player.hand.is_blackjack)

