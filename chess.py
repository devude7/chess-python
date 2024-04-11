import pygame
import copy
from logic import *
from ai import minimax

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1200, 1000))
pygame.display.set_caption("Chess")
font = pygame.font.Font("freesansbold.ttf", 20)
big_font = pygame.font.Font("freesansbold.ttf", 40)
timer = pygame.time.Clock()
fps = 60
black = (0, 0, 0)
white = (255, 255, 255)
turn = 'white'
winner = '-'
restart = False
ai = None

# initialize the board
side = None
selected = 99


# draw the board in pygame
def draw_board():
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, white, (90 * (i + 1.5), 90 * (j + 1), 90, 90))
            else:
                pygame.draw.rect(screen, 'grey', (90 * (i + 1.5), 90 * (j + 1), 90, 90))
    for i in range(9):
        pygame.draw.line(screen, 'dark grey', (90 * (i + 1.5), 90), (90 * (i + 1.5), 810), 5)
        pygame.draw.line(screen, 'dark grey', (135, 90 * (i + 1)), (855, 90 * (i + 1)), 5)

    pygame.draw.rect(screen, 'yellow', (90 * 10.5, 90 * 6, 180, 90), 4)
    screen.blit(big_font.render("Forfeit", True, black), (90 * 10 + 70, 90 * 6 + 25))

    pygame.draw.rect(screen, 'yellow', (90 * 10.5, 90 * 4, 180, 90), 4)
    screen.blit(big_font.render("Restart", True, black), (90 * 10 + 65, 90 * 4 + 25))


# draw the pieces in pygame
def draw_pieces():
    for line in board.pieces:
        for piece in line:
            if piece != None:
                image = pygame.image.load(f'pieces/{piece.image}.png')
                if piece.piece_type == 'pawn':
                    image = pygame.transform.scale(image, (75, 75))
                else:
                    image = pygame.transform.scale(image, (80, 80))
                screen.blit(image, (90 * (piece.x + 1.55), 90 * (piece.y + 1.05)))
            if turn == 'white':
                if selected == piece:
                    pygame.draw.rect(screen, 'red', (90 * (piece.x + 1.5), 90 * (piece.y + 1), 90, 90), 2)
            else:
                if selected == piece:
                    pygame.draw.rect(screen, 'red', (90 * (piece.x + 1.5), 90 * (piece.y + 1), 90, 90), 2)


# draw the valid moves in pygame
def draw_valid_moves(valid_moves):
    if side == 'white':
        for move in valid_moves:
            pygame.draw.circle(screen, 'red', (move[1] * 90 + 180, move[0] * 90 + 135), 8)
    else:
        for move in valid_moves:
            pygame.draw.circle(screen, 'red', (move[1] * 90 + 180, move[0] * 90 + 135), 8)
       
