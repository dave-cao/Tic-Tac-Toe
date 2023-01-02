# TIC TAC TOE GAME
"""
A simple text-based Tic Tac Toe game.

Learning points:
- Using classes and object oriented programming
- Nested lists/arrays
"""
from dcpy import clear

board = """
 A3  | B3  | C3
-----------------
 A2  | B2  | C2
-----------------
 A1  | B1  | C1

"""

# similar to chess, we have to map each position with a number / letter


def main():

    print_intro()
    game = Game()
    game.play()


class Game:
    def __init__(self):
        self.board_size = 3
        self.board = []
        self.column_letter = ("A", "B", "C")
        self.continue_game = True
        self.player_1 = " X "
        self.player_2 = " O "
        self.current_player = self.player_1

        self.create_board()

    def create_board(self):
        """Creates the tic tac toe board (list of lists) with a size of the specified
        board size."""
        for row_number in range(self.board_size, 0, -1):
            row = []
            for letter in self.column_letter:
                row.append(Tile(letter, row_number))
            self.board.append(row)

    def show_board(self):
        """Clears the screen and shows the new board"""
        clear()
        for i, row in enumerate(self.board):
            for q, tile in enumerate(row):
                print(tile.show_content(), end="")

                # gets rid of extra column "|"
                if q < len(row) - 1:
                    print("|", end="")
            print()

            # gets rid of extra row
            if i < len(self.board) - 1:
                print("===========")

    def update_placement(self, user_option):
        """Based on the current player and what they've chosen, update the content
        of the board, and switch the player.

        Args:
            user_option(str): the position that the user wants to update
        """
        for row in self.board:
            for tile in row:
                pos = tile.get_position()
                if "".join(pos) == user_option:
                    # only update content if the content has not been updated yet
                    if tile.content == "   ":
                        tile.flip(self.current_player)
                        self.switch_player()

    def switch_player(self):
        """Switch the player turns"""
        if self.current_player == self.player_1:
            self.current_player = self.player_2
        else:
            self.current_player = self.player_1

    def play(self):
        """Starts the game. Shows, updates, and checks the game board after every turn"""
        while self.continue_game:
            self.show_board()
            user_option = input("\nWhere do you want to play the tic tac: ").upper()
            self.update_placement(user_option)
            self.check_end_condition()

    def check_end_condition(self):
        """Checks to see if the game has ended. If so, end the game."""
        if self.is_win():
            self.show_board()
            self.switch_player()
            print(f"\nPlayer {self.current_player} wins!")
            self.continue_game = False
        elif self.is_tie():
            self.show_board()
            print("TIED")
            self.continue_game = False

    def is_list_win(self, row):
        """Checks if the list given has all the same elemnts. Returns true if so.

        Args:
            row(list): a list containing elements
        Returns:
            Bool: True if all elements are the same, False otherwise.
        """
        first = row[0].content
        for i in range(1, len(row)):
            if row[i].content == "   " or first != row[i].content:
                return False

        return True

    def contains_list_win(self, list_of_tiles):
        """
        Checks if a nested list contains a row that has all the same elements.

        Args:
            list_of_tiles(list[list]): a list of lists to check

        Returns:
            bool: True if a nested list contains all the same elements, False otherwise.
        """
        list_win = False
        for row in list_of_tiles:
            if self.is_list_win(row):
                list_win = True

        return list_win

    def is_row_win(self):
        """
        Checks if the board has a row win

        Returns:
            bool: True if the board has a row win, False otherwise.
        """
        return self.contains_list_win(self.board)

    def is_col_win(self):
        """
        Checks if the board has a column win.

        Returns:
            bool: True if the board has a column win, False otherwise
        """
        list_of_tiles = []
        for col_index in range(len(self.board[0])):
            tiles = []
            for row_index in range(len(self.board)):
                tiles.append(self.board[row_index][col_index])

            list_of_tiles.append(tiles)

        return self.contains_list_win(list_of_tiles)

    def is_diagonal_win(self):
        """
        Checks to see if the board has a diagonal win.

        Returns:
            bool: True if the board has a diagonal win, False otherwise.
        """

        # There is only two possible diagonal wins
        list_of_tiles = [[], []]
        for i in range(len(self.board)):
            # forward diagonal
            list_of_tiles[0].append(self.board[i][i])

            # backwards diagonal
            list_of_tiles[1].append(self.board[i][len(self.board[0]) - 1 - i])
        return self.contains_list_win(list_of_tiles)

    def is_win(self):
        """Checks if someone has won on the board

        Returns:
            bool: True if someone has won, False otherwise.
        """
        return self.is_row_win() or self.is_col_win() or self.is_diagonal_win()

    def is_tie(self):
        """
        Checks if someone has tied on the board.

        Returns:
            bool: True if the game has tied, False otherwise.
        """
        tie = True
        for row in self.board:
            for tile in row:
                if tile.content == "   ":
                    tie = False

        return tie


class Tile:
    def __init__(self, column_letter, row_number):
        """
        The Tile class is the individual elements within the board that consist
        of either an X, O, or " ".

        Args:
            column_letter(str): the column letter position this tile is on the board
            row_number(int): the row position this tile is on the board
        """
        self.row_number = row_number
        self.column_letter = column_letter
        self.content = "   "

    def get_position(self):
        """Get's the current position of the tile on the board.

        Returns:
            tuple: a tuple of the column letter with it's row number of the tile
        """
        return (self.column_letter, str(self.row_number))

    def show_content(self):
        """Returns the content str within this tile. Default is a blank space."""
        return self.content

    def flip(self, current_player):
        """
        Makes the content of the tile into the current player (either X or O)

        Args:
            current_player(str): either the player X or O.
        """
        self.content = current_player


def print_intro():
    """Prints the the game to the screen"""

    print("Welcome to...")
    print(
        """
        88
  ,d    ""              ,d                            ,d
  88                    88                            88
MM88MMM 88  ,adPPYba, MM88MMM ,adPPYYba,  ,adPPYba, MM88MMM ,adPPYba,
  88    88 a8"     ""   88    ""     `Y8 a8"     ""   88   a8"     "8a
  88    88 8b           88    ,adPPPPP88 8b           88   8b       d8
  88,   88 "8a,   ,aa   88,   88,    ,88 "8a,   ,aa   88,  "8a,   ,a8"
  "Y888 88  `"Ybbd8"'   "Y888 `"8bbdP"Y8  `"Ybbd8"'   "Y888 `"YbbdP"'
          """
    )
    print("=================================")
    print("This is the board and positions:")
    print(board)
    input("Press enter to play\n")


main()
