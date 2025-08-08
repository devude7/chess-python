# Constants for endgame evaluation
CHECKMATE_WHITE = 100
CHECKMATE_BLACK = -100
DRAW = 0
STALEMATE = 'stalemate'
ONGOING = 'no'
BOARD_SIZE = 8

# Helper to quickly check if side has any legal moves
def has_any_legal_move(board, color):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            piece = board.pieces[y][x]
            if piece is not None and piece.color == color:
                for move in piece.valid_moves(board):
                    move_info = board.do_move(y, x, move[0], move[1])
                    if not is_in_check(board, color):
                        board.undo_move()
                        return True
                    board.undo_move()
    return False


# checks if game is over or draw
def terminate(board):
    # Checkmate or stalemate
    for color, mate_score in [('white', CHECKMATE_BLACK), ('black', CHECKMATE_WHITE)]:
        in_check = is_in_check(board, color)
        has_move = has_any_legal_move(board, color)
        if in_check and not has_move:
            return mate_score  # Checkmate
        if not in_check and not has_move:
            return STALEMATE   # Stalemate

    # Threefold repetition
    if board.is_repetition():
        return DRAW

    # Dead position draw detection
    # Gather piece types and their positions for each color
    piecesW, piecesB = [], []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            piece = board.pieces[y][x]
            if piece is not None:
                label = piece.piece_type
                if label == 'bishop':
                    label += '-even' if (x + y) % 2 == 0 else '-odd'
                if piece.color == 'white':
                    piecesW.append(label)
                else:
                    piecesB.append(label)
    # King vs King
    if piecesW == ['king'] and piecesB == ['king']:
        return DRAW
    # King and bishop/knight vs King
    if (piecesW == ['king', 'knight'] and piecesB == ['king']) or (piecesB == ['king', 'knight'] and piecesW == ['king']):
        return DRAW
    if (piecesW == ['king', 'bishop-even'] and piecesB == ['king']) or (piecesW == ['king', 'bishop-odd'] and piecesB == ['king']):
        return DRAW
    if (piecesB == ['king', 'bishop-even'] and piecesW == ['king']) or (piecesB == ['king', 'bishop-odd'] and piecesW == ['king']):
        return DRAW
    # King and bishop vs king and bishop, both bishops on same color
    if (set(piecesW) <= {'king', 'bishop-even'} and set(piecesB) <= {'king', 'bishop-even'}) or \
       (set(piecesW) <= {'king', 'bishop-odd'} and set(piecesB) <= {'king', 'bishop-odd'}):
        if len(piecesW) == 2 and len(piecesB) == 2:
            return DRAW

    return ONGOING


# checks if the king is in check
def is_in_check(board, color):
    king_pos = board.king_pos[color]
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            piece = board.pieces[y][x]
            if piece and piece.color != color:
                if king_pos in piece.valid_moves(board):
                    return True
    return False
    

def is_attacked(board, position, color):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            piece = board.pieces[y][x]
            if piece and piece.color != color and piece.piece_type != 'king':
                if position in piece.valid_moves(board):
                    return True
    return False
    

def promotion(board):
    if board.board_bottom == 'white':
        for col in range(BOARD_SIZE):
            piece = board.pieces[0][col]
            if piece and piece.piece_type == 'pawn' and piece.color == 'white':
                board.pieces[0][col] = Queen('white', 0, col)
            piece = board.pieces[7][col]
            if piece and piece.piece_type == 'pawn' and piece.color == 'black':
                board.pieces[7][col] = Queen('black', 7, col)

    elif board.board_bottom == 'black':
        for col in range(BOARD_SIZE):
            piece = board.pieces[7][col]
            if piece and piece.piece_type == 'pawn' and piece.color == 'white':
                board.pieces[7][col] = Queen('white', 7, col)
            piece = board.pieces[0][col]
            if piece and piece.piece_type == 'pawn' and piece.color == 'black':
                board.pieces[0][col] = Queen('black', 0, col)


