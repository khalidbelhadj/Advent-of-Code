import heapq as hq
from typing import List, Tuple, Set, Any
from dataclasses import dataclass


@dataclass
class Node:
    position: Tuple[int, int]
    height: int
    g: float
    h: float
    parent: Any

    def f(self):
        return self.g + self.h
    def __lt__(self, other):
        return self.f() < other.f()
    def __le__(self, other):
        return self.f() <= other.f()
    def __eq__(self, other):
        return self.position == other.position
    def __ne__(self, other):
        return self.position != other.position
    def __gt__(self, other):
        return self.f() > other.f()
    def __ge__(self, other):
        return self.f() >= other.f()


Grid = List[List[Node]]
Point = Tuple[int, int]


def get_node(point: Point, grid: Grid):
    '''Get the node at a given point from a grid'''
    return grid[point[0]][point[1]]


def distance(a: Point, b: Point) -> int:
    '''Manhattan distance between two points a and b'''

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbours(position: Point) -> List[Point]:
    '''Get the neighbours of a position'''

    return [(position[0] + 1, position[1]),
            (position[0] - 1, position[1]),
            (position[0], position[1] + 1),
            (position[0], position[1] - 1)]


def traversable(start: Point, neighbour: Point, grid: Grid) -> bool:
    '''Check if a path is traversable'''

    if not (0 <= neighbour[0] < len(grid) and 0 <= neighbour[1] < len(grid[0])):
        return False

    start_height = get_node(start, grid).height
    neighbour_height = get_node(neighbour, grid).height

    if neighbour_height - start_height > 1:
        return False
    return True


def a_star(grid: Grid, start: Node, end: Node) -> int:
    '''A* algorithm, returns the length of the shortest path'''

    visited: Set[Point] = set()
    to_visit: List[Node] = [start]
    while (current := hq.heappop(to_visit)) != end:

        if len(to_visit) == 0:
            print('No path found')
            return 10**10
        
        visited.add(current.position)

        if current == end:
            break

        neighbours = get_neighbours(current.position)

        for neighbour_point in neighbours:

            if ((not traversable(current.position, neighbour_point, grid))
                    or (neighbour_point in visited)):
                continue

            neighbour_node = get_node(neighbour_point, grid)

            if current.g < neighbour_node.g or neighbour_node not in to_visit:
                neighbour_node.h = distance(neighbour_point, end.position)
                neighbour_node.g = current.g + 1
                neighbour_node.parent = current
                hq.heapify(to_visit)

                if neighbour_node not in to_visit:
                    hq.heappush(to_visit, neighbour_node)

    trail_length = 0
    while current.parent:
        current = current.parent
        trail_length += 1
    return trail_length


def replace_occurence(n: int, text: str, replace_from: str, replace_to: str) -> str:
    '''Swap the n-th occurence of a letter with another in text'''

    count: int = 0
    for i, c in enumerate(text):
        if c == replace_from and (count := count + 1) == n:
            return text[:i] + replace_to + text[i + 1:]
    return text


def parse_grid(text: str) -> Tuple[Grid, Node, Node]:
    '''Parse input text into a grid'''

    rows: List[str] = text.split('\n')
    grid: List[List[Node]] = []
    start: Node = Node((-1, -1), 0, 0, 0, None)
    end: Node = Node((-1, -1), 0, 0, 0, None)

    for i, row in enumerate(rows):
        col = []
        for j, elem in enumerate(row):
            if elem == 'E':
                col.append(start := Node((i, j), 0, 0, float('inf'), None))
            elif elem == 'a':
                col.append(end := Node((i, j), 25, float('inf'), 0, None))
            else:
                col.append(Node((i, j), ord(elem) - 97, float('inf'), float('inf'), None))
        grid.append(col)
    if start and end:
        start.h = distance(start.position, end.position)
    return (grid, start, end)

def main():
    with open('input.txt', 'r') as file:
        grid: Grid
        start: Node
        end: Node
        paths_from_a: Set[int] = set()
        
        text: str = file.read()
        # grid, start, end = parse_grid(text)
        # print(f' Part 1: {a_star(grid, start, end)}')

        grid, start, end = parse_grid(text)
        print(f' Part 2: {a_star(grid, start, end)}')
        # text = text.replace('S', 'a')
        # counter: int = 1
        # while 'S' in (current_grid := replace_occurence(counter, text, 'a', 'S')):
        #     print('current grid: ', current_grid)
        #     counter += 1
        #     grid, start, end = parse_grid(current_grid)
        #     paths_from_a.add(a_star(grid, start, end))
        #     current_grid = current_grid.replace('S', 'a')
        # print(f' Part 2: {min(paths_from_a)}')



if __name__ == '__main__':
    main()