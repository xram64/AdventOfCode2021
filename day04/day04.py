## Advent of Code 2021: Day 4
## https://adventofcode.com/2021/day/4
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 58838, [Part 2]: 6256

from math import floor

class Board():
    def __init__(self, raw_board, id):
        self.id = id    # original position of board in list of boards
        self.score = 0  # final score of a winning board

        # The grid will be a 2D list indexed by board.grid[row][col]
        self.grid = []
        for line in raw_board:
            self.grid.append( line.split() )

        # The marked_grid will be a 5x5 Boolean 2D list to keep track of the marked positions on the board
        self.marked_grid = [ [False]*5, [False]*5, [False]*5, [False]*5, [False]*5 ]

        # 'win' will be False unless the board wins, which will set it to a tuple indicating
        #   whether the win was in a row or column, the row/col index, and the row/col list itself
        #   win = ('row', 0, ['1', ..., '5']), or win = ('col', 0, ['1', ..., '5'])
        self.win = False

        # Keep track of the last checked number, freezing if the board wins (for score calculation)
        self.last_checked_number = 0


    def check_number(self, num):
        # Checks if the given bingo number appears on this board and marks it if so
        # Returns True if the number was found and False if it wasn't
        self.last_checked_number = num

        for row_n, row in enumerate(self.grid):
            try:  # number found in this row
                col_n = row.index(num)
                self.marked_grid[row_n][col_n] = True
                return True

            except ValueError:  # number not found in this row (thrown if index() fails)
                continue

        else:
            return False

    def check_for_win(self):
        # Checks if this board is a winning board (all numbers marked in a row or col)

        # Check for winning rows
        for row_n, row in enumerate(self.marked_grid):
            if not (False in row):
                # If all elements in a row are True, we have a win on this row
                self.win = ('row', row_n, self.grid[row_n])
                return self.win

        # Check for winning columns
        for col_n in range(5):
            for row_n in range(5):
                # If any element in this column is False, skip to the next column
                if self.marked_grid[row_n][col_n] == False:
                    break
            else:
                # If no False's are found, we have a winning column
                self.win = ('col', col_n, [r[col_n] for r in self.grid])
                return self.win

        return False

    def calculate_score(self):
        sum = 0

        for row_n, row in enumerate(self.marked_grid):
            for col_n, mark in enumerate(row):
                if mark == False:
                    # Only add the unmarked numbers
                    sum += int(self.grid[row_n][col_n])

        self.score = sum * int(self.last_checked_number)
        return self.score


if __name__ == '__main__':
    with open('day04_input.txt', 'r') as f:

        # First line of input is list of numbers in drawing order
        numbers = f.readline()

        # Remaining lines in groups of 6 hold 1 new line followed by the 5 bingo board lines
        board_data = f.readlines()

    numbers = numbers.split(',')

    raw_boards = []
    number_of_boards = floor(len(board_data) / 6)
    for i in range(number_of_boards):
        raw_boards.append( [c.strip() for c in board_data[(6*i + 1):(6*i + 6)]] )

    boards = []
    for id, raw_board in enumerate(raw_boards):
        boards.append( Board(raw_board, id) )

    # Check all numbers and keep track of winning boards in order of win, along with their board number
    winning_boards = []
    for number in numbers:
        for board in boards:
            # Skip checking boards that won to make sure we don't keep changing their 'last_checked_number'
            if (board not in winning_boards) and (board.check_number(number)):
                # If we got True, the number is on the board, so now we check if the board won
                if board.check_for_win():
                    # If we don't get False, this board won
                    winning_boards.append(board)

    ## Part 1
    first_winning_board = winning_boards[0]
    print(f"[Part 1] Board #{first_winning_board.id + 1} wins first with a score of {str(first_winning_board.calculate_score())}.")
    print(f"  Board #{first_winning_board.id + 1} wins in {first_winning_board.win[0]} {first_winning_board.win[1]+1}: ")
    for row in first_winning_board.grid:
        print("  " + "\t".join(row))
    print()

    ## Part 2
    last_winning_board = winning_boards[-1]
    print(f"[Part 2] Board #{last_winning_board.id + 1} wins last with a score of {str(last_winning_board.calculate_score())}.")
    print(f"  Board #{last_winning_board.id + 1} wins in {last_winning_board.win[0]} {last_winning_board.win[1]+1}: ")
    for row in last_winning_board.grid:
        print("  " + "\t".join(row))
    print()