# initializes the board with correct pieces
def starting_board(side):
        if side == 'black':
            return [[Rook('white', 0, 0), Knight('white', 0, 1), Bishop('white', 0, 2), King('white', 0, 3), Queen('white', 0, 4), Bishop('white', 0, 5), Knight('white', 0, 6), Rook('white', 0, 7)],
                    [Pawn('white', 1, 0), Pawn('white', 1, 1), Pawn('white', 1, 2), Pawn('white', 1, 3), Pawn('white', 1, 4), Pawn('white', 1, 5), Pawn('white', 1, 6), Pawn('white', 1, 7)],
                    [None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None],
                    [Pawn('black', 6, 0), Pawn('black', 6, 1), Pawn('black', 6, 2), Pawn('black', 6, 3), Pawn('black', 6, 4), Pawn('black', 6, 5), Pawn('black', 6, 6), Pawn('black', 6, 7)],
                    [Rook('black', 7, 0), Knight('black', 7, 1), Bishop('black', 7, 2), King('black', 7, 3), Queen('black', 7, 4), Bishop('black', 7, 5), Knight('black', 7, 6), Rook('black', 7, 7)]]
        elif side == 'white':
            return [[Rook('black', 0, 0), Knight('black', 0, 1), Bishop('black', 0, 2), Queen('black', 0, 3), King('black', 0, 4), Bishop('black', 0, 5), Knight('black', 0, 6), Rook('black', 0, 7)],
                    [Pawn('black', 1, 0), Pawn('black', 1, 1), Pawn('black', 1, 2), Pawn('black', 1, 3), Pawn('black', 1, 4), Pawn('black', 1, 5), Pawn('black', 1, 6), Pawn('black', 1, 7)],
                    [None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None],
                    [Pawn('white', 6, 0), Pawn('white', 6, 1), Pawn('white', 6, 2), Pawn('white', 6, 3), Pawn('white', 6, 4), Pawn('white', 6, 5), Pawn('white', 6, 6), Pawn('white', 6, 7)],
                    [Rook('white', 7, 0), Knight('white', 7, 1), Bishop('white', 7, 2), Queen('white', 7, 3), King('white', 7, 4), Bishop('white', 7, 5), Knight('white', 7, 6), Rook('white', 7, 7)]]


# resets en passant for all pawns so that the move can be only used in the next opponent's turn
def reset_en_passant(board, color):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board.pieces[y][x] != None and board.pieces[y][x].piece_type == 'pawn' and board.pieces[y][x].color == color:
                board.pieces[y][x].en_passant = False


