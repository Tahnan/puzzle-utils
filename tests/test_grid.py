import itertools

import pytest

from puzzle_utils import grid

SAMPLE_GRID = """
ABCDE
FGHIJ
KLMNO
PQRST
""".strip()


def test_turn_functions():
    directions = grid.CARDINALS + (grid.CARDINALS[0],)
    for source, destination in itertools.pairwise(directions):
        assert grid.turn_cw(source) == destination
        assert grid.turn_ccw(destination) == source
    assert grid.turn_180(grid.NORTH) == grid.SOUTH


def test_move():
    assert grid.move((3, 2), (1, -1)) == (4, 1)
    assert grid.move((3, 2), (1, -1), distance=10) == (13, -8)


def test_grid_class():
    small = grid.Grid({(0, 0): 'A', (0, 1): 'B'})
    assert small.rows == 1
    assert small.columns == 2

    from_dims = grid.Grid.from_dimensions(3, 2, default='.')
    from_dims[(1, 1)] = '*'
    assert from_dims.to_text() == '..\n.*\n..'


def test_grid_from_text():
    # Somewhat deeper tests for from_text(), which is the usual entry point
    standard = grid.Grid.from_text(SAMPLE_GRID)
    assert standard.rows == 4
    assert standard.columns == 5
    assert standard[(1, 2)] == 'H'
    assert standard.to_text() == SAMPLE_GRID
    assert standard.to_text(sep='|').splitlines()[0] == 'A|B|C|D|E'

    badly_split = grid.Grid.from_text('A B\nC D')
    assert len(badly_split) == 6
    assert badly_split[(0, 1)] == ' '
    assert badly_split[(1, 2)] == 'D'

    well_split = grid.Grid.from_text('A B\nC D', sep=' ')
    assert len(well_split) == 4
    assert well_split[(1, 1)] == 'D'


def test_grid_retrieval_methods():
    standard = grid.Grid.from_text(SAMPLE_GRID)
    assert standard.get_row(2) == ['K', 'L', 'M', 'N', 'O']
    assert standard.get_column(2) == ['C', 'H', 'M', 'R']

    # Errors are standard exceptions
    with pytest.raises(KeyError):
        standard.get_row(6)

    assert standard.get_neighbors((1, 1)) == ['B', 'H', 'L', 'F']
    assert standard.get_neighbors((1, 1), diagonals=True) == [
        'B', 'C', 'H', 'M', 'L', 'K', 'F', 'A'
    ]
    assert standard.get_neighbors((3, 4)) == ['O', 'S']
    assert standard.get_neighbors((3, 4), diagonals=True) == ['O', 'S', 'N']

    assert standard.get_line((1, 1), grid.SOUTHEAST, 3) == ['G', 'M', 'S']
    assert standard.get_line((1, 1), grid.SOUTHEAST, 4) is None
    assert standard.get_line((1, 1), grid.SOUTHEAST, 4, past_edge='#') == [
        'G', 'M', 'S', '#'
    ]
