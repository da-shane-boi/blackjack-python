import pygame as pg
import sys
import util
from main_gui import display_index_window
from create_players import create_players_window

def BlackjackWindow(window, res, game):
    '''Blackjack window'''

    pg.display.set_caption('Blackjack')
    ubuntu_font = pg.font.SysFont('Ubuntu', 35)
    black = 0, 0, 0
    gray = 170, 170, 170

    back_button_dimensions = back_button_width, back_button_height = 50, 50
    back_button_topleft = res[0] - back_button_width - 20, 0 + 20

    create_players_button_dimensions = create_players_button_width, create_players_button_height = 600, 50
    create_players_topleft = 20, 20

    while True:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                sys.exit()

            if ev.type == pg.MOUSEBUTTONDOWN:
                if util.mouse_over_button(mouse_pos, back_button_topleft, back_button_width, back_button_height):
                    return display_index_window(window, res, game)

                if util.mouse_over_button(mouse_pos, create_players_topleft, create_players_button_width, create_players_button_height):
                    return create_players_window(window, res, game)


        window.fill('black')

        mouse_pos = pg.mouse.get_pos()
        back_button = util.create_button(window, mouse_pos, '<-', ubuntu_font, back_button_topleft, back_button_dimensions, black, gray, gray, black)
        create_players_button = util.create_button(window, mouse_pos, 'Create Players', ubuntu_font, create_players_topleft, create_players_button_dimensions, black, gray, gray, black)

        window.blit(back_button, back_button_topleft)
        window.blit(create_players_button, create_players_topleft)
        pg.display.update()