# class for the board       
class Board:

    def __init__(self, side):
        self.board_bottom = side
        self.pieces = starting_board(side)
        self.history = []  
        self.move_stack = [] # for undo
        self.king_pos = {'white': None, 'black': None}
        self._init_king_positions()
    
    def _init_king_positions(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                piece = self.pieces[y][x]
                if piece and piece.piece_type == 'king':
                    self.king_pos[piece.color] = (y, x)


    def do_move(self, from_y, from_x, to_y, to_x):
        piece = self.pieces[from_y][from_x]
        captured = self.pieces[to_y][to_x]
        self.pieces[to_y][to_x] = piece
        self.pieces[from_y][from_x] = None

        # Track king position before and after
        old_king_pos = self.king_pos[piece.color]
        if piece.piece_type == 'king':
            self.king_pos[piece.color] = (to_y, to_x)

        move_info = (from_y, from_x, to_y, to_x, piece, captured, piece.y, piece.x, piece.first_move, old_king_pos)
        self.move_stack.append(move_info)
        piece.y = to_y
        piece.x = to_x
        piece.first_move = False
        return move_info

    def undo_move(self):
        move_info = self.move_stack.pop()
        extra = None
        if len(move_info) == 11:
            from_y, from_x, to_y, to_x, piece, captured, prev_y, prev_x, prev_first_move, prev_king_pos, extra = move_info
        else:
            from_y, from_x, to_y, to_x, piece, captured, prev_y, prev_x, prev_first_move, prev_king_pos = move_info

        self.pieces[from_y][from_x] = piece
        self.pieces[to_y][to_x] = captured
        piece.y = prev_y
        piece.x = prev_x
        piece.first_move = prev_first_move
        if piece.piece_type == 'king':
            self.king_pos[piece.color] = prev_king_pos

        # restore en passant captured pawn
        if extra and extra[0] == 'ep':
            _, cy, cx = extra
            pass


    def is_repetition(self):
        if self.history.count(self.pieces) >= 3:
            return True
        return False


# class for the pieces to inherit from
class Piece:

    def __init__(self, color, y, x):
        self.color = color
        self.y = y
        self.x = x
        self.image = ''
        self.first_move = True

    # General function for moving pieces (returns True if move was made)
    def move(self, y, x, board):

        legal = []
        for ty, tx in self.valid_moves(board):
            fy, fx = self.y, self.x
            info = board.do_move(fy, fx, ty, tx)
            if not is_in_check(board, self.color):
                legal.append((ty, tx))
            board.undo_move()

        if (y, x) not in legal:
            return False

        # --- EN PASSANT ---
        if self.piece_type == 'pawn':
            dy = y - self.y
            dx = x - self.x
            if abs(dx) == 1 and ((board.pieces[y][x] is None) or getattr(board.pieces[y][x], 'ghost', False)):
                cap_y = y + (1 if (board.board_bottom == 'white' and self.color == 'white') else
                            -1 if (board.board_bottom == 'white' and self.color == 'black') else
                            -1 if (board.board_bottom == 'black' and self.color == 'white') else
                            1)  
                captured = board.pieces[cap_y][x]
                if (captured is not None and captured.piece_type == 'pawn'
                        and captured.color != self.color and getattr(captured, 'en_passant', False)):
                    
                    info = board.do_move(self.y, self.x, y, x)
                    board.pieces[cap_y][x] = None
                    fy, fx, ty, tx, piece, cap, py, px, pfm, oldk = board.move_stack.pop()
                    board.move_stack.append((fy, fx, ty, tx, piece, cap, py, px, pfm, oldk, ('ep', cap_y, x)))
                    board.history.append([row[:] for row in board.pieces])
                    return True

        # --- CASTLING  ---
        if self.piece_type == 'king' and self.first_move:
            ky, kx = self.y, self.x
           
            if (y, x) in [(7,6), (7,2), (0,6), (0,2), (0,5), (0,1), (7,5), (7,1)]:  

                def castle(rook_from, rook_to):
                    board.do_move(ky, kx, y, x)
                    board.do_move(rook_from[0], rook_from[1], rook_to[0], rook_to[1])
                    board.history.append([row[:] for row in board.pieces])

                if self.color == 'white' and board.board_bottom == 'white':
                    if (y, x) == (7,6):  
                        castle((7,7), (7,5))
                        return True
                    if (y, x) == (7,2):  
                        castle((7,0), (7,3))
                        return True
                elif self.color == 'black' and board.board_bottom == 'white':
                    if (y, x) == (0,6):
                        castle((0,7), (0,5))
                        return True
                    if (y, x) == (0,2):
                        castle((0,0), (0,3))
                        return True
                elif self.color == 'white' and board.board_bottom == 'black':
                    if (y, x) == (0,5):
                        castle((0,7), (0,4))
                        return True
                    if (y, x) == (0,1):
                        castle((0,0), (0,2))
                        return True
                elif self.color == 'black' and board.board_bottom == 'black':
                    if (y, x) == (7,5):
                        castle((7,7), (7,4))
                        return True
                    if (y, x) == (7,1):
                        castle((7,0), (7,2))
                        return True

        # --- GENERAL MOVE ---
        board.do_move(self.y, self.x, y, x)
        board.history.append([row[:] for row in board.pieces])

        # set/reset en_passant flag for pawns 
        if self.piece_type == 'pawn':
            self.en_passant = (abs(y - (board.move_stack[-1][0])) == 2) 
        return True


    def move_test(self, y, x, board):
        if (y, x) in self.valid_moves(board):
            info = board.do_move(self.y, self.x, y, x)
            return True
        return False


    def incheck_move(self, y, x, board):
        legal = []
        for ty, tx in self.valid_moves(board):
            fy, fx = self.y, self.x
            info = board.do_move(fy, fx, ty, tx)
            if not is_in_check(board, self.color):
                legal.append((ty, tx))
            board.undo_move()
        if (y, x) in legal:
            board.do_move(self.y, self.x, y, x)
            board.history.append([row[:] for row in board.pieces])
            return True
        return False

        
class Pawn(Piece):

    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.piece_type = 'pawn'
        self.en_passant = False
        if self.color == 'white':
            self.image = 'w_pawn'
        else:
            self.image = 'b_pawn'

    def valid_moves(self, board):
        moves = []
        if board.board_bottom == 'white':
            if self.color == 'white':
                if self.first_move and board.pieces[self.y - 2][self.x] is None and board.pieces[self.y - 1][self.x] is None:
                    moves.append((self.y - 2, self.x))
                if board.pieces[self.y - 1][self.x] is None:
                    moves.append((self.y - 1, self.x))
                if self.y - 1 > -1 and self.x - 1 > -1 and board.pieces[self.y - 1][self.x - 1] is not None and board.pieces[self.y - 1][self.x - 1].color == 'black':
                    moves.append((self.y - 1, self.x - 1))
                if self.y - 1 > -1 and self.x + 1 < BOARD_SIZE and board.pieces[self.y - 1][self.x + 1] is not None and board.pieces[self.y - 1][self.x + 1].color == 'black':
                    moves.append((self.y - 1, self.x + 1))
                # en passant left
                if self.y > 0 and self.x - 1 > -1 and board.pieces[self.y][self.x - 1] is not None and board.pieces[self.y][self.x - 1].piece_type == 'pawn' and board.pieces[self.y][self.x - 1].color == 'black' and board.pieces[self.y][self.x - 1].en_passant:
                    moves.append((self.y - 1, self.x - 1))
                # en passant right
                if self.y > 0 and self.x + 1 < BOARD_SIZE and board.pieces[self.y][self.x + 1] is not None and board.pieces[self.y][self.x + 1].piece_type == 'pawn' and board.pieces[self.y][self.x + 1].color == 'black' and board.pieces[self.y][self.x + 1].en_passant:
                    moves.append((self.y - 1, self.x + 1))
            else:
                if self.first_move and board.pieces[self.y + 2][self.x] is None and board.pieces[self.y + 1][self.x] is None:
                    moves.append((self.y + 2, self.x))
                if self.y + 1 < BOARD_SIZE and board.pieces[self.y + 1][self.x] is None:
                    moves.append((self.y + 1, self.x))
                if self.y + 1 < BOARD_SIZE and self.x - 1 > -1 and board.pieces[self.y + 1][self.x - 1] is not None and board.pieces[self.y + 1][self.x - 1].color == 'white':
                    moves.append((self.y + 1, self.x - 1))
                if self.y + 1 < BOARD_SIZE and self.x + 1 < BOARD_SIZE and board.pieces[self.y + 1][self.x + 1] is not None and board.pieces[self.y + 1][self.x + 1].color == 'white':
                    moves.append((self.y + 1, self.x + 1))
                # en passant left
                if self.x - 1 > -1 and board.pieces[self.y][self.x - 1] is not None and board.pieces[self.y][self.x - 1].piece_type == 'pawn' and board.pieces[self.y][self.x - 1].color == 'white' and board.pieces[self.y][self.x - 1].en_passant:
                    moves.append((self.y + 1, self.x - 1))
                # en passant right
                if self.x + 1 < BOARD_SIZE and board.pieces[self.y][self.x + 1] is not None and board.pieces[self.y][self.x + 1].piece_type == 'pawn' and board.pieces[self.y][self.x + 1].color == 'white' and board.pieces[self.y][self.x + 1].en_passant:
                    moves.append((self.y + 1, self.x + 1))
        elif board.board_bottom == 'black':
            if self.color == 'white':
                if self.first_move and board.pieces[self.y + 2][self.x] is None and board.pieces[self.y + 1][self.x] is None:
                    moves.append((self.y + 2, self.x))
                if self.y + 1 < BOARD_SIZE and board.pieces[self.y + 1][self.x] is None:
                    moves.append((self.y + 1, self.x))
                if self.y + 1 < BOARD_SIZE and self.x - 1 > -1 and board.pieces[self.y + 1][self.x - 1] is not None and board.pieces[self.y + 1][self.x - 1].color == 'black':
                    moves.append((self.y + 1, self.x - 1))
                if self.y + 1 < BOARD_SIZE and self.x + 1 < BOARD_SIZE and board.pieces[self.y + 1][self.x + 1] is not None and board.pieces[self.y + 1][self.x + 1].color == 'black':
                    moves.append((self.y + 1, self.x + 1))
                if self.x - 1 > -1 and board.pieces[self.y][self.x - 1] is not None and board.pieces[self.y][self.x - 1].piece_type == 'pawn' and board.pieces[self.y][self.x - 1].color == 'black' and board.pieces[self.y][self.x - 1].en_passant:
                    moves.append((self.y + 1, self.x - 1))
                if self.x + 1 < BOARD_SIZE and board.pieces[self.y][self.x + 1] is not None and board.pieces[self.y][self.x + 1].piece_type == 'pawn' and board.pieces[self.y][self.x + 1].color == 'black' and board.pieces[self.y][self.x + 1].en_passant:
                    moves.append((self.y + 1, self.x + 1))
            else:
                if self.first_move and board.pieces[self.y - 2][self.x] is None and board.pieces[self.y - 1][self.x] is None:
                    moves.append((self.y - 2, self.x))
                if self.y - 1 > -1 and board.pieces[self.y - 1][self.x] is None:
                    moves.append((self.y - 1, self.x))
                if self.y - 1 > -1 and self.x - 1 > -1 and board.pieces[self.y - 1][self.x - 1] is not None and board.pieces[self.y - 1][self.x - 1].color == 'white':
                    moves.append((self.y - 1, self.x - 1))
                if self.y - 1 > -1 and self.x + 1 < BOARD_SIZE and board.pieces[self.y - 1][self.x + 1] is not None and board.pieces[self.y - 1][self.x + 1].color == 'white':
                    moves.append((self.y - 1, self.x + 1))
                if self.x - 1 > -1 and board.pieces[self.y][self.x - 1] is not None and board.pieces[self.y][self.x - 1].piece_type == 'pawn' and board.pieces[self.y][self.x - 1].color == 'white' and board.pieces[self.y][self.x - 1].en_passant:
                    moves.append((self.y - 1, self.x - 1))
                if self.x + 1 < BOARD_SIZE and board.pieces[self.y][self.x + 1] is not None and board.pieces[self.y][self.x + 1].piece_type == 'pawn' and board.pieces[self.y][self.x + 1].color == 'white' and board.pieces[self.y][self.x + 1].en_passant:
                    moves.append((self.y - 1, self.x + 1))

        moves = [(r, c) for (r, c) in moves if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE]
        return moves

    def incheck_valid_moves(self, board):
        valid = []
        for move_to in self.valid_moves(board):
            from_y, from_x = self.y, self.x
            to_y, to_x = move_to
            board.do_move(from_y, from_x, to_y, to_x)
            if not is_in_check(board, self.color):
                valid.append(move_to)
            board.undo_move()
        return valid

    
class Rook(Piece):

    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.piece_type = 'rook'
        if self.color == 'white':
            self.image = 'w_rook'
        else:
            self.image = 'b_rook'

    def valid_moves(self, board):
        moves = []

        # Check moves along the vertical direction
        for dy in [-1, 1]:
            y = self.y + dy
            while 0 <= y < BOARD_SIZE:
                piece_at_position = board.pieces[y][self.x]
                if piece_at_position is None:
                    moves.append((y, self.x))
                elif piece_at_position.color != self.color:
                    moves.append((y, self.x))
                    break
                else:
                    break
                y += dy

        # Check moves along the horizontal direction
        for dx in [-1, 1]:
            x = self.x + dx
            while 0 <= x < BOARD_SIZE:
                piece_at_position = board.pieces[self.y][x]
                if piece_at_position is None:
                    moves.append((self.y, x))
                elif piece_at_position.color != self.color:
                    moves.append((self.y, x))
                    break
                else:
                    break
                x += dx

        return moves

    def incheck_valid_moves(self, board):
        valid = []
        for move_to in self.valid_moves(board):
            from_y, from_x = self.y, self.x
            to_y, to_x = move_to
            board.do_move(from_y, from_x, to_y, to_x)
            if not is_in_check(board, self.color):
                valid.append(move_to)
            board.undo_move()
        return valid 
        

class Knight(Piece):

    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.piece_type = 'knight'
        if self.color == 'white':
            self.image = 'w_knight'
        else:
            self.image = 'b_knight'

    def valid_moves(self, board):
        moves = []
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dy, dx in directions:
            new_y, new_x = self.y + dy, self.x + dx
            if 0 <= new_y < BOARD_SIZE and 0 <= new_x < BOARD_SIZE:
                piece_at_new_position = board.pieces[new_y][new_x]
                if piece_at_new_position is None or piece_at_new_position.color != self.color:
                    moves.append((new_y, new_x))
        return moves

    def incheck_valid_moves(self, board):
        valid = []
        for move_to in self.valid_moves(board):
            from_y, from_x = self.y, self.x
            to_y, to_x = move_to
            board.do_move(from_y, from_x, to_y, to_x)
            if not is_in_check(board, self.color):
                valid.append(move_to)
            board.undo_move()
        return valid
    

class Bishop(Piece):

    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.piece_type = 'bishop'
        if self.color == 'white':
            self.image = 'w_bishop'
        else:
            self.image = 'b_bishop'

    def valid_moves(self, board):
        moves = []

        # Check moves along the four diagonal directions
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dy, dx in directions:
            y, x = self.y + dy, self.x + dx
            while 0 <= y < BOARD_SIZE and 0 <= x < BOARD_SIZE:
                piece_at_position = board.pieces[y][x]
                if piece_at_position is None:
                    moves.append((y, x))
                elif piece_at_position.color != self.color:
                    moves.append((y, x))
                    break
                else:
                    break
                y += dy
                x += dx

        return moves

    def incheck_valid_moves(self, board):
        valid = []
        for move_to in self.valid_moves(board):
            from_y, from_x = self.y, self.x
            to_y, to_x = move_to
            board.do_move(from_y, from_x, to_y, to_x)
            if not is_in_check(board, self.color):
                valid.append(move_to)
            board.undo_move()
        return valid


class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.piece_type = 'queen'
        if self.color == 'white':
            self.image = 'w_queen'
        else:
            self.image = 'b_queen'

    def valid_moves(self, board):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for direction in directions:
            for i in range(1, BOARD_SIZE):
                new_y, new_x = self.y + i * direction[0], self.x + i * direction[1]

                if not (0 <= new_y < BOARD_SIZE and 0 <= new_x < BOARD_SIZE):
                    break

                piece = board.pieces[new_y][new_x]
                if piece is None:
                    moves.append((new_y, new_x))
                elif piece.color != self.color:
                    moves.append((new_y, new_x))
                    break
                else:
                    break

        return moves

    def incheck_valid_moves(self, board):
        valid = []
        for move_to in self.valid_moves(board):
            from_y, from_x = self.y, self.x
            to_y, to_x = move_to
            board.do_move(from_y, from_x, to_y, to_x)
            if not is_in_check(board, self.color):
                valid.append(move_to)
            board.undo_move()
        return valid


class King(Piece):

    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.piece_type = 'king'
        self.image = 'w_king' if self.color == 'white' else 'b_king'

    def valid_moves(self, board):
        moves = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                new_y, new_x = self.y + dy, self.x + dx
                if 0 <= new_y < BOARD_SIZE and 0 <= new_x < BOARD_SIZE:
                    piece = board.pieces[new_y][new_x]
                    if piece is None or piece.color != self.color:
                        moves.append((new_y, new_x))

        def can_castle(rook_pos, between, target, side_check_positions):
            rook = board.pieces[rook_pos[0]][rook_pos[1]]
            if (self.first_move and rook is not None and
                rook.piece_type == 'rook' and rook.color == self.color and rook.first_move):
                # Squares between must be empty
                if all(board.pieces[y][x] is None for y, x in between):
                    # King can't castle out of, through, or into check
                    if not any(is_attacked(board, pos, self.color) for pos in side_check_positions):
                        moves.append(target)

        if self.color == 'white' and board.board_bottom == 'white':
            # Kingside: (7,4) to (7,6), Rook at (7,7)
            can_castle((7,7), [(7,5), (7,6)], (7,6), [(7,4), (7,5), (7,6)])
            # Queenside: (7,4) to (7,2), Rook at (7,0)
            can_castle((7,0), [(7,1), (7,2), (7,3)], (7,2), [(7,4), (7,3), (7,2)])
        elif self.color == 'black' and board.board_bottom == 'white':
            can_castle((0,7), [(0,5), (0,6)], (0,6), [(0,4), (0,5), (0,6)])
            can_castle((0,0), [(0,1), (0,2), (0,3)], (0,2), [(0,4), (0,3), (0,2)])
        elif self.color == 'white' and board.board_bottom == 'black':
            can_castle((0,7), [(0,5), (0,6), (0,4)], (0,5), [(0,4), (0,5)])
            can_castle((0,0), [(0,1), (0,2)], (0,1), [(0,4), (0,3), (0,2), (0,1)])
        elif self.color == 'black' and board.board_bottom == 'black':
            can_castle((7,7), [(7,5), (7,6), (7,4)], (7,5), [(7,4), (7,5)])
            can_castle((7,0), [(7,1), (7,2)], (7,1), [(7,4), (7,3), (7,2), (7,1)])

        return moves

    def move(self, y, x, board):
        valid = self.valid_moves(board)
        # Castling logic
        if (y, x) in valid and self.first_move:
            # White on bottom
            if self.color == 'white' and board.board_bottom == 'white':
                # Kingside
                if (y, x) == (7, 6):
                    board.do_move(self.y, self.x, 7, 6)  # King move
                    board.do_move(7, 7, 7, 5)            # Rook move
                    board.history.append([row[:] for row in board.pieces])
                    return True
                # Queenside
                if (y, x) == (7, 2):
                    board.do_move(self.y, self.x, 7, 2)
                    board.do_move(7, 0, 7, 3)
                    board.history.append([row[:] for row in board.pieces])
                    return True
            # Black on bottom
            elif self.color == 'black' and board.board_bottom == 'white':
                if (y, x) == (0, 6):
                    board.do_move(self.y, self.x, 0, 6)
                    board.do_move(0, 7, 0, 5)
                    board.history.append([row[:] for row in board.pieces])
                    return True
                if (y, x) == (0, 2):
                    board.do_move(self.y, self.x, 0, 2)
                    board.do_move(0, 0, 0, 3)
                    board.history.append([row[:] for row in board.pieces])
                    return True
            # White on top
            elif self.color == 'white' and board.board_bottom == 'black':
                if (y, x) == (0, 5):
                    board.do_move(self.y, self.x, 0, 5)
                    board.do_move(0, 7, 0, 4)
                    board.history.append([row[:] for row in board.pieces])
                    return True
                if (y, x) == (0, 1):
                    board.do_move(self.y, self.x, 0, 1)
                    board.do_move(0, 0, 0, 2)
                    board.history.append([row[:] for row in board.pieces])
                    return True
            # Black on top
            elif self.color == 'black' and board.board_bottom == 'black':
                if (y, x) == (7, 5):
                    board.do_move(self.y, self.x, 7, 5)
                    board.do_move(7, 7, 7, 4)
                    board.history.append([row[:] for row in board.pieces])
                    return True
                if (y, x) == (7, 1):
                    board.do_move(self.y, self.x, 7, 1)
                    board.do_move(7, 0, 7, 2)
                    board.history.append([row[:] for row in board.pieces])
                    return True

        # General move
        if (y, x) in valid:
            board.do_move(self.y, self.x, y, x)
            board.history.append([row[:] for row in board.pieces])
            return True
        else:
            return False

    def incheck_valid_moves(self, board):
        valid = []
        for move_to in self.valid_moves(board):
            from_y, from_x = self.y, self.x
            to_y, to_x = move_to
            board.do_move(from_y, from_x, to_y, to_x)
            if not is_in_check(board, self.color):
                valid.append(move_to)
            board.undo_move()
        return valid

    