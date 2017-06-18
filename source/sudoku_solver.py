# solve sudoku puzzle
# reference: http://norvig.com/sudoku.html

import time, random

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
    if all(eliminate(values, s, d2) for d2 in eliminate_values):
        return values
    else:
        return False


############## parse a grid ###########################
def grid_value(grid):
    """ Convert a grid into a dict of {square, digit} with '.' for empties"""
    chars = [c for c in grid if c in digits or c in '0.']
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


# #################### Display 2D grid##################
def display(values):
    width  = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*width*3]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)


# ############### search and solve #########################
def time_solve(grid, timelimit):
    start = time.clock()
    values = search(parse_grid(grid))
    t = time.clock() - start
    # Display puzzle that take long enough
    if timelimit is not 0 and t > timelimit:
        print "Puzzle takes unusual amount of time to be solved"
    return solved(parse_grid(getResult(values)))


def solve(grid, timelimit = 0):
    """ Attempt to solve a grid. When time limit is number of second, display
    puzzles that take longer. When timelimit is 0, dont display any puzzles"""
    result = time_solve(grid, timelimit)
    return result


def solved(values):
    """ A puzzle is solved if each unit is a permutation of digits 1 to 9"""
    def unitsovled(unit):
        return set(values[s] for s in unit) == set(digits)
    if values is not False and  all(unitsovled(unit) for unit in unitlist):
        return getResult(values)
    return False


def search(values):
    """ Using depth-first search and propagation, try all possible values."""
    if values is False:
        return False
    if all(len(values[s])==1 for s in squares):
        return values
    # Chose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s])>1)
    return some(search(assign(values.copy(), s, d))
                for d in values[s])


# ############### Utilities ###############################
def some(seq):
    """ Return some elements of seq that is true."""
    for e in seq:
        if e : return e
    return False


def shuffled(seq):
    """ Return a randomly shuffled copy of the input sequence"""
    seq = list(seq)
    random.shuffle(seq)
    return seq

def getResult(values):
    return [values[r+c] for r in rows for c in cols]


#  ################ System test #######################

def random_puzzle(N = 17):
    """ Make a random puzzle with N or more assignments. Restart on comtradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but emperiically
    about 99% of them are sovlable. Some have multiple solutions"""

    values = dict((s,digits) for s in squares)
    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(values[s] if len(values[s])==1 else '.' for s in squares)
    return random_puzzle(N)

grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'

if __name__ == '__main__':
    tests()
    display(grid_value(solve(hard1,10)))
    display(grid_value(solve(random_puzzle(), 10)))












