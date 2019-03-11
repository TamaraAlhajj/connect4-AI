import numpy as np
import sys
import pygame
import random

RED = (237, 37, 78)
YELLOW = (249, 220, 92)
BLUE = (34, 108, 224)
BLACK = (27, 23, 37)
WHITE = (255, 255, 255)

ROWS = 6
COLS = 7
WINDOW_LENGTH = 4

TURN = True  # binary track of turn
EMPTY = 0
PLAYER = 1
AI = 2

MSG = " wins! Good Game"
MSG_POS = (40, 40)

SQUARE = 100  # px
RADIUS = int(SQUARE/2 - 5)

WIDTH = COLS * SQUARE
HEIGHT = (ROWS + 1) * SQUARE  # top buffer row, 6 playable rows

SIZE = (WIDTH, HEIGHT)

board = np.zeros((ROWS, COLS))
running = True


## General functions ##

def valid_move(board, col):
    return board[ROWS-1][col] == EMPTY

def get_open_row(board, col):
    for row in range(ROWS):
        if(board[row, col] == EMPTY):
            return row

def remove_bottom_peg(board, col):
    top = get_open_row(board, col)
    shift = np.copy(board[1:, col])
    board[0:ROWS-1, col] = shift
    # edge case handler
    board[ROWS-1, col] = 0

def make_move(board, row, col, piece):
    board[row][col] = piece

def check_win(board, piece):
    
    # Check horizontal locations for win
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    """  
    for c in range(COLS):
        for r in range(ROWS):
            try:
                # Horizontal win
                if(board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player):
                    return True
            except IndexError:
                continue
            try:
                # Vertical win
                if(board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player):
                    return True
            except IndexError:
                continue
            try:
                # Upwards diagonal win
                if(board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player):
                    return True
            except IndexError:
                continue
            try:
                # Downward diagonal win
                if(board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player):
                    return True
            except IndexError:
                continue
    # ur not the weiner
    return False
    """

def print_board(board):
    # CMD output
    # orient so 0,0 is at the bottom left
    print(np.flip(board, 0))


def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARE, r *
                                            SQUARE+SQUARE, SQUARE, SQUARE))
            pygame.draw.circle(
                screen, BLACK, (int(c*SQUARE+SQUARE/2), int(r*SQUARE+SQUARE+SQUARE/2)), RADIUS)

    for c in range(COLS):
        for r in range(ROWS):
            if board[r][c] == PLAYER:
                pygame.draw.circle(
                    screen, RED, (int(c*SQUARE+SQUARE/2), HEIGHT-int(r*SQUARE+SQUARE/2)), RADIUS)
            elif board[r][c] == AI:
                pygame.draw.circle(screen, YELLOW, (int(
                    c*SQUARE+SQUARE/2), HEIGHT-int(r*SQUARE+SQUARE/2)), RADIUS)
    pygame.display.update()

## AI Functions ##

def evaluate_window(window, piece):
	score = 0

	if(window.count(piece) == 4):
		score += 100
	elif(window.count(piece) == 3 and window.count(EMPTY) == 1):
		score += 5
	elif(window.count(piece) == 2 and window.count(EMPTY) == 2):
		score += 2

	return score

def score_position(board, piece):
	score = 0

	## Score center column, which are best 
	center_array = [int(i) for i in list(board[:, COLS//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROWS):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLS-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLS):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROWS-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score diagonals
	for r in range(ROWS-3):
		for c in range(COLS-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROWS-3):
		for c in range(COLS-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def get_valid_moves(board):
    valid_locations = []
    for col in range(COLS):
        if(valid_move(board, col)):
            valid_locations.append(col)
    return valid_locations

def best_move(board, piece):
    valid_locations = get_valid_moves(board)
    best_score = -np.inf
    best_col = random.choice(valid_locations)

    for col in valid_locations:
        row = get_open_row(board, col)
        temp_board = board.copy()
        make_move(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        
        if(score > best_score):
            best_score = score
            best_col = col

    return best_col 

def minimax(node, depth, maximizingPlayer):
    """ if depth = 0 or node is a terminal node then
        return the heuristic value of node
    if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, minimax(child, depth − 1, FALSE))
        return value
    else (* minimizing player *)
        value := +∞
        for each child of node do
            value := min(value, minimax(child, depth − 1, TRUE))
        return value """

## Game play logic ##

option = input("Option to remove pegs? (yes): ")
if(option.upper() == 'YES'):
    option_to_remove = True
else:
    option_to_remove = False  # default to conventional connect-4 game

pygame.init()

screen = pygame.display.set_mode(SIZE)

draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("ariel", 75)

while running:

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False

        if(event.type == pygame.MOUSEMOTION and TURN):
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE))
            x = event.pos[0]
            pygame.draw.circle(screen, RED, (x, int(SQUARE/2)), RADIUS)

        if(event.type == pygame.KEYDOWN):
            print(event.unicode, event.key)
            # TODO below change mouse button down to KEYDOWN 1 or 2 for drop or remove

        if(event.type == pygame.MOUSEBUTTONDOWN):

            if(TURN and running):
                x = event.pos[0]
                move = x // SQUARE

                # if key is 2 remove
                if(board[0][move] == PLAYER and option_to_remove):
                    remove_bottom_peg(board, move)
                    turn = not turn

                    if(check_win(board, 1)):
                        label = font.render("Player" + MSG, 1, WHITE)
                        screen.blit(label, MSG_POS)
                        running = False

                    TURN = not TURN

                    print_board(board)
                    draw_board(board)

                # if key is 1 drop
                else:
                    if(valid_move(board, move)):
                        row = get_open_row(board, move)
                        make_move(board, row, move, PLAYER)

                        if(check_win(board, PLAYER)):
                            label = font.render("Player" + MSG, 1, WHITE)
                            screen.blit(label, MSG_POS)
                            running = False

                        TURN = not TURN

                        print_board(board)
                        draw_board(board)

    if(not TURN and running):

        # pick random column between 0 and 6 inclusive
        #move = random.randint(0, COLS - 1)

        move = best_move(board, AI)

        if(valid_move(board, move)):
            pygame.time.wait(500)
            row = get_open_row(board, move)
            make_move(board, row, move, AI)

            if(check_win(board, AI)):
                label = font.render("AI " + MSG, 1, YELLOW)
                screen.blit(label, MSG_POS)
                running = False

            TURN = not TURN

    print_board(board)
    draw_board(board)

    if(not running):
        pygame.time.wait(3000)

pygame.quit()  # quits pygame
sys.exit()
