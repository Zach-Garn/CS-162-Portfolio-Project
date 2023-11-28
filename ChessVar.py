# Author: Zachary Garner
# GitHub username: Zach-Garn
# Date: 08/14/2023
# Description: A variation of chess that uses only the king, rook, bishop and knight pieces with alternate starting
# positions. The object of the game is to have your king be the first to reach row 8. Capture and piece movements follow
# traditional chess rules. There are no moves allowed that would place either king into check. The chess board prints
# to the console and the game is played through commands in the console.

import copy


class IllegalMoveError(Exception):
    """Raises an error for when an illegal move in input."""
    pass


class ChessVar:
    """Class that represents the game’s functionality and controls the turns and movement of the pieces. It also checks
     for a King in check after and move and displays the board."""
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

        # white pieces starting position
        self.board[0][0] = King('white')
        self.board[1][0] = Rook('white')
        self.board[0][1] = Bishop('white')
        self.board[1][1] = Bishop('white')
        self.board[0][2] = Knight('white')
        self.board[1][2] = Knight('white')

        # black pieces starting position
        self.board[0][7] = King('black')
        self.board[1][7] = Rook('black')
        self.board[0][6] = Bishop('black')
        self.board[1][6] = Bishop('black')
        self.board[0][5] = Knight('black')
        self.board[1][5] = Knight('black')

        # white makes first move
        self.turn = 'white'

        # current state of the game
        self.state = 'UNFINISHED'

    def get_game_state(self):
        """Keeps track of the current state of the game.
            Returns ‘UNFINISHED’, ‘BLACK_WON’, ‘WHITE_WON’, or ‘TIE"""
        return self.state

    def make_move(self, from_loc, to_loc):
        """Takes two parameters:
        from_loc – square piece is moving from
        to_loc – square piece is moving to
        return True if the move was successful and False if unsuccessful."""
        from_row, from_col = int(from_loc[1]) - 1, ord(from_loc[0]) - ord('a')
        to_row, to_col = int(to_loc[1]) - 1, ord(to_loc[0]) - ord('a')

        if self.board[from_row][from_col] is None:
            return False

        piece = self.board[from_row][from_col]

        if piece.color != self.turn:
            return False

        if (to_row, to_col) not in piece.get_legal_moves((from_row, from_col), self.board):
            return False

        # Create a deepcopy of the board so that it can be determined if that move puts either king in check.
        test_board = copy.deepcopy(self.board)
        test_board[to_row][to_col] = piece
        test_board[from_row][from_col] = None

        if self.is_king_in_check(self.turn, test_board):
            return False

        opponent = 'white' if self.turn == 'black' else 'black'
        if self.is_king_in_check(opponent, test_board):
            return False

        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None

        self.turn = 'black' if self.turn == 'white' else 'white'

        if self.check_winner():
            self.state = self.turn.upper() + '_WON'

        return True

    def is_king_in_check(self, color, board):
        """Takes two parameters:
            color: checks the color of the king returns if the king is in check or not.
            board: to see the positions of the pieces on the board. """
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color != color:
                    if (self.find_king(color, board) in piece.get_legal_moves((row, col), board)):
                        return True
        return False

    def find_king(self, color, board):
        """"Takes two parameters:
        color: checks for the color of the king
        board: searches the board to find the position of king"""
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    return row, col
        raise Exception(f'King of color {color} not found on board!')

    def check_winner(self):
        """Checks to see if any of the color kings reached the 8th row and then returns which color won.
        if there was a tie, then it returns 'TIE'"""
        white_king_found = False
        black_king_found = False
        for col in range(8):
            king = self.board[7][col]
            if isinstance(king, King):
                if king.color == 'white':
                    white_king_found = True
                elif king.color == 'black':
                    black_king_found = True

        if white_king_found and black_king_found:
            self.state = 'TIE'
            return True
        elif white_king_found:
            self.state = 'WHITE_WON'
            return True
        elif black_king_found:
            self.state = 'BLACK_WON'
            return True
        return False

    def display_board(self):
        """Displays the board by creating columns a - h and rows 1-8. Initializes to the pieces starting positions."""
        print("  a b c d e f g h")
        for row in range(7, -1, -1):
            print(row + 1, end=' ')
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    print(piece.symbol(), end=' ')  # Call the symbol method
                else:
                    print('.', end=' ')
            print(row + 1)
        print("  a b c d e f g h")


class Piece:
    """Class that represents all the pieces of the game and their legal moves."""
    def __init__(self, color):
        self.color = color

    def get_legal_moves(self, position, board):
        """Raises the IllegalMoveError when an illegal move is made."""
        raise IllegalMoveError("Illegal move")


