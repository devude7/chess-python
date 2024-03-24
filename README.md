# Chess in python
A small chess project implemented in python!
I believe that I've implemented all the special rules of chess like en-passant, castling or draw by repetition, so the game is complete in that regard. It is definitely not the most efficient and optimized chess implementation, so the game might lag at times. 

![chess](https://github.com/devude7/chess-python/assets/112627008/b898f641-329f-4909-ac12-1ff55da564d7)

# Structure

All aspects related to running and visualizing the game are contained within the `chess.py` file, implemented using the **pygame** library. Meanwhile, the underlying game mechanics are handled in the `logic.py` file

In `chess.py`, we find the main loop responsible for running the game, along with variables for handling game logic and visualizing the game state. Several functions facilitate these processes, including `draw_board`, `draw_pieces`, and `draw_valid_moves`. Additionally, there are lines of code for displaying appropriate messages to the user and handling events.

Much more operations take place in `logic.py` where all the classes are defined, including: `Board`, `Piece`, `Pawn`, `Bishop`, `Knight`, `Rook`, `Queen` and `King`. All the pieces inherit from `Piece` class. Now we'll have a look on what is inside them:

`Board` class has three attributes: **board_bottom**, **pieces** and **history**. `board_bottom` helps figure out which pieces are on which side so pawns can move correctly. `pieces` keeps track of where everything is on the board. And `history` lets you have draws by repeating moves.

`Piece` contain crutial attributes to all types of pieces: **coordiates**, **color**, **first_move** (essential for certain pieces) and **image** used for graphical representation. There are also functions for moving pieces on the board - `move` that is the general function for moving, but it also accounts for some special moves e.g castling. Furthermore, the `move` function prevents any moves that would result in a check. Second is `incheck_move` that handles moves while being in check.

Each piece class features its own unique function for returning valid moves(`valid_moves`) and valid moves while being in check(`incheck_valid_moves`) that simulates all potential moves to return correct moves. Additionally, the class sets the appropriate image for visualization, and some pieces, such as pawns, have extra attributes like en_passant.

In `logic.py`, there are essential functions apart from class implementations. Firstly, `terminate` determines if there's a winner (returning -100 for black, 100 for white) or if the game ends in a draw. It assesses various draw scenarios in chess, including dead position, repetition, or stalemate, and provides the appropriate message or value.

There are also functions such as `is_in_check`, `is_attacked`, `promotion`, `starting_board`, and `reset_en_passant`. Their are quite self-explanatory, so I won't provide additional details here.

# Future 
Initially, I had planned to implement an AI using the minimax algorithm to play against, but after some attempts, I've decided to postpone it for now. Perhaps I'll work on it later on.

Additionally, as I mentioned at the beginning, there is room for optimization. Certain elements could be restructured or relocated within the code for better efficiency, making the game run more smoothly.

chess pieces images: https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent
