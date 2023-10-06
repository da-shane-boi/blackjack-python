import unittest
from io import StringIO
from test_base import captured_io
from util import deck as dk
from util import dealer as dlr
from main import main 

class test_deck(unittest.TestCase):        

    # def test_deck_cards(self):
    # # Test that is deck
        # cards = dk()
        # self.assertEqual(cards.cards, ['♥A', '♠A', '♣A', '♦A', '♥2', '♠2', '♣2', '♦2', '♥3', '♠3', '♣3', '♦3', '♥4', '♠4', '♣4', '♦4', '♥5', '♠5', '♣5', '♦5',
        #                                     '♥6', '♠6', '♣6', '♦6', '♥7', '♠7', '♣7', '♦7', '♥8', '♠8', '♣8', '♦8','♥9', '♠9', '♣9', '♦9', '♥10', '♠10', '♣10', '♦10',
        #                                     '♥J', '♠J', '♣J', '♦J', '♥Q', '♠Q', '♣Q', '♦Q', '♥K', '♠K', '♣K', '♦K'])
    
    def test_shuffle(self):
    # Test that deck shuffles
        cards = dk()
        # cards.shuffle()
        self.assertNotEqual(cards.cards,   ['♥A', '♠A', '♣A', '♦A', '♥2', '♠2', '♣2', '♦2', '♥3', '♠3', '♣3', '♦3', '♥4', '♠4', '♣4', '♦4', '♥5', '♠5', '♣5', '♦5',
                                                '♥6', '♠6', '♣6', '♦6', '♥7', '♠7', '♣7', '♦7', '♥8', '♠8', '♣8', '♦8','♥9', '♠9', '♣9', '♦9', '♥10', '♠10', '♣10', '♦10',
                                                '♥J', '♠J', '♣J', '♦J', '♥Q', '♠Q', '♣Q', '♦Q', '♥K', '♠K', '♣K', '♦K'])

    def test_deck_in_main(self):
        game = main()
        self.assertNotEqual(game.deck.cards, ['♥A', '♠A', '♣A', '♦A', '♥2', '♠2', '♣2', '♦2', '♥3', '♠3', '♣3', '♦3', '♥4', '♠4', '♣4', '♦4', '♥5', '♠5', '♣5', '♦5',
                                            '♥6', '♠6', '♣6', '♦6', '♥7', '♠7', '♣7', '♦7', '♥8', '♠8', '♣8', '♦8','♥9', '♠9', '♣9', '♦9', '♥10', '♠10', '♣10', '♦10',
                                            '♥J', '♠J', '♣J', '♦J', '♥Q', '♠Q', '♣Q', '♦Q', '♥K', '♠K', '♣K', '♦K'])

class test_dealer(unittest.TestCase):
    def test_max_score(self):
        # Test that dealer will stand
        dealer_1 = dlr()
        dealer_1.hand.current_hand = ['♠A', '♠6']
        dealer_1.hand.calculate_score()
        dealer_1.max_score(['♥A'])
        self.assertEqual(dealer_1.hand.current_hand, ['♠A', '♠6'])
        self.assertEqual(dealer_1.hand.score, 17)

        # Test that dealer will hit 
        dealer_2 = dlr()
        dealer_2.hand.current_hand = ['♠9', '♦4']
        dealer_1.hand.calculate_score()
        dealer_2.max_score(['♥6'])
        self.assertEqual(dealer_2.hand.current_hand, ['♠9', '♦4', '♥6'])
        self.assertEqual(dealer_2.hand.score, 19)

        # Test that dealer will hit twice and bust 
        dealer_3 = dlr()
        dealer_3.hand.current_hand = ['♠9', '♦4']
        dealer_1.hand.calculate_score()
        dealer_3.max_score(['♥Q', '♥A'])
        self.assertEqual(dealer_3.hand.current_hand, ['♠9', '♦4', '♥A', '♥Q'])
        self.assertEqual(dealer_3.hand.score, 24)
        self.assertTrue(dealer_3.hand.is_bust)

    def test_show_start(self):
        # Test that only 1 card is shown to the players
        with captured_io(StringIO('')) as (out, err):
            dealer_1 = dlr()
            dealer_1.hand.current_hand = ['♠J', '♣J']
            dealer_1.show_start()
        output = out.getvalue().strip()
        self.assertEqual('♠J ##', output)

