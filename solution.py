assignments = []

# Define Rows
rows = 'ABCDEFGHI'
#Define Columns
cols = '123456789'
#Define reverse columns for solving diagnol Sudoku
#reverseCols = '987654321'
reverseCols = cols[::-1]
#function for Cross
def cross(a, b):
    return [s+t for s in a for t in b]
#Calling Cross function
if rows is not None and cols is not None:
    boxes = cross(rows, cols)

#Declaring diagnols for diagnol sudoku - Changed as per suggestions from reviewer
diagonal_units = [[r+c for r,c in zip(rows,cols)], [r+c for r,c in zip(rows,cols[::-1])]]
#Declaring Row Units
row_units = [cross(r, cols) for r in rows]
#Declaring Column units
column_units = [cross(rows, c) for c in cols]
#Declaring Square Units
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#Declaring unitlist including diagonal units
unitlist = row_units + column_units + square_units + diagonal_units
#Declaring units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
#Declaring peers
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
#Test Grids
"""
gridString = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
gridString2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

gridString2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
"""
def assign_value(values, box, value):
    """
    if values[box] == value:
       return values
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def remove_naked_twins(values):
    # Remove_naked_twins function to remove naked twins values from their peers
    possible_twins = [box for box in values.keys () if len ( values[box] ) == 2]
    naked_twins = [[box1, box2] for box1 in possible_twins for box2 in peers[box1] if set ( values[box1] ) == set ( values[box2] )]
    for i in range ( len ( naked_twins ) ):
        box1 = naked_twins[i][0]
        box2 = naked_twins[i][1]

        peers1 = set ( peers[box1] )
        peers2 = set ( peers[box2] )
        newPeers = peers1 & peers2

        for newPeerValue in newPeers:
            if len ( values[newPeerValue] ) > 2:
                for removeValue in values[box1]:
                    values = assign_value ( values, newPeerValue, values[newPeerValue].replace ( removeValue, '' ) )
                    #print("Returned Values from Naked twins :: ",values)
    return values


def naked_twins(values):
    #Naked twins function created to call remove_naked_twins methods under while loop. This is done because there can be possiblity that grid returned from remove_naked_twins
    #method can have more naked twins values and grid can be refined further
    no_more_twins = False
    while not no_more_twins:
        solved_naked_twins_grid_before = values.copy()
        values = remove_naked_twins(values)
        solved_naked_twins_grid_after = values.copy()
        #Calling while loop again if there is some change done to original grid by remove_naked_twins method.
        #if there is a change in 2 grids before and after calling remove_naked_twins method then we call while loop again - In order to refine grid more.
        no_more_twins = solved_naked_twins_grid_before == solved_naked_twins_grid_after
        
    return values

def grid_values(gridString):
    #grid_values function to replace all '.' by '123456789'
    values = []
    all_digits = cols
    for c in gridString:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    #display(dict(zip(boxes, values)))
    return dict(zip(boxes, values))

def display(values):
    #Display function to display 9*9 sudoku grid
    print('\n')
    if values is not None:
        width = 1 + max(len(values[s]) for s in boxes)
        if width is not None:
            line = '+'.join(['-'*(width*3)]*3)
        for r in rows:
            print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
            if r in 'CF': print(line)
    return

def eliminate(values):
    #eliminate method based on elimination algorithm.
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            #values[peer] = values[peer].replace(digit,'')
            values = assign_value ( values, peer, values[peer].replace ( digit, '' ) )
    #display(values)
    return values

def only_choice(values):
    #only choice method based on only_choice algorithm
    for unit in unitlist:
        for digit in cols:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                values = assign_value ( values, dplaces[0], digit )
    #display(values)
    return values


def reduce_puzzle(values):
    # Reduce puzzle - Imp method to call all 3 algorithms(eliminate,only_choice and naked_twins) again and again till before_grid!=after_grid - This will refine the grid.
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    #search method to define the search algorithm.
    values = reduce_puzzle(values)

    if values == False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values

    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):

    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #print("Starting from Main Method")
    #diagnol_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    reviewSudokuGrid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    newGrid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    #Display Call has been commented out to verify test results
    display(solve(newGrid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
