import numpy as np

# Define constants
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2
ROW_COUNT = 6
COLUMN_COUNT = 7
WINNING_LENGTH = 4

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT - (WINNING_LENGTH - 1)):
        for r in range(ROW_COUNT):
            if all(board[r][c+c1] == piece for c1 in range(WINNING_LENGTH)):
                return True

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - (WINNING_LENGTH - 1)):
            if all(board[r+r1][c] == piece for r1 in range(WINNING_LENGTH)):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - (WINNING_LENGTH - 1)):
        for r in range(ROW_COUNT - (WINNING_LENGTH - 1)):
            if all(board[r+r1][c+c1] == piece for (r1, c1) in zip(range(WINNING_LENGTH), range(WINNING_LENGTH))):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - (WINNING_LENGTH - 1)):
        for r in range(WINNING_LENGTH - 1, ROW_COUNT):
            if all(board[r-r1][c+c1] == piece for (r1, c1) in zip(range(WINNING_LENGTH), range(WINNING_LENGTH))):
                return True

    return False

def print_board(board):
    print(np.flip(board, 0))

def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_1 if piece == PLAYER_2 else PLAYER_2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - (WINNING_LENGTH - 1)):
            window = row_array[c:c+WINNING_LENGTH]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - (WINNING_LENGTH - 1)):
            window = col_array[r:r+WINNING_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT - (WINNING_LENGTH - 1)):
        for c in range(COLUMN_COUNT - (WINNING_LENGTH - 1)):
            window = [board[r+i][c+i] for i in range(WINNING_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(ROW_COUNT - (WINNING_LENGTH - 1)):
        for c in range(COLUMN_COUNT - (WINNING_LENGTH - 1)):
            window = [board[r+i][c+3-i] for i in range(WINNING_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_1) or winning_move(board, PLAYER_2) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, PLAYER_2):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_1):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, PLAYER_2))

    if maximizing_player:
        value = -np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_2)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_1)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def main():
    board = create_board()
    game_over = False
    turn = 0

    print_board(board)
    while not game_over:
        if turn == 0:
            # Human player's turn
            col = int(input("Player 1 make your selection (0-6):"))
            if col not in range(COLUMN_COUNT) or not is_valid_location(board, col):
                print("Invalid move! Try again.")
                continue
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_1)
            if winning_move(board, PLAYER_1):
                print("Player 1 wins!")
                game_over = True
        else:
            # Computer player's turn
            col, _ = minimax(board, 5, -np.Inf, np.Inf, True)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_2)
            if winning_move(board, PLAYER_2):
                print("Player 2 wins!")
                game_over = True

        print_board(board)
        turn += 1
        turn %= 2

        if len(get_valid_locations(board)) == 0:
            print("It's a tie!")
            game_over = True

if __name__ == "__main__":
    main()
