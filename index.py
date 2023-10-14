import pygame as pg
import sys
import util



def index_window(window, res:tuple[int,int], game) -> str:    
    '''Index page'''
    black = 0, 0, 0
    gray = 170, 170, 170
    smallfont = pg.font.SysFont('Ubuntu', 35)


    button_1_dimensions = button_1_width, button_1_height = 450, 50  
    button_1_topleft =  20, 20

    button_2_dimensions = button_2_width, button_2_height = 240, 50
    button_2_topleft = res[0] - 20 - button_2_width, res[1] - 20 - button_2_height


    while True:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                sys.exit()

            if ev.type == pg.MOUSEBUTTONDOWN:
                if util.mouse_over_button(mouse_pos, button_1_topleft, button_1_width, button_1_height):
                    return 'blackjack'
                if util.mouse_over_button(mouse_pos, button_2_topleft, button_2_width, button_2_height):
                    return 'exit'    
            
            
        window.fill(black)
        mouse_pos = pg.mouse.get_pos()

        blackjack_button = util.create_button(window, mouse_pos, 'Blackjack', smallfont, button_1_topleft, button_1_dimensions, black, gray, gray, black)
        exit_button = util.create_button(window, mouse_pos, 'Exit', smallfont, button_2_topleft, button_2_dimensions, black, gray, gray, black)

        window.blit(exit_button, button_2_topleft)
        window.blit(blackjack_button, button_1_topleft)
        pg.display.update()