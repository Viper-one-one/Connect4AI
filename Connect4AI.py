
from ast import Global
from faulthandler import is_enabled
from tkinter import Widget
from tkinter.ttk import Progressbar
from turtle import position
import pygame
import random
import numpy as np
import sys
import math
import pygame_menu
from pygame_menu import themes

#definitions
HEIGHT = 700
WIDTH = 700
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

#game functions and ai control
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def check_win(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

#Player types
def random_player():
    return 0

def blocking_player():
    return 0

#pygame creation
pygame.init()
ai_type = 0
surface = pygame.display.set_mode((HEIGHT,WIDTH))
board = create_board()
turn = 0
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
RADIUS = int(SQUARESIZE / 2 - 5)
my_font = pygame.font.SysFont("monospace", 75)

#menu functions
def start_game():
    print_board(board)
    play()

def ai_player_type_menu():
    mainmenu._open(ai)

def set_ai(type, num):
    ai_type = num



def play():
    game_over = False
    turn = 0
    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                positionx = event.pos[0]
                if turn == PLAYER: 
                    pygame.draw.circle(screen, RED, (positionx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                if turn == PLAYER:
                    positionx = event.pos[0]
                    col = int(math.floor(positionx/SQUARESIZE))

                    if is_valid(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                    if check_win(board, PLAYER_PIECE):
                        label = my_font.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True
                    turn += 1
                    turn = turn % 2
                    print_board(board)
                    draw_board(board)
        if turn == AI and not game_over:
            if ai_type == 1:
                positionx = random.choice(range(0,ROW_COUNT))
                col = int(math.floor(positionx/SQUARESIZE))
                if is_valid(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, col, row, AI_PIECE)
                    if check_win(board, AI_PIECE):
                        label = my_font("Random AI wins!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True
                    turn += 1
                    turn = turn % 2
                    print_board(board)
                    draw_board(board)
        if game_over:
            pygame.time.wait(5000)


#Welcome Screen and Menu
mainmenu = pygame_menu.Menu('Welcome', HEIGHT, WIDTH, theme=themes.THEME_DARK)
mainmenu.add.button('Play', start_game)
mainmenu.add.button('AI Settings', ai_player_type_menu)

ai = pygame_menu.Menu('Select a style of AI player', HEIGHT, WIDTH, theme=themes.THEME_DARK)
ai.add.selector('Styles: ', [('Random', 1), ('Blocking', 2), ('State Space Search', 3)], default=0, onchange=set_ai)

loading = pygame_menu.Menu('Loading...', HEIGHT, WIDTH, theme=themes.THEME_SOLARIZED)
loading.add.progress_bar('Progress', progressbar_id='1', default=0, width=100)

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10,15))

update_loading = pygame.USEREVENT+0

print(random.choice(range(0,ROW_COUNT)))

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget('1')
            if progress.get_value() >= 100:
                progress.reset_value()
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
