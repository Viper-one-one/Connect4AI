
from faulthandler import is_enabled
from tkinter import Widget
from tkinter.ttk import Progressbar
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
    print("hello world")

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
ai.add.selector('Styles: ', [('Random', 1), ('Blocking', 2), ('State Space Search', 3)], default=0, onchange=set_ai)

loading = pygame_menu.Menu('Loading...', HEIGHT, WIDTH, theme=themes.THEME_SOLARIZED)
loading.add.progress_bar('Progress', progressbar_id='1', default=0, width=100)

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10,15))

update_loading = pygame.USEREVENT+0

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget('1')
            progress.set_value(progress.get_value() + 1)
            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading,0)
        if event.type == pygame.QUIT:
            exit()
    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)
        if(mainmenu.get_current().get_selected_widget()):
            arrow.draw(surface, mainmenu.get_current().get_selected_widget())

    pygame.display.update()
