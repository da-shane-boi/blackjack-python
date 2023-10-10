import pygame as pg
import sys

class FrontWindow():

    def mouse_over_button(mouse:tuple, topleft:tuple, width:int, height:int) -> bool:
        '''Returns True if mouse is within pixel range'''
        if topleft[0] <= mouse[0] <= topleft[0] + width and topleft[1] <= mouse[1] <= topleft[1] + height:
            return True

    pg.init()

    res = width, height = 1600, 900
    screen = pg.display.set_mode(res)

    black = 0, 0, 0
    white = 255, 255, 25
    gray = 170, 170, 170
    dark_gray = 100, 100, 100


    smallfont = pg.font.SysFont('Ubuntu', 35)

    button_1_height = 50 
    button_1_width = 450
    button_1_topleft = button_1_left, button_1_top =  20, 20



    while True:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                sys.exit()

            if ev.type == pg.MOUSEBUTTONDOWN:
                if mouse_over_button(mouse, button_1_topleft, button_1_width, button_1_height):
                    sys.exit()
            
        screen.fill(black)
        mouse = pg.mouse.get_pos()

        if mouse_over_button(mouse, button_1_topleft, button_1_width, button_1_height):
            pg.draw.rect(screen, gray, [button_1_left, button_1_top, button_1_width, button_1_height])
            blackjack_button = smallfont.render('Blackjack', True, black)
        else:
            pg.draw.rect(screen, black, [button_1_left, button_1_top, button_1_width, button_1_height])
            blackjack_button = smallfont.render('Blackjack', True, gray)


        screen.blit(blackjack_button, button_1_topleft)
        pg.display.update()