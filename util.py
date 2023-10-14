import random
from player import player as ply
import pygame as pg


class deck:
    def __init__(self):
        self.suits = ["♥", "♠", "♣", "♦"]
        self.card_nums = [
            "A",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "J",
            "Q",
            "K",
        ]
        self.cards = self.build()
        self.shuffle()

    def build(self):
        return [f"{suit}{card}" for card in self.card_nums for suit in self.suits]

    def shuffle(self):
        random.shuffle(self.cards)


class dealer:
    def __init__(self):
        self.hand = ply.hand_class()
        self.username = "Dealer"
        self.is_split = False

    def max_score(self, deck: list[str]) -> None:
        while self.hand.score <= 16 and not self.hand.is_bust:
            self.hand.hit(deck)

    def show_start(self) -> None:
        print(f"{self.hand.current_hand[0]} ##")


def mouse_over_button(mouse: tuple, topleft: tuple, width: int, height: int) -> bool:
    """Returns True if mouse is within pixel range"""
    return (
        topleft[0] <= mouse[0] <= topleft[0] + width
        and topleft[1] <= mouse[1] <= topleft[1] + height
    )


def create_button(
    window,
    mouse: tuple[int, int],
    text: str,
    font,
    button_topleft: tuple,
    button_dimensions: tuple,
    colour_button_normal: tuple[int, int, int],
    colour_button_highlighted: tuple[int, int, int],
    colour_text_normal: tuple[int, int, int],
    colour_text_highlighted: tuple[int, int, int],
):
    """Creates button that will change when is hovered over. Will draw button on window parsed when mouse co-ordinates are within dimensions of button."""
    if mouse_over_button(
        mouse, button_topleft, button_dimensions[0], button_dimensions[1]
    ):
        pg.draw.rect(
            window,
            colour_button_highlighted,
            [
                button_topleft[0],
                button_topleft[1],
                button_dimensions[0],
                button_dimensions[1],
            ],
        )
        return font.render(text, True, colour_text_highlighted)
    else:
        pg.draw.rect(
            window,
            colour_button_normal,
            [
                button_topleft[0],
                button_topleft[1],
                button_dimensions[0],
                button_dimensions[1],
            ],
        )
        return font.render(text, True, colour_text_normal)
