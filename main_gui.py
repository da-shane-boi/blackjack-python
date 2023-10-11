from index import FrontWindow as fw
import blackjack_gui
import pygame as pg
import util
import sys


def index_window(screen, res):
    match fw(screen, res):
        case "exit":
            sys.exit()
        case "blackjack":
            blackjack_gui.BlackjackWindow(screen, res)


if __name__ == "__main__":
    pg.init()

    res = width, height = 1600, 900
    screen = pg.display.set_mode(res)

    index_window(screen, res)
