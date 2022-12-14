from typing import Tuple, List
from re import findall
from colorama import Fore

Point = Tuple[int, int]

grid: List[List[bool | None]] = []
grid_dimensions: List[int] = []
start: Point = (0, 0)


def draw_between(a: Point, b: Point) -> None:
    global grid
    dx = b[0] - a[0]
    dy = b[1] - a[1]

    if dx == 0:
        for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
            grid[y][a[0]] = False
    elif dy == 0:
        for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
            grid[a[1]][x] = False
    else:
        print('Error: diagonal line')


def draw_border(points: List[Point]) -> None:
    for i in range(len(points) - 1):
        draw_between(points[i], points[i + 1])


def print_grid() -> None:
    print('\nGrid:')
    for i, g in enumerate(grid):
        print(Fore.WHITE + f'{i:03d} ', end='')
        for j, c in enumerate(g):
            if (j, i) == start:
                print(Fore.WHITE + '+', end='')
            elif c is None:
                print(Fore.LIGHTYELLOW_EX + 'o', end='')
            elif c == True:
                print(Fore.WHITE + '.', end='')
            else:
                print(Fore.BLUE + '#', end='')
        print()
    print()


def drop(a: Point, part_2: bool) -> int:
    (x, y) = a
    to_abyss: bool = False

    if grid[start[1]][start[0]] is None:
        return 0

    if y + 1 < grid_dimensions[0]:
        if grid[y + 1][x]:
            return drop((x, y + 1), part_2)
    else:
        to_abyss = True

    if y + 1 < grid_dimensions[0] and x - 1 >= 0:
        if grid[y + 1][x - 1]:
            return drop((x - 1, y + 1), part_2)
    else:
        to_abyss = True

    if y + 1 < grid_dimensions[0] and x + 1 < grid_dimensions[1]:
        if grid[y + 1][x + 1]:
            return drop((x + 1, y + 1), part_2)
    else:
        to_abyss = True

    if not to_abyss:
        grid[y][x] = None
        return 1

    if not part_2:
        return -1

    if to_abyss:
        if x - 1 < 0:
            extend_left()
            return drop((x + 1, y), True)

        if x + 1 >= grid_dimensions[1]:
            extend_right()
            return drop((x, y), True)

    return -1


def extend_right() -> None:
    global grid
    global start

    for i, row in enumerate(grid):
        if i == grid_dimensions[0] - 1:
            row.append(False)
        else:
            row.append(True)
    grid_dimensions[1] += 1


def extend_left() -> None:
    global grid
    global start

    for i, row in enumerate(grid):
        if i == grid_dimensions[0] - 1:
            row.insert(0, False)
        else:
            row.insert(0, True)
    start = (start[0] + 1, start[1])
    grid_dimensions[1] += 1


def solve(file_text: str) -> Tuple[int, int]:
    global grid
    units_of_sand_1: int = 0
    units_of_sand_2: int = 0

    init_grid(file_text)

    while (x := drop(start, False)) == 1:
        units_of_sand_1 += 1

    init_grid(file_text)

    grid.append([True] * grid_dimensions[1])
    grid.append([False] * grid_dimensions[1])
    grid_dimensions[0] += 2

    while (x := drop(start, True)) != 0:
        units_of_sand_2 += 1
    return (units_of_sand_1, units_of_sand_2)


def init_grid(file_text: str) -> None:
    global grid
    global start
    global grid_dimensions
    lines = list(map((lambda xs: xs.split('->')), file_text.splitlines()))

    # Finding width of the grid
    x_values: List[int] = list(map(int, findall('(\d+),', file_text)))
    max_x: int = max(x_values)
    min_x: int = min(x_values)

    # Finding height of the grid
    y_values = list(map((lambda x: int(x[0])), findall('(\d+)(( ->)|(\n))', file_text)))
    max_y: int = max(y_values)

    start = (500 - min_x, 0)

    # Initialising the grid
    grid = [[True] * (max_x - min_x + 1) for _ in range(max_y + 1)]
    grid_dimensions = [len(grid), len(grid[0])]

    # Finding the rock borders
    rock_borders: List[List[Point]] = []
    for i, line in enumerate(lines):
        rock_borders.append(
            list(map((lambda xs: tuple(map(int, findall('(\d+)', xs)))), line)))

    # Drawing the rocks
    for border in rock_borders:
        # Making the list of points relative to the grid
        x = list(map((lambda xs: (xs[0] - min_x, xs[1])), border))
        draw_border(x)


def main():
    with open('input.txt', 'r') as file:
        file_text: str = file.read()

        units_of_sand_1, units_of_sand_2 = solve(file_text)

        print(f'Part 1: {units_of_sand_1}')
        print(f'Part 2: {units_of_sand_2}')
        # print_grid()


if __name__ == "__main__":
    main()
