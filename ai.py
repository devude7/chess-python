from logic import terminate
import math
from copy import deepcopy

def action(board, move):

    new_board = deepcopy(board)

    # applying action to the copy
    new_board.pieces[move[0]][move[1]].move(move[2], move[3], new_board)
    return new_board


def score(board):

    term = terminate(board)
    if term in [100, -100]:
        return term
    if term in [0, 'stalemate']:
        return 0
    piece_values = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 0}
    score = 0
    for y in range(8):
        for x in range(8):
            if board.pieces[y][x] != None:
                color_multiplier = 1 if board.pieces[y][x].color == 'white' else -1
                score += color_multiplier * piece_values[board.pieces[y][x].piece_type]
    
    return score


def all_valid_moves(board, color):
    moves = []
    for y in range(8):
        for x in range(8):
            if board.pieces[y][x] != None and board.pieces[y][x].color == color:
                moves.append((y, x, board.pieces[y][x].incheck_valid_moves(board)))

    new_moves = [
        (x, y, sub_x, sub_y)
        for x, y, sublist in moves if sublist
        for sub_x, sub_y in sublist
    ]

    return new_moves

def Max_Value(board, value, color, depth):
    # maximizing player
    if depth == 0 or terminate(board) != 'no':
        return score(board)

    v = -math.inf
    if terminate(board) != 'no':
        return terminate(score)
    for move in all_valid_moves(board, color):
        v = max(v, Min_Value(action(board, move), value, 'black', depth-1))
        #Alpha-beta pruning. The 'value not in' part assures that it doesn't affect first move otherwise it wouldn't work properly 
        if v > value and value not in [-math.inf, math.inf]:
            return v
    return v


def Min_Value(board, value, color, depth):
    #minimizing player
    if depth == 0 or terminate(board) != 'no':
        return score(board)

    v = math.inf
    if terminate(board) != 'no':
        return terminate(score)
    for move in all_valid_moves(board, color):
        v = min(v, Max_Value(action(board, move), value, 'white', depth-1))
        #Alpha-beta pruning. The 'value not in' part assures that it doesn't affect first possible move otherwise it wouldn't work properly
        if v < value and value not in [-math.inf, math.inf]:
            return v
    return v



def minimax(board, depth, color, alpha=-math.inf, beta=math.inf):
    if depth == 0 or terminate(board) != 'no':
        return score(board), None

    best_move = None

    if color == 'white':
        max_eval = -math.inf
        for move in all_valid_moves(board, color):
            from_y, from_x, to_y, to_x = move
            board.do_move(from_y, from_x, to_y, to_x)
            eval, _ = minimax(board, depth-1, 'black', alpha, beta)
            board.undo_move()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = math.inf
        for move in all_valid_moves(board, color):
            from_y, from_x, to_y, to_x = move
            board.do_move(from_y, from_x, to_y, to_x)
            eval, _ = minimax(board, depth-1, 'white', alpha, beta)
            board.undo_move()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move