class King(Piece):
    """Class that represents the King piece and inherits from the Piece class"""
    # legal moves for King
    def get_legal_moves(self, position, board):
        """Function that determines the legal moves for the King piece by determining all directions the king can move
        and making sure that the move is legal. Also, if the move interferes with a friendly piece or captures."""
        legal_moves = []
        row, col = position
        # accounts for movement in all directions, including diagonal
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for row_change, column_change in directions:
            new_row, new_col = row + row_change, col + column_change
            if 0 <= new_row < 8 and 0 <= new_col < 8:  # check move remains on board
                if board[new_row][new_col] is None:  # make sure new position is empty
                    legal_moves.append((new_row, new_col))
                elif board[new_row][new_col].color != self.color:  # make sure same color isn't being captured
                    legal_moves.append((new_row, new_col))

        return legal_moves

    def symbol(self):
        """Creates the visual representation of both the white and black King pieces when the board is displayed"""
        return 'K' if self.color == 'white' else 'k'


class Rook(Piece):
    """Class that represents the Rook piece and inherits from the Piece class"""
    # legal moves for Rook
    def get_legal_moves(self, position, board):
        """Function that determines the legal moves for the Rook piece by determining all directions the rook can move
            and making sure that the move is legal. Also, if the move interferes with a friendly piece or captures."""
        legal_moves = []
        row, col = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # accounts for movement in all directions, excluding diagonal

        for row_change, column_change in directions:
            for distance in range(1, 8):
                new_row, new_col = row + row_change * distance, col + column_change * distance
                if 0 <= new_row < 8 and 0 <= new_col < 8:  # check move remains on board
                    if board[new_row][new_col] is None:  # make sure new position is empty
                        legal_moves.append((new_row, new_col))
                    elif board[new_row][new_col].color != self.color:  # make sure same color isn't being captured
                        legal_moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return legal_moves

    def symbol(self):
        """Creates the visual representation of both the white and black Rook pieces when the board is displayed"""
        return 'R' if self.color == 'white' else 'r'


class Bishop(Piece):
    """Class that represents the Bishop piece and inherits from the Piece class"""
    # legal moves for Bishop
    def get_legal_moves(self, position, board):
        """Function that determines the legal moves for the Bishop piece by determining all directions the bishop can
        move and making sure that the move is legal. Also, if the move interferes with a friendly piece or captures."""
        legal_moves = []
        row, col = position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # accounts for movement in all diagonal directions

        for row_change, column_change in directions:
            for distance in range(1, 8):
                new_row, new_col = row + row_change * distance, col + column_change * distance
                if 0 <= new_row < 8 and 0 <= new_col < 8:  # check move remains on board
                    if board[new_row][new_col] is None:  # make sure new position is empty
                        legal_moves.append((new_row, new_col))
                    elif board[new_row][new_col].color != self.color:  # make sure same color isn't being captured
                        legal_moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return legal_moves

    def symbol(self):
        """Creates the visual representation of both the white and black Bishop pieces when the board is displayed"""
        return 'B' if self.color == 'white' else 'b'


class Knight(Piece):
    """Class that represents the Knight piece and inherits from the Piece class"""
    # legal moves for Knight
    def get_legal_moves(self, position, board):
        """Function that determines the legal moves for the Knight piece by determining all directions the knight can
        move and making sure that the move is legal. Also, if the move interferes with a friendly piece or captures."""
        legal_moves = []
        row, col = position
        # accounts for 8 distinct L shaped movements
        directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

        for row_change, column_change in directions:
            new_row, new_col = row + row_change, col + column_change
            if 0 <= new_row < 8 and 0 <= new_col < 8:  # check move remains on board
                # make sure new position is empty or contains an opponents piece
                if board[new_row][new_col] is None or board[new_row][new_col].color != self.color:
                    legal_moves.append((new_row, new_col))

        return legal_moves

    def symbol(self):
        """Creates the visual representation of both the white and black Knight pieces when the board is displayed"""
        return 'N' if self.color == 'white' else 'n'


# def main():
#     game = ChessVar()
#     game.display_board()
#     while game.get_game_state() == 'UNFINISHED':
#         try:
#             from_loc = input(f"{game.turn.capitalize()}'s turn. Enter the location of the piece you want to move (e.g., 'a1'): ")
#             to_loc = input(f"Enter the location you want to move to (e.g., 'a2'): ")
#             if game.make_move(from_loc, to_loc):
#                 game.display_board()
#             else:
#                 print("Invalid move. Try again.")
#         except Exception as e:
#             print("An error occurred:", e)
#
#     print("Game over. Result:", game.get_game_state())
#
# if __name__ == "__main__":
#     main()
