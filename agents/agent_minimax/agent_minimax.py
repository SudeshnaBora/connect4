import numpy as np
from agents.common import common as cn
import math
from typing import Optional

# was struggling with switching between agent and \
# user input in players so introduced two variables

AGENT = cn.NO_PLAYER
HUMAN = cn.NO_PLAYER
# depth of the algorithm
GLOBAL_DEPTH = 3


def generate_move(board: np.ndarray, player: cn.BoardPiece,
                  saved_state: Optional) -> object:
    """
    Generate move function for the minimax agent

    :parameter board: the playing board of type np.ndarray
    :parameter player: the player making the move
    :parameter saved_state : Optional parameter to use the SavedState

    :return: a tuple containing column number and \
     maximizing score for next move
    """
    global AGENT
    global HUMAN

    # assuming that this will always get called by AGENT
    AGENT = player
    if AGENT == cn.PLAYER1:
        HUMAN = cn.PLAYER2
    else:
        HUMAN = cn.PLAYER1

    assert not HUMAN == cn.NO_PLAYER

    col, minimax_score = minimax(board, GLOBAL_DEPTH, -math.inf, math.inf, True)
    print('Column selected {} with score {}'.format(col, minimax_score))
    return col, saved_state


def score_row(board: np.ndarray, player: cn.BoardPiece) -> int:
    """
    Scores a row of the board.

    :parameter board: the playing board of type np.ndarray
    :parameter player: the player making the move

    :return: The score of the row
    """
    score = 0
    current_player = player
    if current_player == cn.PLAYER1:
        opposite_player = cn.PLAYER2
    else:
        opposite_player = cn.PLAYER1
    # loop through all rows. I may change it to get only the last open row
    for i in range(6):
        row = board[i, :]
        for col in range(4):
            current_slab = list(row[col:col + 4])
            count = current_slab.count(current_player)
            empty_count = current_slab.count(cn.NO_PLAYER)
            opponent_count = current_slab.count(opposite_player)
            if count == 4:
                score += 100
            if count == 3 and empty_count == 1:
                score += 5
            if count == 2 and empty_count == 1:
                score += 2
            if opponent_count == 3 and empty_count == 1:
                score -= 4
            if opponent_count == 4:
                score -= 100
    return score


def score_column(board: np.ndarray, player: cn.BoardPiece) -> int:
    """
    Scores the column of the board.

    :parameter board: the playing board of type np.ndarray
    :parameter player: the player making the move

    :return: The score of the column
    """
    score = 0
    opposite_player = player
    if player == cn.PLAYER1:
        opposite_player = cn.PLAYER2
    elif player == cn.PLAYER2:
        opposite_player = cn.PLAYER1
    for i in range(7):
        col = board[:, i]
        for j in range(3):
            current_slab = list(col[j:j + 4])
            count = current_slab.count(player)
            empty_count = current_slab.count(cn.NO_PLAYER)
            opponent_count = current_slab.count(opposite_player)
            if count == 4:
                score += 100
            if count == 3 and empty_count == 1:
                score += 5
            if count == 2 and empty_count == 1:
                score += 2
            if opponent_count == 3 and empty_count == 1:
                score -= 4
            if opponent_count == 4:
                score -= 100
    return score


def score_right_diagonal(board: np.ndarray, player: cn.BoardPiece) -> int:
    """
    Scores the right diagonal of the board

    :parameter board: the playing board of type np.ndarray
    :parameter player: the player making the move

    :return: The score of the right diagonal
    """
    score = 0
    opposite_player = player
    if player == cn.PLAYER1:
        opposite_player = cn.PLAYER2
    elif player == cn.PLAYER2:
        opposite_player = cn.PLAYER1
    for i in range(3):
        for j in range(4):
            for x in range(4):
                current_slab = [board[i + x][j + x] for x in range(4)]
            count = current_slab.count(player)
            empty_count = current_slab.count(cn.NO_PLAYER)
            opponent_count = current_slab.count(opposite_player)
            if count == 4:
                score += 100
            if count == 3 and empty_count == 1:
                score += 5
            if count == 2 and empty_count == 1:
                score += 2
            if opponent_count == 3 and empty_count == 1:
                score -= 4
            if opponent_count == 4:
                score -= 100
    return score


