

ALIVE_CHAR = 'X'
DEAD_CHAR = '.'


def print_grid(grid):
    for row in grid:
        for cell_value in row:
            if cell_value:
                print(f' {ALIVE_CHAR} ', end='')
            else:
                print(f' {DEAD_CHAR} ', end='')
        print()
