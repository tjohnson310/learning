"""
Tic Tac Toe Player
"""

import math

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
    board_new = board
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
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError


if __name__ == "__main__":
    initial = initial_state()
    next_player = player(initial)
    all_available_actions = actions(initial)

    new_action = (2, 1)
    new_board = result(initial, new_action)
    print(new_board)