run = True
# main loop
while run:
    timer.tick(fps)
    screen.fill("gray")

    if side == None:
        pygame.draw.rect(screen, 'yellow', (90 * 2.5, 90 * 1, 720, 720), 4)
        screen.blit(big_font.render("Choose a side", True, black), (90 * 5, 90 * 2))
        pygame.draw.rect(screen, 'yellow', (90 * 3.5, 90 * 4.5, 180, 90), 4)
        screen.blit(big_font.render("White", True, black), (90 * 3.5 + 35, 90 * 4.5 + 25))
        pygame.draw.rect(screen, 'yellow', (90 * 7.5, 90 * 4.5, 180, 90), 4)
        screen.blit(big_font.render("Black", True, black), (90 * 7.5 + 35, 90 * 4.5 + 25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]            
                if (x >= 319 and x <= 492) and (y >= 408 and y <= 491):
                    side = 'white'
                    board = Board(side)
                elif (x >= 677 and x <= 852) and (y >= 407 and y <= 492):
                    side = 'black'
                    board = Board(side)
    elif ai == None:
        pygame.draw.rect(screen, 'yellow', (90 * 2.5, 90 * 1, 720, 720), 4)
        screen.blit(big_font.render("Play", True, black), (110 * 5, 90 * 2))
        pygame.draw.rect(screen, 'yellow', (90 * 3.5, 90 * 4.5, 180, 90), 4)
        screen.blit(big_font.render("vs. AI", True, black), (90 * 3.5 + 35, 90 * 4.5 + 25))
        pygame.draw.rect(screen, 'yellow', (90 * 7.5, 90 * 4.5, 180, 90), 4)
        screen.blit(big_font.render("Alone", True, black), (90 * 7.5 + 35, 90 * 4.5 + 25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]            
                if (x >= 319 and x <= 492) and (y >= 408 and y <= 491):
                    ai = True 
                elif (x >= 677 and x <= 852) and (y >= 407 and y <= 492):
                    ai = False
    else:
        draw_board()
        draw_pieces()
        promotion(board)
        term = terminate(board)
        rep = board.is_repetition() 
        if restart == True:
            board = Board(side)
            selected = 99
            turn = 'white'
            winner = '-'
            restart = False
        if winner != '-':
            text = big_font.render(f"{winner} wins", True, black)
            screen.blit(text, (400, 870))
        if turn == 'white' and winner == '-':
            text = big_font.render("White's turn", True, black)
            if rep == True:
                text = big_font.render("Draw by repetition", True, black)
            if term == 'stalemate':
                text = big_font.render("Stalemate", True, black)
            if term == 0:
                text = big_font.render("Draw", True, black)
            if is_in_check(board, turn):
                if term == -100:
                    text = big_font.render("Black wins", True, black)  
                else:
                    text = big_font.render("White is in check", True, black)
            screen.blit(text, (400, 870))
        elif turn == 'black' and winner == '-':
            text = big_font.render("Black's turn", True, black)
            if rep == True:
                text = big_font.render("Draw by repetition", True, black)
            if term == 'stalemate':
                text = big_font.render("Stalemate", True, black)
            if term == 0:
                text = big_font.render("Draw", True, black)
            if is_in_check(board, turn):
                if term == 100:
                    text = big_font.render("White wins", True, black)  
                else:
                    text = big_font.render("Black is in check", True, black)
            screen.blit(text, (400, 870))
        if turn == 'white':
            reset_en_passant(board, 'white')
        else:
            reset_en_passant(board, 'black')
        if selected != 99 and winner == '-': # if a piece is selected, draw the valid moves
            if is_in_check(board, turn):
                valid_moves = selected.incheck_valid_moves(board)
            else:
                valid_moves = []
                for move in selected.valid_moves(board):
                    board_test = copy.deepcopy(board)
                    selected_test = copy.deepcopy(selected)
                    selected_test.move_test(move[0], move[1], board_test)
                    if not is_in_check(board_test, selected_test.color):
                        valid_moves.append(move)
            draw_valid_moves(valid_moves)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                x = (pos[0] - 135) // 90
                y = (pos[1] - 90) // 90
                if (x, y) == (10, 3) or (x, y) == (9, 3):
                    restart = True
                if turn == 'white': # if it is white's turn, select a white piece and move it
                    if (x, y) == (9, 5) or (x, y) == (10, 5):
                        winner = 'Black'    
                    if x >= 0 and x <= 7 and y >= 0 and y <= 7 and rep == False and term != 0 and winner == '-':
                        if board.pieces[y][x] != None and board.pieces[y][x].color == 'white':
                            selected = board.pieces[y][x]
                        elif selected != 99:
                            if is_in_check(board, turn):
                                if selected.incheck_move(y, x, board):
                                    turn = 'black'
                                    selected = 99
                            else:
                                if selected.move(y, x, board):
                                    turn = 'black'
                                    selected = 99
                elif turn == 'black': # if it is black's turn, select a black piece and move it
                    if (x, y) == (9, 5) or (x, y) == (10, 5):
                        winner = 'White'
                    if x >= 0 and x <= 7 and y >= 0 and y <= 7 and rep == False and term != 0 and winner == '-':
                        if board.pieces[y][x] != None and board.pieces[y][x].color == 'black':
                            selected = board.pieces[y][x]
                        elif selected != 99:
                            if is_in_check(board, turn):
                                if selected.incheck_move(y, x, board):
                                    turn = 'white'
                                    selected = 99
                            else:
                                if selected.move(y, x, board):
                                    turn = 'white'
                                    selected = 99

        if ai == True and turn != board.board_bottom:
            draw_board()
            draw_pieces()
            promotion(board)
            pygame.draw.rect(screen, 'grey', (400, 870, text.get_width(), text.get_height()))
            text = big_font.render("AI makes move...", True, black)
            screen.blit(text, (400, 870))  
            pygame.display.flip()  
            best_move = minimax(board, 2, turn)  
            board.pieces[best_move[0]][best_move[1]].move(best_move[2], best_move[3], board)  
            turn = board.board_bottom
            selected = 99

    pygame.display.flip()
pygame.quit()

