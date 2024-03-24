import copy

# checks if game is over or draw
def terminate(board):
    movesW = []
    movesB = []
    if is_in_check(board, 'white'):
        for y in range(8):
            for x in range(8):
                if board.pieces[y][x] != None and board.pieces[y][x].color == 'white':
                    movesW.append(board.pieces[y][x].incheck_valid_moves(board))
        movesW = [x for x in movesW if x]
        if len(movesW) < 1:                      
            return -100
    
    elif is_in_check(board, 'black'):
        for y in range(8):
            for x in range(8):
                if board.pieces[y][x] != None and board.pieces[y][x].color == 'black':
                    movesB.append(board.pieces[y][x].incheck_valid_moves(board))
        movesB = [x for x in movesB if x]
        if len(movesB) < 1:
            return 100
    elif not is_in_check(board, 'white') and not is_in_check(board, 'black'):
        movesW = []
        movesB = []
        for y in range(8):
            for x in range(8):
                if board.pieces[y][x] != None and board.pieces[y][x].color == 'white':
                    for move in board.pieces[y][x].valid_moves(board):
                        board_test = copy.deepcopy(board)
                        board_test.pieces[y][x].move_test(move[0], move[1], board_test)
                        if not is_in_check(board_test, 'white'):
                            movesW.append(move)
                if board.pieces[y][x] != None and board.pieces[y][x].color == 'black':
                    for move in board.pieces[y][x].valid_moves(board):
                        board_test = copy.deepcopy(board)
                        board_test.pieces[y][x].move_test(move[0], move[1], board_test)
                        if not is_in_check(board_test, 'black'):
                            movesB.append(move)                      
        movesW = [x for x in movesW if x]
        movesB = [x for x in movesB if x]
        if len(movesW) == 0 or len(movesB) == 0:
            return 'stalemate'
    elif board.is_repetition():
        return 0
    piecesW = []
    piecesB = []
    #dead position draws
    for y in range(8):
        for x in range(8):
            if board.pieces[y][x] != None and board.pieces[y][x].color == 'white':
                if board.pieces[y][x].piece_type == 'bishop' and (x + y) % 2 == 0:
                    piecesW.append('bishop-even')
                elif board.pieces[y][x].piece_type == 'bishop' and (x + y) % 2 != 0:
                    piecesW.append('bishop-odd')
                else:
                    piecesW.append(board.pieces[y][x].piece_type)
            if board.pieces[y][x] != None and board.pieces[y][x].color == 'black':
                if board.pieces[y][x].piece_type == 'bishop' and (x + y) % 2 == 0:
                    piecesB.append('bishop-even')
                elif board.pieces[y][x].piece_type == 'bishop' and (x + y) % 2 != 0:
                    piecesB.append('bishop-odd')
                else:
                    piecesB.append(board.pieces[y][x].piece_type)
    if len(piecesW) == 1 and len(piecesB) == 1:
        return 0
    if len(piecesW) == 2 and len(piecesB) == 1 and 'knight' in piecesW:
        return 0
    if len(piecesW) == 1 and len(piecesB) == 2 and 'knight' in piecesB:
        return 0
    if len(piecesW) == 2 and len(piecesB) == 1 and ('bishop-even' in piecesW or 'bishop-odd' in piecesW):
        return 0
    if len(piecesW) == 1 and len(piecesB) == 2 and ('bishop-even' in piecesB or 'bishop-odd' in piecesB):
        return 0
    if len(piecesW) == 2 and len(piecesB) == 2 and (('bishop-even' in piecesW and 'bishop-odd' in piecesB) or ('bishop-odd' in piecesW and 'bishop-even' in piecesB)):
        return 0
    
                             
    return 'no'


# checks if the king is in check
def is_in_check(board, color):
    moves = []
    for y in range(8):
        for x in range(8):
            if board.pieces[y][x] != None and board.pieces[y][x].color != color:
                moves += board.pieces[y][x].valid_moves(board)
            if board.pieces[y][x] != None and board.pieces[y][x].color == color and board.pieces[y][x].piece_type == 'king':
                king = (y, x)
    if king in moves:
        return True
    else: 
        return False
    

def is_attacked(board, position, color):
    attacked = []
    for y in range(8):
        for x in range(8):
            if board.pieces[y][x] != None and board.pieces[y][x].color != color and board.pieces[y][x].piece_type != 'king':
                attacked += board.pieces[y][x].valid_moves(board)
    if position in attacked:
        return True
    return False
    

