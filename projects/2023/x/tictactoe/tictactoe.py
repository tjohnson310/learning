"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_x = 0
    num_o = 0
    for row in board:
        for row_item in row:
            if row_item == X:
                num_x += 1
            elif row_item == O:
                num_o += 1

    if num_o >= num_x:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = set()
    for i, row in enumerate(board):
        for j, row_item in enumerate(row):
            if row_item == EMPTY:
                all_actions.add((i, j))

    return all_actions


def result(board, action: tuple):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_new = copy.deepcopy(board)
    player_who = player(board)
    row = action[0]
    col = action[1]

    try:
        if board[row][col] == EMPTY:
            board_new[row][col] = player_who
            return board_new
        else:
            raise Exception('Player may not make a move in this square...')
    except IndexError:
        raise Exception('Player may not make a move in this square...')


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0] == row[1] == row[2]:
            return row[0]

    left_diag = board[0][0] == board[1][1] == board[2][2]
    right_diag = board[0][2] == board[1][1] == board[2][0]

    if left_diag:
        return board[0][0]
    elif right_diag:
        return board[0][2]
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    if EMPTY not in [item for sublist in board for item in sublist]:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    who_won = winner(board)
    if who_won == X:
        return 1
    elif who_won == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    whose_move = player(board)
    test_board = copy.deepcopy(board)

    def max_value(state, actions_values: list = None):
        if terminal(state):
            return utility(state)
        v = -math.inf
        for action in actions(state):
            actions_values.append((action, max_value(result(state, action), actions_values)))
            v = max(v, min_value(result(state, action)))
        return v

    def min_value(state, actions_values: tuple = None):
        if terminal(state):
            return utility(state)
        v = math.inf
        for action in actions(state):
            v = min(v, max_value(result(state, action)))
        return v

    if whose_move == X:
        max_player = True
    elif whose_move == O:
        max_player = False
    else:
        raise Exception("Invalid player option...")


if __name__ == "__main__":
    initial = initial_state()
    next_player = player(initial)
    all_available_actions = actions(initial)

    new_action = (2, 1)
    new_board = result(initial, new_action)
    print(new_board)
