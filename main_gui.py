from index import index_window
import blackjack_gui
import pygame as pg
import util
import sys
from main import main as blackjack

def display_index_window(window, res, game):
    pg.display.set_caption('Index')
    match index_window(window, res, game):
        case "exit":
            sys.exit()
        case "blackjack":
            return blackjack_gui.BlackjackWindow(window, res, game)


if __name__ == "__main__":
    pg.init()
    game = blackjack()
    res = width, height = 1600, 900
    window = pg.display.set_mode(res)

    display_index_window(window, res, game)
