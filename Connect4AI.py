# Group Name
# Member 1
# Taylor Nastally
# Member 2
# Manpreet Dhindsa
# Member 3
# Member 4


from ast import Global
from faulthandler import is_enabled
from tkinter import Widget
from tkinter.ttk import Progressbar
from turtle import position
import pygame
import random
import numpy as np
from random import randrange
import sys
import math
import pygame_menu
from pygame_menu import themes

# 1 is player (red), 2 is ai (yellow)

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
RANDOM_AI = 1
BLOCKING_AI = 2
STATE_SPACE_SEARCH = 3
WINDOW_LENGTH = 4
#game functions and ai control
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece                 #out of bounds here

def is_valid(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
    return None

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

def state_space_player():
    return 0

#pygame creation
pygame.init()
global ai_type
ai_type = RANDOM_AI
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
    global ai_type
    ai_type = num
    print("ai_type = " + str(ai_type))

# 7 cols and 6 rows
def colInRange(colNum):
    return True if colNum >= 0 and colNum <= 6 else False

def isInRange(board, row, col):
    return True if row >= 0 and row <= 5 and col >= 0 and col <= 6 else False

def isValidBlockingMove(board, row, col):
    if isInRange(board, row, col) and board[row][col] == 0:
        if row > 0:
            for j in range(row - 1 , -1, -1):
                if board[j][col] == 0:
                    return False
        return True
    return False

"""
Checks for 3 in a row for Player 1, if found returns the col# to block else null
"""
def checkThreeInARow(board, piece):
    # For horizontal or diagonal, there can be 2 possible blocks (check if they are valid and in range) - return one at random
    # append possible blocks to possibleBlocks[] and at the end, return one that is in range/works
    possibleBlocks = []

    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece:
                if (isInRange(board,r,c-1) and isValidBlockingMove(board,r,c-1)):
                    possibleBlocks.append((r,c-1))
                if (isInRange(board,r,c+3) and isValidBlockingMove(board,r,c+3)):
                    possibleBlocks.append((r,c+3))
    
    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 2):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece:
                if (isInRange(board,r+3,c) and isValidBlockingMove(board,r+3,c)):
                    possibleBlocks.append((r+3,c))

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT - 2):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece:
                if (isInRange(board,r+3,c+3) and isValidBlockingMove(board,r+3,c+3)):
                    possibleBlocks.append((r+3,c+3))
                if (isInRange(board,r-1,c-1) and isValidBlockingMove(board,r-1,c-1)):
                    possibleBlocks.append((r-1,c-1))

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 2):
        for r in range(2, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece:
                if (isInRange(board,r-3,c+3) and isValidBlockingMove(board,r-3,c+3)):
                    possibleBlocks.append((r-3,c+3))
                if (isInRange(board,r+1,c-1) and isValidBlockingMove(board,r+1,c-1)):
                    possibleBlocks.append((r+1,c-1))

    # Find locations where there is a gapped block X0XX or XX0X, previous implementation handles XXXO and OXXX (for horizontal + diagonals)
    # Check horizontal locations for gapped block
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == 0 and board[r][c + 2] == piece and board[r][c + 3] == piece: #XOXX
                if (isInRange(board,r,c+1) and isValidBlockingMove(board,r,c+1)):
                    possibleBlocks.append((r,c+1))
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == 0 and board[r][c + 3] == piece: #XXOX
                if (isInRange(board,r,c+2) and isValidBlockingMove(board,r,c+2)):
                    possibleBlocks.append((r,c+2))

    # Check positively sloped diaganols for gapped block
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == 0 and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece: #XOXX
                if (isInRange(board,r+1,c+1) and isValidBlockingMove(board,r+1,c+1)):
                    possibleBlocks.append((r+1,c+1))
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == 0 and board[r + 3][c + 3] == piece: #XXOX
                if (isInRange(board,r+2,c+2) and isValidBlockingMove(board,r+2,c+2)):
                    possibleBlocks.append((r+2,c+2))

    # Check negatively sloped diaganols for gapped block
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == 0 and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece: #XOXX
                if (isInRange(board,r-1,c+1) and isValidBlockingMove(board,r-1,c+1)):
                    possibleBlocks.append((r-1,c+1))
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == 0 and board[r - 3][c + 3] == piece: #XXOX
                if (isInRange(board,r-2,c+2) and isValidBlockingMove(board,r-2,c+2)):
                    possibleBlocks.append((r-2,c+2))

    print("possible blocks")
    print(possibleBlocks)

    if (len(possibleBlocks) > 0):
        return possibleBlocks[0][1] # return the col of the first item
    return None
    



def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score


def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score


def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid(board, col):
			valid_locations.append(col)
	return valid_locations

def is_terminal_node(board):
	return check_win(board, PLAYER_PIECE) or check_win(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if check_win(board, AI_PIECE):
				return (None, 100000000000000)
			elif check_win(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col






















def play():
    game_over = False
    game_turns = 0
    turn = 0
    board = create_board()
    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()
    print("In play method - ai_type = " + str(ai_type))
    NotValidCols = set()
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

            validPlayerMove = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                if turn == PLAYER:
                    positionx = event.pos[0]
                    col = int(math.floor(positionx / SQUARESIZE))
                    pygame.display.update()

                    if is_valid(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)
                        validPlayerMove = True

                    if validPlayerMove == True:
                        if game_turns > 3 and check_win(board, PLAYER_PIECE):
                            label = my_font.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40,10))
                            game_over = True
                        game_turns += 1
                        turn += 1
                        turn = turn % 2
                        print_board(board)
                        draw_board(board)
        if turn == AI and not game_over:
            if ai_type == RANDOM_AI:
                col = randrange(0, 7)
                while not is_valid(board, col):
                    col = randrange(0, 7)
                if is_valid(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)
                    if game_turns > 3 and check_win(board, AI_PIECE):
                        label = my_font.render("Random AI wins!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        game_over = True
                    game_turns += 1
                    turn += 1
                    turn = turn % 2
                    print_board(board)
                    draw_board(board)
            elif ai_type == BLOCKING_AI:
                blockCol = checkThreeInARow(board, PLAYER_PIECE)
                print("Return from checkThreeInARow")
                print(blockCol)
                if (blockCol != None and is_valid(board, blockCol)):
                    row = get_next_open_row(board, blockCol)
                    drop_piece(board, row, blockCol, AI_PIECE)
                else: #random ai move
                    if (blockCol):
                        NotValidCols.add(blockCol)
                    while (True):
                        col = randrange(0, 7)
                        if (col not in NotValidCols and is_valid(board, col)):
                            break
                    if is_valid(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, AI_PIECE)
                    else:
                        NotValidCols.add(col)
                if game_turns > 3 and check_win(board, AI_PIECE):
                    label = my_font.render("Blocking AI wins!", 1, YELLOW)
                    screen.blit(label, (40,10))
                    game_over = True
                game_turns += 1
                turn += 1
                turn = turn % 2
                print_board(board)
                draw_board(board)
            if (game_turns == 42 and game_over == False):
                print("This is a draw!")
                label = my_font.render("Draw!!!", 1, BLUE)
                screen.blit(label, (40,10))
                game_over = True
                print_board(board)
                draw_board(board)
            elif ai_type == STATE_SPACE_SEARCH:
                #col = random.randint(0, COLUMN_COUNT-1)
		        #col = pick_best_move(board, AI_PIECE)
                col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
                if is_valid(board, col):
			        #pygame.time.wait(500)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)
                    if check_win(board, AI_PIECE):
                        label = my_font.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        game_over = True
                        
                    print_board(board)
                    draw_board(board)
                    
                    turn += 1
                    turn = turn % 2

        if game_over:
            pygame.time.wait(5000)


#Welcome Screen and Menu
mainmenu = pygame_menu.Menu('Welcome', HEIGHT, WIDTH, theme=themes.THEME_DARK)
mainmenu.add.button('Play', start_game)
mainmenu.add.button('AI Settings', ai_player_type_menu)

ai = pygame_menu.Menu('Select a style of AI player', HEIGHT, WIDTH, theme=themes.THEME_DARK)
ai.add.selector('Styles: ', [('Random', 1), ('Blocking', 2), ('State Space Search', 3)], default=1, onchange=set_ai)

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