def score_left_diagonal(board: np.ndarray, player: cn.BoardPiece) -> int:
    """
    Scores the left diagonal of the board.

    :parameter board: the playing board of type np.ndarray
    :parameter player: the player making the move

    :return: The score of the left diagonal
    """
    score = 0
    opposite_player = player
    if player == cn.PLAYER1:
        opposite_player = cn.PLAYER2
    elif player == cn.PLAYER2:
        opposite_player = cn.PLAYER1
    for i in range(3):
        for j in range(4):
            for x in range(4):
                current_slab = [board[i + 3 - x][j + x] for x in range(4)]
            count = current_slab.count(player)
            empty_count = current_slab.count(cn.NO_PLAYER)
            opponent_count = current_slab.count(opposite_player)
            if count == 4:
                score += 100
            if count == 3 and empty_count == 1:
                score += 5
            if count == 2 and empty_count == 1:
                score += 2
            if opponent_count == 3 and empty_count == 1:
                score -= 4
            if opponent_count == 4:
                score -= 100
    return score


def heuristic_scoring(board: np.ndarray, player: cn.BoardPiece) -> int:
    """
    The heuristic scoring algorithm

    :parameter board: the playing board of type np.ndarray
    :parameter player: the player making the move

    :return: The heuristic score of the current board state for a player.
    """
    value = 0

    # check horizontal
    value += score_row(board, player)

    # check column
    value += score_column(board, player)

    # check right diagonal
    value += score_right_diagonal(board, player)

    # check left diagonal
    value += score_left_diagonal(board, player)

    return value


def minimax(board: np.ndarray, depth: int, alpha: int,
            beta: int, maximizing_player: bool) -> tuple:
    """
    Applies the minimax algorithm on the board to
    give a suggested column number and maximising/minimising score

    :parameter board: the playing board of type np.ndarray
    :parameter depth: the depth till which to evaluate the
     board with the algorithm
    :parameter alpha: the minimum score the maximising player is assured of
    :parameter beta: the maximum score the minimising player is assured of
    :parameter maximizing_player: boolean flag suggesting if the
    algorithm needs to maximise or minimise

    :return: The column and computed maximum/minimum score
    """
    # if depth is 0 or node is terminal, return heuristic value of the node
    # if terminal check if it is win , loss or draw
    if cn.connected_four(board, AGENT):
        return None, 10000
    if cn.connected_four(board, HUMAN):
        return None, -10000
    # Check if there is a draw
    if cn.check_end_state(board, AGENT) == cn.GameState.IS_DRAW:
        return None, 0
    # if depth is 0, calculate heuristic scoring
    if depth == 0:
        return None, heuristic_scoring(board, AGENT)

    # get a list of columns open for placement
    col_list = cn.get_free_columns(board)
    if maximizing_player:
        # value = -infinity
        value = -math.inf
        column = np.random.choice(col_list)
        # for child node (interpreted it as available columns)
        for col in col_list:
            # apply a random column to check the minimax
            b_copy, ori_board = cn.apply_player_action(board, col, AGENT, True)
            # get the score only
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            # personal debugging
            if depth == GLOBAL_DEPTH:
                print('For col {}, the score is {}'.format(col, new_score))
            # use the new score if higher
            if new_score > value:
                value = new_score
                column = col
            # prune in the maximising node
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    # minimising branch
    else:
        # value = +infinity
        value = math.inf
        column = np.random.choice(col_list)
        for col in col_list:
            b_copy, ori_board = cn.apply_player_action(board, col, HUMAN, True)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            # get the minimizing score
            if new_score < value:
                value = new_score
                column = col
            # do beta pruning check
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
