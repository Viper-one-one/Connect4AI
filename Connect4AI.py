
import pygame
import random
import numpy as np
import sys
import math
import pygame_menu
from pygame_menu import themes

#definitions
HEIGHT = 800
WIDTH = 600

#game functions and ai control
def create_board():
    board = 1
    return board

def is_valid():
    return True

def random_player():
    return 0

def blocking_player():
    return 0

#pygame creation
pygame.init()
surface = pygame.display.set_mode((HEIGHT,WIDTH))

#menu functions
def start_game():
    pass

def ai_player_type_menu():
    mainmenu._open(ai)

def set_ai(type, num):
    return 0

#Welcome Screen and Menu
mainmenu = pygame_menu.Menu('Welcome', HEIGHT, WIDTH, theme=themes.THEME_DARK)
mainmenu.add.text_input('Name: ', default='username', maxchar=15)
mainmenu.add.button('Play', start_game)
mainmenu.add.button('AI Settings', ai_player_type_menu)

ai = pygame_menu.Menu('Select a style of AI player', HEIGHT, WIDTH, theme=themes.THEME_DARK)
ai.add.selector('Styles: ', [('Random', 1), ('Blocking', 2), ('State Space Search', 3)], onchange=set_ai)

mainmenu.mainloop(surface)