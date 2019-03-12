import numpy as np
import random
import pygame
import sys
import math

#### MACROS ####

RED = (237, 37, 78)
YELLOW = (249, 220, 92)
BLUE = (34, 108, 224)
BLACK = (0, 0, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1
turn = random.randint(0, 1)

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

h1 = False

game_over = False
option_to_remove = True
board = np.zeros((ROW_COUNT, COLUMN_COUNT))
nodes_searched = 0
bad_setup = False

#### SETUP ####

print("_"*30)
print("-"*8 + "Connect-4 Menu" + "-"*8)
print("_"*30)

try:
    game_type = int(input("\nHow many AIs? 1 or 2: "))

    comp_vs_comp_easy = False
    comp_vs_comp_med = False
    comp_vs_comp_perf = False

    if game_type == 2:
        ai_type = int(
            input("Do you want the smart AI to play a dumb (1) or avg AI (2) or smart AI (3)? "))
        if ai_type == 1:
            comp_vs_comp_easy = True
        elif ai_type == 2:
            comp_vs_comp_med = True
        elif ai_type == 3:
            comp_vs_comp_perf = True
        else:
            raise ValueError
    elif game_type != 1:
        raise ValueError

    heuristic = int(input("Offensive (1) or defensive (2) heuristic? "))
    if heuristic == 1:
        h1 = True
    elif heuristic == 2:
        h1 = False
    else:
        raise ValueError

    if comp_vs_comp_perf:
        option_to_remove = False
    else:
        option = input("Option to remove? Type no, else any key: ")
        if option_to_remove == "no":
            option_to_remove = False

except ValueError:
    print("Error please try again and follow directions from CLI.")
    bad_setup = True

#### GAME FUNCTIONS ####


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def remove_bottom_peg(board, col):
    for i in range(0, 5):
        board[i, col] = board[i+1, col]


def is_valid_location(board, col):
    return not np.all(board[:, col])


def can_remove(board, col, piece):
    return board[0][col] == piece


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def get_valid_removals(board, piece):
    valid_removals = []
    for col in range(COLUMN_COUNT):
        if can_remove(board, col, piece):
            valid_removals.append(col)
    return valid_removals


def print_board(board):
    print(np.flip(board, 0), end='\n\n')


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r *
                                            SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(
                c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()

#### AI FUNCTIONS ####


def winning_move(board, piece):

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # Check horizontal locations for win
            if c < COLUMN_COUNT - 3:
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

            # Check vertical locations for win
            if r < ROW_COUNT - 3:
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

            # Check positively sloped diagonals
            if c < COLUMN_COUNT - 3 and r < ROW_COUNT - 3:
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

            # Check negatively sloped diagonals
            try:
                if c < COLUMN_COUNT - 3:
                    if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                        return True
            except IndexError:
                pass

def offence(window, piece):
    # Heuristic 1
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
        score -= 3

    return score


def defence(window, piece):
    # Heuristic 2
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

    if window.count(opp_piece) == 4:
        score -= 5
    elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score -= 1

    return score


def score_position(board, piece):
    # Handle Heuristic
    score = 0
    block = 0

    # Score center column highly, best opportunity
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += offence(window, piece)
            block += defence(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += offence(window, piece)
            block += defence(window, piece)

    # Score diagonals
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            # positive slope
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += offence(window, piece)
            block += defence(window, piece)

            # negative slope
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += offence(window, piece)
            block += defence(window, piece)

    if h1:
        return score
    return block


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    global nodes_searched
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -np.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            nodes_searched += 1
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]

            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)

            if alpha >= beta:
                # Beta cutoff
                # Killer heuristic can be implemented here
                break

        return column, value

    else:  # Minimizing player
        value = np.inf
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
                # alpha cutoff
                break

        return column, value


if not bad_setup:
    #### PYGAME SETUP ####
    pygame.init()

    screen = pygame.display.set_mode(size)
    myfont = pygame.font.SysFont("ariel", 75)

    print_board(board)
    draw_board(board)
    pygame.display.update()

    #### GAME LOGIC ####

    # COMP VS HUMAN #
    if not comp_vs_comp_easy and not comp_vs_comp_med and not comp_vs_comp_perf:
        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if turn == PLAYER:
                        pygame.draw.circle(
                            screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

                pygame.display.update()

                if turn == PLAYER:

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_d:
                            pygame.draw.rect(
                                screen, BLACK, (0, 0, width, SQUARESIZE))

                            col = int(math.floor(posx/SQUARESIZE))

                            if can_remove(board, col, PLAYER_PIECE):
                                row = 0
                                remove_bottom_peg(board, col)

                                if winning_move(board, PLAYER_PIECE):
                                    label = myfont.render(
                                        "Player wins!", 1, RED)
                                    screen.blit(label, (40, 40))
                                    game_over = True

                                turn += 1
                                turn = turn % 2

                                print_board(board)
                                draw_board(board)

                        elif event.key == pygame.K_a:
                            pygame.draw.rect(
                                screen, BLACK, (0, 0, width, SQUARESIZE))

                            col = int(math.floor(posx/SQUARESIZE))

                            if is_valid_location(board, col):
                                row = get_next_open_row(board, col)
                                drop_piece(board, row, col, PLAYER_PIECE)

                                if winning_move(board, PLAYER_PIECE):
                                    label = myfont.render(
                                        "Player wins!", 1, RED)
                                    screen.blit(label, (40, 40))
                                    game_over = True

                                turn += 1
                                turn = turn % 2

                                print_board(board)
                                draw_board(board)

            if turn == AI and not game_over:
                col, minimax_score = minimax(board, 5, -np.inf, np.inf, True)

                if is_valid_location(board, col):

                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)

                    if winning_move(board, AI_PIECE):
                        label = myfont.render("AI wins!", 1, YELLOW)
                        screen.blit(label, (40, 40))
                        game_over = True

                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2

            pygame.time.wait(400)

            if game_over:
                pygame.time.wait(3000)

    # COMP VS COMP #
    elif comp_vs_comp_easy:
        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if turn == PLAYER:

                chance = random.randint(0, 10)
                col = random.randint(0, COLUMN_COUNT-1)

                if chance < 4 and option_to_remove:
                    # Find a peg to remove
                    if len(get_valid_removals(board, PLAYER_PIECE)) > 0:
                        col = get_valid_removals(board, PLAYER_PIECE)[0]
                        remove_bottom_peg(board, col)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Dumb AI wins!", 1, RED)
                            screen.blit(label, (40, 40))
                            game_over = True

                            print_board(board)
                            draw_board(board)

                            turn += 1
                            turn = turn % 2

                elif is_valid_location(board, col) and turn == PLAYER:
                    # try to drop a peg in a random open spot
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Dumb AI wins!", 1, RED)
                        screen.blit(label, (40, 40))
                        game_over = True

                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2

            if turn == AI and not game_over:

                col, minimax_score = minimax(
                    board, 5, -np.inf, np.inf, True)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)

                    if winning_move(board, AI_PIECE):
                        label = myfont.render("Smart AI wins!", 1, YELLOW)
                        screen.blit(label, (40, 40))
                        game_over = True

                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2

            pygame.time.wait(200)

            if game_over:
                pygame.time.wait(3000)

    # COMP VS COMP #
    elif comp_vs_comp_med:
        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if turn == PLAYER:

                chance = random.randint(0, 10)
                col, minimax_score = minimax(
                    board, 1, -np.inf, np.inf, True)

                if chance < 4 and option_to_remove:
                    # Find a peg to remove
                    if len(get_valid_removals(board, PLAYER_PIECE)) > 0:
                        col = get_valid_removals(board, PLAYER_PIECE)[0]
                        remove_bottom_peg(board, col)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Avg AI wins!", 1, RED)
                            screen.blit(label, (40, 40))
                            game_over = True

                            print_board(board)
                            draw_board(board)

                            turn += 1
                            turn = turn % 2

                elif is_valid_location(board, col):
                    # try to drop a peg in a random open spot
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Avg AI wins!", 1, RED)
                        screen.blit(label, (40, 40))
                        game_over = True

                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2

            if turn == AI and not game_over:

                col, minimax_score = minimax(
                    board, 5, -np.inf, np.inf, True)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)

                    if winning_move(board, AI_PIECE):
                        label = myfont.render("Smart AI wins!", 1, YELLOW)
                        screen.blit(label, (40, 40))
                        game_over = True

                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2

            pygame.time.wait(100)

            if game_over:
                pygame.time.wait(3000)

    # COMP VS COMP #
    elif comp_vs_comp_perf:
        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if len(get_valid_locations(board)) == 0:
                print("It's a tie!")
                game_over = True

            elif turn == PLAYER:
                h1 = True
                col, minimax_score = minimax(
                    board, 5, -np.inf, np.inf, False)

                if is_valid_location(board, col):

                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Smart1 AI wins!", 1, RED)
                        screen.blit(label, (40, 40))
                        game_over = True

                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2

            if turn == AI and not game_over:
                h1 = False
                col, minimax_score = minimax(
                    board, 5, -np.inf, np.inf, True)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)

                    if winning_move(board, AI_PIECE):
                        label = myfont.render("Smart2 AI wins!", 1, YELLOW)
                        screen.blit(label, (40, 40))
                        game_over = True

                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2

            if game_over:
                pygame.time.wait(3000)

    print("Game complete, {} nodes searched.".format(nodes_searched))