def promotion(board):
    for i in range(8):
        if board.pieces[0][i] != None and board.pieces[0][i].piece_type == 'pawn' and board.pieces[0][i].color == 'white':
            board.pieces[0][i] = Queen('white', 0, i)
        if board.pieces[7][i] != None and board.pieces[7][i].piece_type == 'pawn' and board.pieces[7][i].color == 'white':
            board.pieces[7][i] = Queen('white', 7, i)
        if board.pieces[0][i] != None and board.pieces[0][i].piece_type == 'pawn' and board.pieces[0][i].color == 'black':
            board.pieces[0][i] = Queen('black', 0, i)
        if board.pieces[7][i] != None and board.pieces[7][i].piece_type == 'pawn' and board.pieces[7][i].color == 'black':
            board.pieces[7][i] = Queen('black', 7, i)

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
    for y in range(8):
        for x in range(8):
            if board.pieces[y][x] != None and board.pieces[y][x].piece_type == 'pawn' and board.pieces[y][x].color == color:
                board.pieces[y][x].en_passant = False


# class for the board       
class Board:

    def __init__(self, side):
        self.board_bottom = side
        self.pieces = starting_board(side)
        self.history = []  

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

    # general function for moving pieces
    def move(self, y, x, board):
        valid = []
        for move in self.valid_moves(board):
            board_test = copy.deepcopy(board)
            board_test.pieces[self.y][self.x].move_test(move[0], move[1], board_test)
            if not is_in_check(board_test, self.color):
                valid.append(move)
        # en passant setup(pawn normal moves)
        if self.piece_type == 'pawn' and (y, x) in valid and self.first_move and board.pieces[y][x] == None:
            if abs(self.y - y) == 2:
                board.pieces[self.y][self.x] = None
                board.pieces[y][x] = None
                self.x = x
                self.y = y
                board.pieces[y][x] = self
                self.first_move = False
                self.en_passant = True
                board.history.append([row[:] for row in board.pieces])
                return True
            else:
                board.pieces[self.y][self.x] = None
                board.pieces[y][x] = None
                self.x = x
                self.y = y
                board.pieces[y][x] = self
                self.first_move = False
                self.en_passant = False
                board.history.append([row[:] for row in board.pieces])
                return True
        # en passant capture
        if ((board.board_bottom == 'white' and self.color == 'white') or (board.board_bottom == 'black' and self.color == 'black')) and self.piece_type == 'pawn' and (y, x) in valid and board.pieces[y + 1][x] != None and board.pieces[y + 1][x].piece_type == 'pawn' and board.pieces[y + 1][x].color != self.color and board.pieces[y + 1][x].en_passant == True:
            board.pieces[y + 1][x] = None
            board.pieces[self.y][self.x] = None
            board.pieces[y][x] = None
            self.x = x
            self.y = y
            board.pieces[y][x] = self
            self.first_move = False
            return True
        if ((board.board_bottom == 'white' and self.color == 'black') or (board.board_bottom == 'black' and self.color == 'white')) and self.piece_type == 'pawn' and (y, x) in valid and board.pieces[y - 1][x] != None and board.pieces[y - 1][x].piece_type == 'pawn' and board.pieces[y - 1][x].color != self.color and board.pieces[y - 1][x].en_passant == True:
            board.pieces[y - 1][x] = None
            board.pieces[self.y][self.x] = None
            board.pieces[y][x] = None
            self.x = x
            self.y = y
            board.pieces[y][x] = self
            self.first_move = False
            return True
        # castling
        if self.piece_type == 'king' and (y, x) in valid and board.board_bottom == 'white' and self.color == 'white' and self.first_move:
            if x == 6:
                board.pieces[7][7].move(7, 5, board)
                board.pieces[self.y][self.x] = None
                board.pieces[y][x] = None
                self.x = x
                self.y = y
                board.pieces[y][x] = self
                self.first_move = False
                board.history.append([row[:] for row in board.pieces])
                return True
            elif x == 2:
                board.pieces[7][0].move(7, 3, board)
                board.pieces[self.y][self.x] = None
                board.pieces[y][x] = None
                self.x = x
                self.y = y
                board.pieces[y][x] = self
                self.first_move = False
                board.history.append([row[:] for row in board.pieces])
                return True
        if self.piece_type == 'king' and (y, x) in valid and board.board_bottom == 'white' and self.color == 'black' and self.first_move:
            if x == 6:
                board.pieces[0][7].move(0, 5, board)
                board.pieces[self.y][self.x] = None
                board.pieces[y][x] = None
                self.x = x
                self.y = y
                board.pieces[y][x] = self
                self.first_move = False
                board.history.append([row[:] for row in board.pieces])
                return True
            elif x == 2:
                board.pieces[0][0].move(0, 3, board)
                board.pieces[self.y][self.x] = None
                board.pieces[y][x] = None
                self.x = x
                self.y = y
                board.pieces[y][x] = self
                self.first_move = False
                board.history.append([row[:] for row in board.pieces])
                return True 
        if self.piece_type == 'king' and (y, x) in valid and board.board_bottom == 'black' and self.color == 'white' and self.first_move:
            if x == 5:
                board.pieces[0][7].move(0, 4, board)
                board.pieces[self.y][self.x] = None
                board.pieces[y][x] = None
                self.x = x
                self.y = y
                board.pieces[y][x] = self
                self.first_move = False
                board.history.append([row[:] for row in board.pieces])
                return True
            elif x == 1:
                board.pieces[0][0].move(0, 2, board)
                board.pieces[self.y][self.x] = None
                board.pieces[y][x] = None
                self.x = x
                self.y = y
                board.pieces[y][x] = self
                self.first_move = False
                board.history.append([row[:] for row in board.pieces])
                return True
        if self.piece_type == 'king' and (y, x) in valid and board.board_bottom == 'black' and self.color == 'black' and self.first_move:
            if x == 5:
                board.pieces[7][7].move(7, 4, board)
                board.pieces[self.y][self.x] = None
                board.pieces[y][x] = None
                self.x = x
                self.y = y
                board.pieces[y][x] = self
                self.first_move = False
                board.history.append([row[:] for row in board.pieces])
                return True
            elif x == 1:
                board.pieces[7][0].move(7, 2, board)
                board.pieces[self.y][self.x] = None
                board.pieces[y][x] = None
                self.x = x
                self.y = y
                board.pieces[y][x] = self
                self.first_move = False
                board.history.append([row[:] for row in board.pieces])
                return True
        # general move
        if (y, x) in valid:
            board.pieces[self.y][self.x] = None
            board.pieces[y][x] = None
            self.x = x
            self.y = y
            board.pieces[y][x] = self
            self.first_move = False
            board.history.append([row[:] for row in board.pieces])
            return True
        else:
            return False
        
    # to avoid endless loops (propably due to poor design :( ) 
    def move_test(self, y, x, board):
        if (y, x) in self.valid_moves(board):
            board.pieces[self.y][self.x] = None
            board.pieces[y][x] = None
            self.x = x
            self.y = y
            board.pieces[y][x] = self
            self.first_move = False
            board.history.append([row[:] for row in board.pieces])
            return True
        else:
            return False

    
    # function for moving pieces when in check
    def incheck_move(self, y, x, board):
        if (y, x) in self.incheck_valid_moves(board):
            board.pieces[self.y][self.x] = None
            board.pieces[y][x] = None
            self.x = x
            self.y = y
            board.pieces[y][x] = self
            self.first_move = False
            return True
        else:
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
                if self.first_move and board.pieces[self.y - 2][self.x] == None and board.pieces[self.y - 1][self.x] == None:
                    moves.append((self.y - 2, self.x))
                if board.pieces[self.y - 1][self.x] == None:
                    moves.append((self.y - 1, self.x))
                if self.y - 1 > -1 and board.pieces[self.y - 1][self.x - 1] != None and board.pieces[self.y - 1][self.x - 1].color == 'black':
                    moves.append((self.y - 1, self.x - 1))
                if self.x + 1 < 8 and board.pieces[self.y - 1][self.x + 1] != None and board.pieces[self.y - 1][self.x + 1].color == 'black':
                    moves.append((self.y - 1, self.x + 1))
                if self.x - 1 > -1 and board.pieces[self.y][self.x - 1] != None and board.pieces[self.y][self.x - 1].piece_type == 'pawn' and board.pieces[self.y][self.x - 1].color == 'black' and board.pieces[self.y][self.x - 1].en_passant == True:
                    moves.append((self.y - 1, self.x - 1))
                if self.x + 1 < 8 and board.pieces[self.y][self.x + 1] != None and board.pieces[self.y][self.x + 1].piece_type == 'pawn' and board.pieces[self.y][self.x + 1].color == 'black' and board.pieces[self.y][self.x + 1].en_passant == True:
                    moves.append((self.y - 1, self.x + 1))
            else:
                if self.first_move and board.pieces[self.y + 2][self.x] == None and board.pieces[self.y + 1][self.x] == None:
                    moves.append((self.y + 2, self.x))
                if  self.y +1 < 8 and board.pieces[self.y + 1][self.x] == None:
                    moves.append((self.y + 1, self.x))
                if self.y +1 < 8 and self.y + 1 < 8 and board.pieces[self.y + 1][self.x - 1] != None and board.pieces[self.y + 1][self.x - 1].color == 'white':
                    moves.append((self.y + 1, self.x - 1))
                if self.y +1 < 8 and self.x + 1 < 8 and board.pieces[self.y + 1][self.x + 1] != None and board.pieces[self.y + 1][self.x + 1].color == 'white':
                    moves.append((self.y + 1, self.x + 1))
                if self.x - 1 > -1 and board.pieces[self.y][self.x - 1] != None and board.pieces[self.y][self.x - 1].piece_type == 'pawn'and board.pieces[self.y][self.x - 1].color == 'white' and board.pieces[self.y][self.x - 1].en_passant == True:
                    moves.append((self.y + 1, self.x - 1))
                if self.x + 1 < 8 and board.pieces[self.y][self.x + 1] != None and board.pieces[self.y][self.x + 1].piece_type == 'pawn' and board.pieces[self.y][self.x + 1].color == 'white' and board.pieces[self.y][self.x + 1].en_passant == True:
                    moves.append((self.y + 1, self.x + 1))
        elif board.board_bottom == 'black':
            if self.color == 'white':
                if self.first_move and board.pieces[self.y + 2][self.x] == None and board.pieces[self.y + 1][self.x] == None:
                    moves.append((self.y + 2, self.x))
                if board.pieces[self.y + 1][self.x] == None:
                    moves.append((self.y + 1, self.x))
                if self.y + 1 < 8 and board.pieces[self.y + 1][self.x - 1] != None and board.pieces[self.y + 1][self.x - 1].color == 'black':
                    moves.append((self.y + 1, self.x - 1))
                if self.x + 1 < 8 and board.pieces[self.y + 1][self.x + 1] != None and board.pieces[self.y + 1][self.x + 1].color == 'black':
                    moves.append((self.y + 1, self.x + 1))
                if self.x - 1 > -1 and board.pieces[self.y][self.x - 1] != None and board.pieces[self.y][self.x - 1].piece_type == 'pawn' and board.pieces[self.y][self.x - 1].color == 'black' and board.pieces[self.y][self.x - 1].en_passant == True:
                    moves.append((self.y + 1, self.x - 1))
                if self.x + 1 < 8 and board.pieces[self.y][self.x + 1] != None and board.pieces[self.y][self.x + 1].piece_type == 'pawn' and board.pieces[self.y][self.x + 1].color == 'black' and board.pieces[self.y][self.x + 1].en_passant == True:
                    moves.append((self.y + 1, self.x + 1))
            else:
                if self.first_move and board.pieces[self.y - 2][self.x] == None and board.pieces[self.y - 1][self.x] == None:
                    moves.append((self.y - 2, self.x))
                if board.pieces[self.y - 1][self.x] == None:
                    moves.append((self.y - 1, self.x))
                if self.y - 1 > -1 and board.pieces[self.y - 1][self.x - 1] != None and board.pieces[self.y - 1][self.x - 1].color == 'white':
                    moves.append((self.y - 1, self.x - 1))
                if self.x + 1 < 8 and board.pieces[self.y - 1][self.x + 1] != None and board.pieces[self.y - 1][self.x + 1].color == 'white':
                    moves.append((self.y - 1, self.x + 1))
                if self.x - 1 > -1 and board.pieces[self.y][self.x - 1] != None and board.pieces[self.y][self.x - 1].piece_type == 'pawn' and board.pieces[self.y][self.x - 1].color == 'white' and board.pieces[self.y][self.x - 1].en_passant == True:
                    moves.append((self.y - 1, self.x - 1))
                if self.x + 1 < 8 and board.pieces[self.y][self.x + 1] != None and board.pieces[self.y][self.x + 1].piece_type == 'pawn' and board.pieces[self.y][self.x + 1].color == 'white' and board.pieces[self.y][self.x + 1].en_passant == True:
                    moves.append((self.y - 1, self.x + 1))
        
            
        for move in moves:
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                moves.remove(move)
          
        return moves
    
    def incheck_valid_moves(self, board):
        moves = self.valid_moves(board)
        valid = []
                
        for move in moves:
            board_test = copy.deepcopy(board)
            board_test.pieces[self.y][self.x].move(move[0], move[1], board_test)
            if not is_in_check(board_test, self.color):
                valid.append(move)
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
            while 0 <= y < 8:
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
            while 0 <= x < 8:
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
        moves = self.valid_moves(board)
        valid = []
                
        for move in moves:
            board_test = copy.deepcopy(board)
            board_test.pieces[self.y][self.x].move(move[0], move[1], board_test)
            if not is_in_check(board_test, self.color):
                valid.append(move)
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
            if 0 <= new_y < 8 and 0 <= new_x < 8:
                piece_at_new_position = board.pieces[new_y][new_x]
                if piece_at_new_position is None or piece_at_new_position.color != self.color:
                    moves.append((new_y, new_x))
        return moves
    
    def incheck_valid_moves(self, board):
        moves = self.valid_moves(board)
        valid = []
                
        for move in moves:
            board_test = copy.deepcopy(board)
            board_test.pieces[self.y][self.x].move(move[0], move[1], board_test)
            if not is_in_check(board_test, self.color):
                valid.append(move)
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
            while 0 <= y < 8 and 0 <= x < 8:
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
        moves = self.valid_moves(board)
        valid = []
                
        for move in moves:
            board_test = copy.deepcopy(board)
            board_test.pieces[self.y][self.x].move(move[0], move[1], board_test)
            if not is_in_check(board_test, self.color):
                valid.append(move)
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
                for i in range(1, 8):
                    new_y, new_x = self.y + i * direction[0], self.x + i * direction[1]

                    if not (0 <= new_y < 8 and 0 <= new_x < 8):
                        break

                    if board.pieces[new_y][new_x] is None:
                        moves.append((new_y, new_x))
                    elif board.pieces[new_y][new_x].color != self.color:
                        moves.append((new_y, new_x))
                        break
                    else:
                        break

            return moves
        
        def incheck_valid_moves(self, board):
            moves = self.valid_moves(board)
            valid = []
                    
            for move in moves:
                board_test = copy.deepcopy(board)
                board_test.pieces[self.y][self.x].move(move[0], move[1], board_test)
                if not is_in_check(board_test, self.color):
                    valid.append(move)
            return valid
    


