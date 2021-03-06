"""
Tic Tac Toe Player
"""

import math
import numpy as np
import copy
from random import randrange

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
    arr = np.array(board)
    xCount = np.count_nonzero(arr == "X")
    oCount = np.count_nonzero(arr == "O")
    return X if xCount == oCount else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    arr = np.array(board)
    possibleActionList = np.transpose(np.nonzero(arr == EMPTY))
    actionSet = set()

    for action in possibleActionList:
        actionSet.add(tuple(action))

    return actionSet


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    playerTurn = player(board)
    arr = copy.deepcopy(board)
    row = action[0]
    column = action[1]
    cellToUpdate = arr[row][column]

    if cellToUpdate != EMPTY:
        raise ValueError

    arr[row][column] = playerTurn
    return arr


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    """Look for winner in each row """
    for row in board:
        if row[0] == row[1] and row[0] == row[2] and (row[0] == X or row[0] == O):
            return X if row[0] == "X" else O

    """Look for winner in each column"""
    for x in range(3):
        if(board[0][x] == board[1][x] == board[2][x] and (board[0][x] == "X" or board[0][x] == "O")):
            return X if board[0][x] == "X" else O

    """Check for winner across"""
    if((board[0][0] == board[1][1] == board[2][2] and (board[1][1] == X or board[1][1] == O)) or (board[0][2] == board[1][1] == board[2][0] and (board[1][1] == X or board[1][1] == O))):
        return X if board[1][1] == "X" else O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if(winner(board) != None):
        return True

    arr = np.array(board)
    xCount = np.count_nonzero(arr == "X")
    oCount = np.count_nonzero(arr == "O")

    if xCount == 5 and oCount == 4:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    gameWinner = winner(board)
    if gameWinner == X:
        return 1
    elif gameWinner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if board == initial_state():
        return (randrange(3), randrange(3))

    # Player X should maximize the utility score
    # Chooses the action which would result in the largest score
    if player(board) == X:
        v = -math.inf
        move = (-10, -10)
        for action in actions(board):
            minv = MIN_VALUE(result(board, action))
            if (minv > v):
                v = minv
                move = action
        return move

    # Player O should minimize the utility score
    # Chooses the action which would result in the smallest score
    if player(board) == O:
        v = math.inf
        move = (10, 10)
        for action in actions(board):
            maxv = MAX_VALUE(result(board, action))
            if(maxv < v):
                v = maxv
                move = action
        return move


def MIN_VALUE(board):
    if (terminal(board)):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, MAX_VALUE(result(board, action)))
    return v


def MAX_VALUE(board):
    if (terminal(board)):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, MIN_VALUE(result(board, action)))
    return v
