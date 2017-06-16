# solve sudoku puzzle
# reference: http://norvig.com/sudoku.html

import pprint

def cross(A,B):
    """ Cross product of elements in A and elements in B. """
    return [a+b for a in A for b in B]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = '123456789'
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u]) for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in squares)


#############  Unit test ########################
def tests():
    """ Test set"""
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C3', 'C4', 'C5',
                               'C6', 'C7', 'C8', 'C9', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'])
    print('Test passed.')


############## Constraint propagation ####################
def eliminate(values, s, d):
    """ Eliminate d from values[s]; propagate when values or places <=2, return values
    if a contradiction is detect, return false."""
    if d not in values[s]:
        return values  # already eliminated

    values[s] = values[s].replace(d, '')
    # (1) If a square is reduced to one value d2, then eliminated d2 from peers
    if len(values[s]) == 0:
        return False  # at least 1
    elif len(values[s]) == 1:
        if not all(eliminate(values, s2, values[s]) for s2 in peers[s]):
            return False

    # (2) If a unit u is reduced to only one space for a value d, then put it there
    for u in units[s]:
        dplace = [s for s in u if d in values[s]]
        if len(dplace) == 0:
            return False # no place contradition
        elif len(dplace) == 1:
            if not assign(values, dplace[0], d):
                return False
    return values


def assign(values, s, d):
    """ Eliminate all the other values (except d) from values[s] return values
     if a contradiction is detect, return False"""
    eliminate_values = values[s].replace(d, '')
    if all(eliminate(values, s, eliminate_values)):
        return values
    else:
        return False


############## parse a grid ###########################
def grid_value(grid):
    """ Convert a grid into a dict of {square, digit} with '.' for empties"""
    chars = [c for c in grid if c in digits or c is '.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


def parse_grid(grid):
    """
    Convert the grid to a dict of possible values, {squares, values}
    or return False if a contradiction is detected.
    """
    values = dict((s, digits) for s in squares)
    for s,d in grid_value(grid).items():
        if d in digits and not assign(values, s, d):
            return False
    return values






