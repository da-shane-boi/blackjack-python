import pygame as pg
import sys
import util
from main_gui import index_window


def BlackjackWindow(surface, res):
    '''Blackjack window'''

    black = 0, 0, 0
    gray = 170, 170, 170

    back_button_dimensions = back_button_width, back_button_height = 50, 50
    back_button_topleft = res[0] - back_button_width - 20, 0 + 20

    ubuntu_font = pg.font.SysFont('Ubuntu', 35)


    while True:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                sys.exit()

            if ev.type == pg.MOUSEBUTTONDOWN:
                if util.mouse_over_button(mouse_pos, back_button_topleft, back_button_width, back_button_height):
                    index_window(surface, res)



        surface.fill('black')
        mouse_pos = pg.mouse.get_pos()

        back_button = util.create_button(surface, mouse_pos, '<-', ubuntu_font, back_button_topleft, back_button_dimensions, black, gray, gray, black)

        surface.blit(back_button, back_button_topleft)

        pg.display.update()



