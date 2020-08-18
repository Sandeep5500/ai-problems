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
    countx=0
    counto=0
    for row in board:
        for symbol in row:
            if symbol == X:
                countx+=1
            elif symbol == O:
                counto+=1
    if countx > counto:
        return O
    else:
        return X 


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY :
                actions.add((i,j))
    return actions         


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # print(f"{action}")
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError
    else:
        new_board = copy.deepcopy(board)
        new_board[action[0]][action[1]] = player(board)

    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0]==board[i][1] and board[i][1]==board[i][2] and board[i][0] != EMPTY:
            return board[i][0]    
    for j in range(3):
        if board[0][j]==board[1][j] and board[1][j]==board[2][j] and board[0][j] != EMPTY:
            return board[0][j]
    if board[0][0] == board[1][1] == board[2][2] or board[2][0] == board[1][1] == board[0][2] and board[1][1] != EMPTY:
        return board[1][1]              
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    else:
        for row in board:
            for element in row:
                if element == EMPTY:
                    return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if(player(board)== X):
        return Max(board)[0]
    elif(player(board)== O):
        return Min(board)[0]  

def Max(board):
    if(terminal(board)):
        return (None,utility(board))

    val = -2
    optimal_action = ()

    for action in actions(board):
        if (Min(result(board,action))[1] > val):
            val = Min(result(board,action))[1]
            optimal_action = action
            if val == 1:
                break
    
    return (optimal_action,val)

def Min(board):
    if(terminal(board)):
        return (None,utility(board))

    val = 2
    optimal_action = ()

    for action in actions(board):
        if (Max(result(board,action))[1] < val):
            val = Max(result(board,action))[1]
            optimal_action = action
            if val == -1:
                break

    return (optimal_action,val)