class King(Piece):
    
        def __init__(self, color, x, y):
            super().__init__(color, x, y)
            self.piece_type = 'king'
            if self.color == 'white':
                self.image = 'w_king'
            else:
                self.image = 'b_king'

        def valid_moves(self, board):
            moves = []
            if self.y - 1 > -1 and self.x - 1 > -1 and (board.pieces[self.y - 1][self.x - 1] == None or board.pieces[self.y - 1][self.x - 1].color != self.color):
                moves.append((self.y - 1, self.x - 1))
            if self.y - 1 > -1 and (board.pieces[self.y - 1][self.x] == None or board.pieces[self.y - 1][self.x].color != self.color):
                moves.append((self.y - 1, self.x))
            if self.y - 1 > -1 and self.x + 1 < 8 and (board.pieces[self.y - 1][self.x + 1] == None or board.pieces[self.y - 1][self.x + 1].color != self.color):
                moves.append((self.y - 1, self.x + 1))
            if self.x - 1 > -1 and (board.pieces[self.y][self.x - 1] == None or board.pieces[self.y][self.x - 1].color != self.color):
                moves.append((self.y, self.x - 1))
            if self.x + 1 < 8 and (board.pieces[self.y][self.x + 1] == None or board.pieces[self.y][self.x + 1].color != self.color):
                moves.append((self.y, self.x + 1))
            if self.y + 1 < 8 and self.x - 1 > -1 and (board.pieces[self.y + 1][self.x - 1] == None or board.pieces[self.y + 1][self.x - 1].color != self.color):
                moves.append((self.y + 1, self.x - 1))
            if self.y + 1 < 8 and (board.pieces[self.y + 1][self.x] == None or board.pieces[self.y + 1][self.x].color != self.color):
                moves.append((self.y + 1, self.x))
            if self.y + 1 < 8 and self.x + 1 < 8 and (board.pieces[self.y + 1][self.x + 1] == None or board.pieces[self.y + 1][self.x + 1].color != self.color):
                moves.append((self.y + 1, self.x + 1))

            #castling
            if board.board_bottom == 'white':
                if self.color == 'white':
                    if self.first_move and board.pieces[7][7] != None and board.pieces[7][7].first_move and board.pieces[7][7].piece_type == 'rook' and board.pieces[7][7].color == 'white' and board.pieces[7][6] == None and board.pieces[7][5] == None and is_attacked(board, (self.y, self.x) ,'white') == False:
                        moves.append((7, 6))
                    if self.first_move and board.pieces[7][0] != None and board.pieces[7][0].first_move and board.pieces[7][0].piece_type == 'rook' and board.pieces[7][0].color == 'white' and board.pieces[7][1] == None and board.pieces[7][2] == None and board.pieces[7][3] == None and is_attacked(board, (self.y, self.x) ,'white') == False:
                        moves.append((7, 2))
                else:
                    if self.first_move and board.pieces[0][7] != None and board.pieces[0][7].first_move and board.pieces[0][7].piece_type == 'rook' and board.pieces[0][7].color == 'black' and board.pieces[0][6] == None and board.pieces[0][5] == None and is_attacked(board, (self.y, self.x) ,'black') == False:
                        moves.append((0, 6))
                    if self.first_move and board.pieces[0][0] != None and board.pieces[0][0].first_move and board.pieces[0][0].piece_type == 'rook' and board.pieces[0][0].color == 'black' and board.pieces[0][1] == None and board.pieces[0][2] == None and board.pieces[0][3] == None and is_attacked(board, (self.y, self.x) ,'black') == False:
                        moves.append((0, 2))
            elif board.board_bottom == 'black':
                if self.color == 'white':
                    if self.first_move and board.pieces[0][7] != None and board.pieces[0][7].first_move and board.pieces[0][7].piece_type == 'rook' and board.pieces[0][7].color == 'white' and board.pieces[0][6] == None and board.pieces[0][5] == None  and board.pieces[0][4] == None and is_attacked(board, (self.y, self.x) ,'white') == False:
                        moves.append((0, 5))
                    if self.first_move and board.pieces[0][0] != None and board.pieces[0][0].first_move and board.pieces[0][0].piece_type == 'rook' and board.pieces[0][0].color == 'white' and board.pieces[0][1] == None and board.pieces[0][2] == None and is_attacked(board, (self.y, self.x) ,'white') == False:
                        moves.append((0, 1))
                else:
                    if self.first_move and board.pieces[7][7] != None and board.pieces[7][7].first_move and board.pieces[7][7].piece_type == 'rook' and board.pieces[7][7].color == 'black' and board.pieces[7][6] == None and board.pieces[7][5] == None and board.pieces[7][4] == None and is_attacked(board, (self.y, self.x) ,'black') == False:
                        moves.append((7, 5))
                    if self.first_move and board.pieces[7][0] != None and board.pieces[7][0].first_move and board.pieces[7][0].piece_type == 'rook' and board.pieces[7][0].color == 'black' and board.pieces[7][1] == None and board.pieces[7][2] == None and is_attacked(board, (self.y, self.x) ,'black') == False:
                        moves.append((7, 1))
            
            if is_attacked(board, (self.y , self.x + 1), self.color) and (self.y, self.x + 2) in moves:
                moves.remove((self.y, self.x + 2))
            if is_attacked(board, (self.y , self.x - 1), self.color) and (self.y, self.x - 2) in moves:
                moves.remove((self.y, self.x - 2))

            return moves
        
        
        def incheck_valid_moves(self, board):
            moves = self.valid_moves(board)
            valid = []
                    
            for move in moves:
                board_test = copy.deepcopy(board)
                board_test.pieces[self.y][self.x].move(move[0], move[1], board_test)
                if not is_in_check(board_test, self.color):
                    valid.append(move)
            return valid
    

    