"""Console-based sudoku game."""
import pickle
import random
from typing import List, Optional


class SudokuField:
    """Sudoku game state."""

    cells: List[Optional[int]]
    row_width: int
    filled_count: int

    def __init__(self, cells: List[Optional[int]], row_width: int):
        """Initialize game state."""
        self.cells = cells
        self.row_width = row_width
        self.filled_count = len(list(filter(
            lambda x: x is not None, self.cells
        )))

    def get_row(self, row_id: int) -> List[Optional[int]]:
        """Get row cell list."""
        return self.cells[
            row_id * self.row_width:(row_id + 1) * self.row_width
        ]

    def get_column(self, column_id: int) -> List[Optional[int]]:
        """Get column cell list."""
        return self.cells[column_id::self.row_width]

    def get_cell(self, row_id: int, column_id: int) -> Optional[int]:
        """Get cell value."""
        return self.cells[row_id * self.row_width + column_id]

    def set_cell(self, row_id: int, column_id: int, value: int) -> None:
        """Set cell value."""
        if (value <= 0) or (value > 9):
            raise ValueError()
        if not self.can_set_cell(row_id, column_id, value):
            raise ValueError()
        if self.cells[row_id * self.row_width + column_id] is None:
            self.filled_count += 1
        self.cells[row_id * self.row_width + column_id] = value

    # TODO: sub-squares 3x3

    def get_cell_str(self, cell: Optional[int]) -> str:
        """Get string representation of cell."""
        if cell is None:
            return ' '
        return str(cell)

    def get_row_str(self, row_cells: List[Optional[int]]) -> str:
        """Get string representation of field row."""
        return '|'.join(list(map(
            lambda cell: self.get_cell_str(cell), row_cells
        )))

    def __str__(self) -> str:
        """Get string representation of game field."""
        separator_size = 2 * len(self.cells) // self.row_width - 1
        separator_line = (
            '\n' + '-' * separator_size + '\n'
        )
        return separator_line.join(list(
            map(
                lambda row_id: self.get_row_str(self.get_row(row_id)),
                range(len(self.cells) // self.row_width)
            )
        ))

    def can_set_cell(self, row_id: int, column_id: int, value: int) -> bool:
        """Return `True` if cell can be set to value."""
        if self.get_cell(row_id, column_id) == value:
            return True
        if value in self.get_row(row_id):
            return False
        if value in self.get_column(column_id):
            return False
        return True

    def is_filled(self) -> bool:
        """Return `True` if all cells are filled."""
        return self.filled_count == len(self.cells)


def generate_random_field(filled_count: int) -> SudokuField:
    """Generate random sudoku field with given filled cell count."""
    if filled_count >= 81:
        raise ValueError()  # TODO
    game = SudokuField([None] * 81, 9)

    current_filled_count = 0
    while current_filled_count < filled_count:
        while True:
            row_id = random.randint(0, 8)
            column_id = random.randint(0, 8)
            if game.get_cell(row_id, column_id) is not None:
                continue
            value = random.randint(1, 9)
            if game.can_set_cell(row_id, column_id, value):
                game.set_cell(row_id, column_id, value)
                break
        current_filled_count += 1

    return game


def play(game: SudokuField) -> bool:
    """Play game in console dialog mode, return `True` if player has won."""
    print(game)
    while not game.is_filled():
        print('>', end=' ')
        command_tokens = input().split()
        if len(command_tokens) == 0:
            continue
        if command_tokens[0] == 'SET':
            if len(command_tokens) < 3:
                print('Command SET requires 3 parameters')
                continue

            try:
                row_id = int(command_tokens[1])
                if (row_id < 0) or (row_id >= 9):
                    raise ValueError()
            except ValueError:
                print('Command SET requires parameter 1 to be int from 0 to 9')
                continue

            try:
                column_id = int(command_tokens[2])
                if (column_id < 0) or (column_id >= 9):
                    raise ValueError()
            except ValueError:
                print('Command SET requires parameter 2 to be int from 0 to 9')
                continue

            try:
                value = int(command_tokens[3])
                if (value <= 0) or (value > 9):
                    raise ValueError()
            except ValueError:
                print('Command SET requires parameter 3 to be int from 0 to 9')
                continue

            if not game.can_set_cell(row_id, column_id, value):
                print(
                    f'You can not set cell at {row_id}, {column_id} to {value}'
                )
                continue
            game.set_cell(row_id, column_id, value)
            print(game)
        elif command_tokens[0] == 'PRINT':
            print(game)
        elif command_tokens[0] == 'SAVE':
            if len(command_tokens) < 2:
                print('Command SAVE requires 1 parameter')
                continue
            try:
                with open(command_tokens[1], mode='wb') as output_file:
                    pickle.dump(game, output_file)
            except IOError as exc:
                print('Error:', str(exc))
        elif command_tokens[0] == 'EXIT':
            return False
        elif command_tokens[0] == 'HELP':
            print('Commands:')
            print('SET i j v -- set cell at i, j to value v and print game')
            print('        i -- row id,    in range from 0 to 9')
            print('        j -- column id, in range from 0 to 9')
            print('        v -- new value, in range from 0 to 9')
            print('SAVE f    -- save game state to pickle file')
            print('        f -- file path, .pkl extension is recommended')
            print('PRINT     -- print game')
            print('HELP      -- print this help text')
            print('EXIT      -- give up and exit')

    return True


def main() -> None:
    """Start and play sudoku game in console dialog mode."""
    game: SudokuField

    while True:
        print(
            'Type NEW to start new game or LOAD to load game from pickle file'
        )
        start_method = input()
        if start_method in ('NEW', 'LOAD'):
            break
        else:
            print('Invalid input')

    if start_method == 'NEW':
        while True:
            print('Type filled cell count or empty string to cancel:', end=' ')
            filled_count_str = input()
            if not filled_count_str:
                return
            try:
                filled_count = int(filled_count_str)
            except ValueError:
                print('Invalid data')
            else:
                break
        game = generate_random_field(filled_count)
    else:
        while True:
            print(
                'Type file name or to load game from or empty string to'
                ' cancel:',
                end=' '
            )
            file_name = input()
            if not file_name:
                return
            try:
                with open(file_name, mode='rb') as input_file:
                    game = pickle.load(input_file)
            except Exception as exc:
                print('Error:', str(exc))
                continue
            else:
                break

    win = play(game)
    if win:
        print('You win!')
    else:
        print('You lose!')


if __name__ == '__main__':
    main()
