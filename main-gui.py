from landing import FrontWindow as fw
import pygame as pg
import util
import sys

# def landing_page(screen, res):


if __name__ == "__main__":
    pg.init()

    res = width, height = 1600, 900
    screen = pg.display.set_mode(res)
    
    match fw(screen, res):
        case 'exit':
            sys.exit()
        case 'blackjack':
            sys.exit()
                