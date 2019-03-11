import numpy as np
import sys
import pygame

RED = (237, 37, 78)
YELLOW = (249, 220, 92)
BLUE = (34, 108, 224)
BLACK = (27, 23, 37)
GREEN = (31, 140, 90)

ROWS = 7 # extra top row
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
        if(board[row, col] == 0):
            return row


def valid_move(board, col):
    return board[ROWS-2][col] == 0


def make_move(board, row, col, player):
    # player is 1 or 2
    board[row][col] = player


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
                if board[r][c] == 1:
                    pygame.draw.circle(
                        screen, RED, (int(c*SQUARE+SQUARE/2), height-int(r*SQUARE+SQUARE/2)), RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, YELLOW, (int(
                        c*SQUARE+SQUARE/2), height-int(r*SQUARE+SQUARE/2)), RADIUS)
        pygame.display.update()


board = np.zeros((ROWS, COLS))
option_to_remove = False  # default to conventional connect-4 game
running = True
turn = False  # binary track of turn starting with Player 1

pygame.init()

SQUARE = 100  # px
RADIUS = int(SQUARE/2 - 5)

width = COLS * SQUARE
height = ROWS * SQUARE

size = (width, height)
screen = pygame.display.set_mode(size)

draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("ariel", 75)

""" option = input("Option to remove pegs? y/n: ")
if(option.upper() == 'Y'):
    option_to_remove = True """

while running:

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False

        if(event.type == pygame.MOUSEBUTTONDOWN):

            if(not turn):
                x = event.pos[0]
                move = x // SQUARE

                if(board[0][move] == 1 and option_to_remove):
                    move_type = int(
                        input("Would you like to drop a peg here or remove your bottom peg? 1 or 2: "))
                    if(move_type == 2):
                        remove_bottom_peg(board, move)
                        print_board(board)
                    else:
                        if(valid_move(board, move)):
                            row = get_open_row(board, move)
                            make_move(board, row, move, 1)
                            if(check_win(board, 1)):
                                label = font.render(
                                    "Player 1 wins! GG", 1, RED)
                                screen.blit(label, (40, 10))
                                running = False
                        else:
                            #label = font.render("invalid move, miss a turn", 1, RED)
                            #screen.blit(label, (40, 10))
                else:
                    if(valid_move(board, move)):
                        row = get_open_row(board, move)
                        make_move(board, row, move, 1)
                        if(check_win(board, 1)):
                            label = font.render(
                                "Player 1 wins! GG", 1, RED)
                            screen.blit(label, (40, 10))
                            running = False
                    else:
                        #label = font.render("invalid move, miss a turn", 1, RED)
                        #screen.blit(label, (40, 10))
            else:
                x = event.pos[0]
                move = x // SQUARE

                if(board[0][move] == 2 and option_to_remove):
                    move_type = int(
                        input("Would you like to drop a peg here or remove your bottom peg? 1 or 2: "))
                    if(move_type == 2):
                        remove_bottom_peg(board, move)
                    else:
                        if(valid_move(board, move)):
                            row = get_open_row(board, move)
                            make_move(board, row, move, 2)
                            if(check_win(board, 2)):
                                label = font.render(
                                    "Player 2 wins! GG", 1, YELLOW)
                                screen.blit(label, (40, 10))
                                running = False
                        else:
                            #label = font.render("invalid move, miss a turn", 1, YELLOW)
                            #screen.blit(label, (40, 10))

                else:
                    if(valid_move(board, move)):
                        row = get_open_row(board, move)
                        make_move(board, row, move, 2)
                        if(check_win(board, 2)):
                            label = font.render(
                                "Player 2 wins! GG", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            running = False
                    else:
                        #label = font.render("invalid move, miss a turn", 1, YELLOW)
                        #screen.blit(label, (40, 10))


            print_board(board)
            draw_board(board)
            turn = not turn
            if(not running):
                screen.blit(label, (40, 10))
                pygame.time.wait(5000)

pygame.quit()  # quits pygame
sys.exit()
