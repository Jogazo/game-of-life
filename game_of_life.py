#!/usr/bin/env python3
"""
rules:
1. live cell with 2 or 3 live neighbours survives. All other live cells die.
2. dead cell with 3 live neighbours becomes alive. All other dead cells stay dead.
"""
from utils import print_grid


NUMBER_OF_ROWS = 15
NUMBER_OF_COLUMNS = 25


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
                    # print(self.grid[i][j], self.sum_space[i][j], alive[self.sum_space[i][j]])
                    ts_row.append(alive[self.sum_space[i][j]])
                else:  # dead
                    # print(self.grid[i][j], self.sum_space[i][j], dead[self.sum_space[i][j]])
                    ts_row.append(dead[self.sum_space[i][j]])
            ts.append(ts_row)
        return ts

    def print_sum_space(self):
        for row in self.sum_space:
            for cell_value in row:
                print(f' {cell_value} ', end='')
            print()


def ticks(grid, previous_grid, iteration):
    if grid == previous_grid:
        return True
    print('====', iteration, '====')
    print_grid(grid)
    tick_space = TickSpace(grid)
    # print('_'*3*NUMBER_OF_COLUMNS)
    # tick_space.print_sum_space()
    return ticks(tick_space.next_grid, grid, iteration + 1)


def create_seed():
    seed = list()
    for i in range(NUMBER_OF_ROWS):
        seed.append([0] * NUMBER_OF_COLUMNS)
    seed[0][1] = 1
    seed[2][0] = 1
    seed[2][1] = 1
    seed[2][2] = 1
    seed[3] = [1] * NUMBER_OF_COLUMNS
    return seed
    # dying_seed = list()
    # for i in range(NUMBER_OF_ROWS):
    #     dying_seed.append([0]*NUMBER_OF_COLUMNS)
    # dying_seed[1][1] = 1
    # dying_seed[2][2] = 1
    # dying_seed[3][1] = 1
    # return dying_seed


def main():
    seed = create_seed()
    ticks(seed, None, 0)


if __name__ == '__main__':
    main()
