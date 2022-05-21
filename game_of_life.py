#!/usr/bin/env python3
"""
rules:
1. live cell with 2 or 3 live neighbours survives. All other live cells die.
2. dead cell with 3 live neighbours becomes alive. All other dead cells stay dead.
"""
from random import randint
import curses
from time import sleep


NUMBER_OF_ROWS = 20
NUMBER_OF_COLUMNS = 20
ALIVE_CHAR = '█'
DEAD_CHAR = '.'


class TickSpace:
    def __init__(self, grid):
        self.grid = grid
        self.sum_space = self._get_sum_space()
        self.next_grid = self.map_sum_space_to_next_grid()

    def _get_sum_space(self):
        ss = list()
        for i in range(NUMBER_OF_ROWS):
            ts_row = list()
            for j in range(NUMBER_OF_COLUMNS):
                ts_row.append(self.__aggregate_alive_neighbours(i, j))
            ss.append(ts_row)
        return ss

    def __aggregate_alive_neighbours(self, row, col):
        neighbour_sum = 0
        if 0 == row:  # top row
            if col == 0:  # top left corner
                neighbour_sum += self.grid[row][col + 1]
                neighbour_sum += self.grid[row + 1][col]
                neighbour_sum += self.grid[row + 1][col + 1]
            elif col == NUMBER_OF_COLUMNS - 1:  # top right corner
                neighbour_sum += self.grid[row][col - 1]
                neighbour_sum += self.grid[row + 1][col - 1]
                neighbour_sum += self.grid[row + 1][col]
            else:
                neighbour_sum += self.grid[row][col - 1]
                neighbour_sum += self.grid[row][col + 1]
                neighbour_sum += self.grid[row + 1][col - 1]
                neighbour_sum += self.grid[row + 1][col]
                neighbour_sum += self.grid[row + 1][col + 1]
        elif row == NUMBER_OF_ROWS - 1:
            if col == 0:  # bottom left corner
                neighbour_sum += self.grid[row - 1][col]
                neighbour_sum += self.grid[row - 1][col + 1]
                neighbour_sum += self.grid[row][col + 1]
            elif col == NUMBER_OF_COLUMNS - 1:  # bottom right corner
                neighbour_sum += self.grid[row - 1][col - 1]
                neighbour_sum += self.grid[row - 1][col]
                neighbour_sum += self.grid[row][col - 1]
            else:
                neighbour_sum += self.grid[row - 1][col - 1]
                neighbour_sum += self.grid[row - 1][col]
                neighbour_sum += self.grid[row - 1][col + 1]
                neighbour_sum += self.grid[row][col - 1]
                neighbour_sum += self.grid[row][col + 1]
        else:
            if col == 0:  # left edge
                neighbour_sum += self.grid[row - 1][col]
                neighbour_sum += self.grid[row - 1][col + 1]
                neighbour_sum += self.grid[row][col + 1]
                neighbour_sum += self.grid[row + 1][col]
                neighbour_sum += self.grid[row + 1][col + 1]
            elif col == NUMBER_OF_COLUMNS - 1:  # right edge
                neighbour_sum += self.grid[row - 1][col - 1]
                neighbour_sum += self.grid[row - 1][col]
                neighbour_sum += self.grid[row][col - 1]
                neighbour_sum += self.grid[row + 1][col - 1]
                neighbour_sum += self.grid[row + 1][col]
            else:
                for i in range(-1, 2):
                    neighbour_sum += self.grid[row - 1][col + i]
                    neighbour_sum += self.grid[row + 1][col + i]
                neighbour_sum += self.grid[row][col - 1]
                neighbour_sum += self.grid[row][col + 1]

        return neighbour_sum

    def map_sum_space_to_next_grid(self):
        alive = {
            0: 0,
            1: 0,
            2: 1,
            3: 1,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0
        }
        dead = {
            0: 0,
            1: 0,
            2: 0,
            3: 1,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0
        }

        ts = list()
        for i in range(NUMBER_OF_ROWS):
            ts_row = list()
            for j in range(NUMBER_OF_COLUMNS):
                if self.grid[i][j]:  # alive
                    ts_row.append(alive[self.sum_space[i][j]])
                else:  # dead
                    ts_row.append(dead[self.sum_space[i][j]])
            ts.append(ts_row)
        return ts

    def print_sum_space(self):
        for row in self.sum_space:
            for cell_value in row:
                print(f' {cell_value} ', end='')
            print()


def print_grid(screen, grid, x_offset=1, y_offset=1):
    i = 0
    for row in grid:
        j = 0
        for cell in row:
            if cell:  # alive
                screen.addstr(i + y_offset, j + x_offset, ALIVE_CHAR)
            else:
                screen.addstr(i + y_offset, j + x_offset, DEAD_CHAR)
            j += 1
        i += 1
    screen.refresh()


def ticks(screen, grid, previous_grid, iteration):
    if grid == previous_grid:
        return True

    print_grid(screen, grid)
    screen.addstr(0, 0, f'ticks: {iteration:8}')
    tick_space = TickSpace(grid)
    sleep(0.02)
    return ticks(screen, tick_space.next_grid, grid, iteration + 1)


def create_seed(pre_set=None):
    seed = list()

    if 1 == pre_set:  # ever living when 15 rows and 25 columns
        for i in range(NUMBER_OF_ROWS):
            seed.append([0] * NUMBER_OF_COLUMNS)
        seed[0][1] = 1
        seed[2][0] = 1
        seed[2][1] = 1
        seed[2][2] = 1
        seed[3] = [1] * NUMBER_OF_COLUMNS
        return seed

    if 2 == pre_set:  # dying set
        for i in range(NUMBER_OF_ROWS):
            seed.append([0]*NUMBER_OF_COLUMNS)
        seed[1][1] = 1
        seed[2][2] = 1
        seed[3][1] = 1
        return seed

    for i in range(NUMBER_OF_ROWS):
        current_row = []
        for j in range(NUMBER_OF_COLUMNS):
            current_row.append(randint(0, 1))
        seed.append(current_row)

    return seed


def main(stdscr):
    # assert that terminal window has sufficient lines and columns to draw the grid
    assert curses.LINES > NUMBER_OF_ROWS + 1, 'Too many game-of-life rows to show in terminal'
    assert curses.COLS > NUMBER_OF_COLUMNS + 1, 'Too many game-of-life columns to show in terminal'

    curses.curs_set(False)  # Do not blink the cursor
    input_key = 'y'
    while input_key == 'y':
        stdscr.clear()
        ticks(stdscr, grid, None, 0)
        stdscr.addstr(NUMBER_OF_ROWS + 1, 0, 'Press `y` to run again.')
        input_key = stdscr.getkey()
        if not input_key == 'y':
            break


if __name__ == '__main__':
    grid = create_seed()
    curses.wrapper(main)
