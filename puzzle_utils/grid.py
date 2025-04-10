"""
A Grid class and other utilities for working with grids.

To be clear, these are *grid* utilities, not *coordinate plane* utilities.
That means that (0, 0) is in the upper left, and the row number (y axis)
comes before the column number (x axis), because that's how we think of grids.
"""
# That is:
#
#        GRID              PLANE
#       1 2 3 4         4
#     1   |             3 - *
#     2   |             2   |
#     3 - *             1   |
#     4                   1 2 3 4
#   star at (3, 2)    star at (2, 3)
#
# though of course the upper left of an actual Grid object is (0, 0).

# Directions are (dx, dy)
NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)
NORTHWEST = (-1, -1)
SOUTHWEST = (1, -1)
NORTHEAST = (-1, 1)
SOUTHEAST = (1, 1)

DIRECTIONS = (NORTH, NORTHEAST, EAST, SOUTHEAST,
              SOUTH, SOUTHWEST, WEST, NORTHWEST)

CARDINALS = (NORTH, EAST, SOUTH, WEST)


def turn_cw(direction):
    """
    Given a (dx, dy) direction, return the direction 90 degrees clockwise.
    """
    dx, dy = direction
    return dy, -dx


def turn_ccw(direction):
    """
    Given a (dx, dy) direction, return the direction 90 degrees
    counterclockwise.
    """
    dx, dy = direction
    return -dy, dx


def turn_180(direction):
    """
    Given a (dx, dy) direction, return the opposite direction.
    """
    dx, dy = direction
    return -dx, -dy


# Aliases for the spacially-challenged (i.e., me)
turn_right = turn_cw
turn_left = turn_ccw
turn_around = turn_180


def move(start, direction, distance=1):
    """
    Given a starting coordinate and a direction, and optionally a distance,
    return the coordinate that distance in that direction.
    """
    x, y = start
    dx, dy = direction
    return (x + dx * distance, y + dy * distance)


class Grid(dict):
    """
    A subclass of dictionary to hold rectangular grids, i.e. mappings from
    (row, column) coordinates to the (usually length-1) string at that
    coordinate.
    """
    def __init__(self, grid):
        # Note that this does not have error-checking to ensure that the grid
        # doesn't have holes or is otherwise going to cause problems later.
        super().__init__(grid)
        mr, mc = max(self)
        self.rows = mr + 1
        self.columns = mc + 1

    @classmethod
    def from_text(cls, grid_text, sep=None):
        """
        Given a string as line-separated rows, make a Grid out of it.  By
        default, rows are expected to be undelimited, but a separator `sep`
        can be spcified.
        """
        if sep is None:
            sepfunc = lambda x: x
        else:
            sepfunc = lambda x: x.split(sep)
        dic = {}
        for row, line in enumerate(grid_text.splitlines()):
            for col, entry in enumerate(sepfunc(line)):
                dic[(row, col)] = entry
        return cls(dic)

    @classmethod
    def from_dimensions(cls, row, col, default=''):
        """
        Get an empty grid with the given dimensions.  All cells will be filled
        with the provided default value (default: the empty string).
        """
        return cls({(a, b): default for b in range(col) for a in range(row)})

    def to_text(self, sep=''):
        """
        Turn a Grid dictionary into a printable string, with rows separated by
        newlines and the cells in each row separated by `sep`.
        """
        return '\n'.join(
            sep.join(self[(r, c)] for c in range(self.columns))
            for r in range(self.rows)
        )

    def get_row(self, rownum):
        """
        Given a row number, return the contents of that row (as a list).
        """
        return [self[(rownum, c)] for c in range(self.columns)]

    def get_column(self, colnum):
        """
        Given a column number, return the contents of that column (as a list).
        """
        return [self[(r, colnum)] for r in range(self.rows)]

    def get_neighbors(self, coord, diagonals=False):
        """
        Given a coordinate, get a list of the contents of adjacent coordinates,
        clockwise from north.  If `diagonals` is False, includes only the four
        orthogonally adjacent cells; if True, includes all eight surrounding
        cells.

        Coordinates outside the grid will be skipped (so a coordinate on an
        edge will have three neighbors, or five if diaonals are included).
        """
        neighbors = []
        directions = DIRECTIONS if diagonals else CARDINALS
        for direction in directions:
            nb = move(coord, direction)
            if nb in self:
                neighbors.append(self[nb])
        return neighbors

    def get_line(self, coord, direction, distance, past_edge=None):
        """
        Given a coordinate, a direction, and a length, get the contents of
        that many cells in the direction from the coordinate, *including the
        starting point*.

        If `past_edge` is None, this function returns None if the line goes
        past the edge of the grid.  Otherwise, cells past the edge will be
        returned as the supplied `past_edge` value.
        """
        if (past_edge is None
            and move(coord, direction, distance - 1) not in self):
            return
        return [self.get(move(coord, direction, i), past_edge)
                for i in range(distance)]
