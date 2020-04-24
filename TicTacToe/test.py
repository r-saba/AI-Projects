from tictactoe import player
from tictactoe import actions
from tictactoe import result
from tictactoe import winner
from tictactoe import terminal
from tictactoe import utility
from tictactoe import optimalMove
from tictactoe import minimax


import copy
import numpy as np
EMPTY = None

board = [[EMPTY, "X", "X"],
         [EMPTY, "O", EMPTY],
         ["O", "X", EMPTY]]
print(optimalMove(board))
