import numpy as np
import pygame
import sys

RED = ()
BLUE = (34,108, 224)
BLACK = (27,23,37)

ROWS = 6
COLS = 7

def remove_bottom_peg(board, col):
    top = get_open_row(board, col)
    shift = np.copy(board[1:, col])
    board[0:ROWS-1, col] = shift
    # edge case handler
    board[ROWS-1, col] = 0 

def check_win(board, player):

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

def get_open_row(board, col):
    for row in range(ROWS):
        if(board[row,col] == 0):
            return row

def valid_move(board, col):
	return board[ROWS-1][col] == 0

def make_move(board, row, col, player):
    # player is 1 or 2
    board[row][col] = player

def print_board(board):
    # CMD output
    # orient so 0,0 is at the bottom left
    print(np.flip(board, 0))

def draw_board(board):
    # pygame screen
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARE, r*SQUARE+SQUARE, SQUARE, SQUARE))
            pygame.draw.circle(screen, BLACK, (c*SQUARE+SQUARE//2, r*SQUARE+SQUARE+SQUARE//2), RADIUS)

board = np.zeros((ROWS,COLS))
option_to_remove = False # default to conventional connect-4 game
running = True
turn = False # binary track of turn starting with Player 1

pygame.init()

SQUARE = 100 #px
RADIUS = int(SQUARE/2 -5)

width = COLS * SQUARE
height = (ROWS+1) * SQUARE

size = (width, height)
screen = pygame.display.set_mode(size)

draw_board(board)
pygame.display.update()
'''
option = input("Would you like to play with the option to remove pegs? y/n: ")
if(option.upper() == 'Y'):
    option_to_remove = True
'''
while running:

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = false
        
        if(event.type == pygame.MOUSEBUTTONDOWN):
            print(event.pos)
            """
            if(not turn):
                move = int(input("Player 1, make your move (0-6): "))
                if(board[0][move] == 1):
                    move_type = int(input("Would you like to drop a peg here or remove your bottom peg? 1 or 2: "))
                    if(move_type == 2):
                        remove_bottom_peg(board, move)
                        print_board(board)
                    else:
                        if(valid_move(board, move)):
                            row = get_open_row(board, move)
                            make_move(board, row, move, 1)
                            if(check_win(board, 1)):
                                print("P1 wins! P2 ur a sucka")
                                running = False
                        else:
                            print("invalid move, you loss your turn")
                else:
                    if(valid_move(board, move)):
                        row = get_open_row(board, move)
                        make_move(board, row, move, 1)
                        if(check_win(board, 1)):
                            print("P1 wins! P2 ur a sucka")
                            running = False
                    else:
                        print("invalid move, you loss your turn")
            else:
                move = int(input("Player 2, make your move (0-6): "))
                if(board[0][move] == 2):
                    move_type = int(input("Would you like to drop a peg here or remove your bottom peg? 1 or 2: "))
                    if(move_type == 2):
                        remove_bottom_peg(board, move)
                    else:
                        if(valid_move(board, move)):
                            row = get_open_row(board, move)
                            make_move(board, row, move, 2)
                            if(check_win(board, 2)):
                                print("P2 wins! P1 ur a sucka")
                                running = False
                        else:
                            print("invalid move, you loss your turn")

                else:
                    if(valid_move(board, move)):
                        row = get_open_row(board, move)
                        make_move(board, row, move, 2)
                        if(check_win(board, 2)):
                            print("P2 wins! P1 ur a sucka")
                            running = False
                    else:
                        print("invalid move, you loss your turn")
            print_board(board)
            turn = not turn """
        pygame.quit()  # quits pygame
        sys.exit()
