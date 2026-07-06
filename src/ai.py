from .logic import CHECKMATE_BLACK, CHECKMATE_WHITE, DRAW, ONGOING, draw_status, is_in_check, legal_moves
import math


PIECE_VALUES = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 0}
MOVE_ORDER_VALUES = {'pawn': 10, 'knight': 30, 'bishop': 30, 'rook': 50, 'queen': 90, 'king': 1000}
EXACT = 'exact'
LOWER_BOUND = 'lower'
UPPER_BOUND = 'upper'


def score(board):
    score = 0
    for y in range(8):
        for x in range(8):
            if board.pieces[y][x] != None:
                color_multiplier = 1 if board.pieces[y][x].color == 'white' else -1
                score += color_multiplier * PIECE_VALUES[board.pieces[y][x].piece_type]
    
    return score


def no_moves_score(board, color):
    if is_in_check(board, color):
        return CHECKMATE_BLACK if color == 'white' else CHECKMATE_WHITE
    return 0


def board_key(board, color):
    pieces = []
    for y in range(8):
        for x in range(8):
            piece = board.pieces[y][x]
            if piece is None:
                pieces.append(None)
            else:
                pieces.append((
                    piece.color,
                    piece.piece_type,
                    piece.first_move,
                    getattr(piece, 'en_passant', False),
                ))

    return board.board_bottom, color, tuple(pieces)


def move_priority(board, move, cached_move=None):
    if move == cached_move:
        return 10000

    from_y, from_x, to_y, to_x = move
    piece = board.pieces[from_y][from_x]
    captured = board.pieces[to_y][to_x]
    priority = 0

    if captured is not None:
        attacker_value = MOVE_ORDER_VALUES[piece.piece_type]
        captured_value = MOVE_ORDER_VALUES[captured.piece_type]
        priority += 1000 + captured_value - attacker_value

    if piece.piece_type == 'pawn' and to_y in [0, 7]:
        priority += 900

    return priority


def ordered_moves(board, color, cached_move=None):
    moves = legal_moves(board, color)
    return sorted(moves, key=lambda move: move_priority(board, move, cached_move), reverse=True)


def minimax(board, depth, color, alpha=-math.inf, beta=math.inf, transposition_table=None):
    if transposition_table is None:
        transposition_table = {}

    original_alpha = alpha
    original_beta = beta
    key = board_key(board, color)
    cached_move = None
    cached = transposition_table.get(key)
    if cached is not None:
        cached_depth, cached_eval, cached_flag, cached_move = cached
        if cached_depth >= depth:
            if cached_flag == EXACT:
                return cached_eval, cached_move
            if cached_flag == LOWER_BOUND:
                alpha = max(alpha, cached_eval)
            elif cached_flag == UPPER_BOUND:
                beta = min(beta, cached_eval)
            if alpha >= beta:
                return cached_eval, cached_move

    draw_term = draw_status(board)
    if draw_term != ONGOING:
        transposition_table[key] = (depth, DRAW, EXACT, None)
        return DRAW, None
    if depth == 0:
        material_score = score(board)
        transposition_table[key] = (depth, material_score, EXACT, None)
        return material_score, None

    best_move = None
    moves = ordered_moves(board, color, cached_move)
    if not moves:
        end_score = no_moves_score(board, color)
        transposition_table[key] = (depth, end_score, EXACT, None)
        return end_score, None

    if color == 'white':
        max_eval = -math.inf
        for move in moves:
            from_y, from_x, to_y, to_x = move
            board.do_move(from_y, from_x, to_y, to_x)
            eval, _ = minimax(board, depth-1, 'black', alpha, beta, transposition_table)
            board.undo_move()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        if max_eval <= original_alpha:
            flag = UPPER_BOUND
        elif max_eval >= original_beta:
            flag = LOWER_BOUND
        else:
            flag = EXACT
        transposition_table[key] = (depth, max_eval, flag, best_move)
        return max_eval, best_move

    else:
        min_eval = math.inf
        for move in moves:
            from_y, from_x, to_y, to_x = move
            board.do_move(from_y, from_x, to_y, to_x)
            eval, _ = minimax(board, depth-1, 'white', alpha, beta, transposition_table)
            board.undo_move()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        if min_eval <= original_alpha:
            flag = UPPER_BOUND
        elif min_eval >= original_beta:
            flag = LOWER_BOUND
        else:
            flag = EXACT
        transposition_table[key] = (depth, min_eval, flag, best_move)
        return min_eval, best_move
