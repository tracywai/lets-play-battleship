"""Battleship Functions"""

# Use these constants in your code
from typing import TextIO, List

MIN_SHIP_SIZE = 1
MAX_SHIP_SIZE = 10
MAX_GRID_SIZE = 10
UNKNOWN = "-"
EMPTY = "."
HIT = "X"
MISS = "M"


def read_ship_data(game_file: TextIO) -> List:
    """
    Return a list containing the ship characters in game_file as a list
    of strings at index 0, and ship sizes in game_file as a list of ints
    at index 1.
    """

    ship_characters = game_file.readline().split()

    ship_sizes = game_file.readline().split()

    for i in range(len(ship_sizes)):
        ship_sizes[i] = int(ship_sizes[i])

    return [ship_characters, ship_sizes]

def has_ship(fleet: List[List[str]], row: int, col: int,
             schar: str, shipsize: int) -> bool:
    """
    Return True if and only if the ship appears with the correct size,
    completely in a row or a completely in a column at the given starting cell

    >>> has_ship([[EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],['a','b','d',EMPTY,EMPTY],[EMPTY,EMPTY,'e',EMPTY,EMPTY],\
    ['c',EMPTY,EMPTY,EMPTY,EMPTY]],1,2,'d',1)
    True
    >>> has_ship([[EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],[EMPTY,'b','d',EMPTY,EMPTY],[EMPTY,EMPTY,'e',EMPTY,EMPTY],\
    ['c',EMPTY,EMPTY,EMPTY,EMPTY]],1,0,'d',1)
    False
    >>> has_ship([['a',EMPTY,'d',EMPTY,EMPTY],['a','b','d',EMPTY,EMPTY],[EMPTY,EMPTY,'e',EMPTY,EMPTY],\
    ['c',EMPTY,EMPTY,EMPTY,EMPTY]],0,1,'d',1)
    False
    """
    ship_count = 0
    starter = fleet[row][col]
    for gamerow in fleet:
        ship_count = gamerow.count(schar)
    if not ship_count == shipsize and not starter == schar:
        return False
    return True

def validate_character_count(fleet: List[List[str]], schar: List[str],
                             shipsize: List[int]) -> bool:
    """
    Return True if and only if the grid contains the correct number of
    ship characters for each ship and the correct number of empty characters.
    Precondition: len(schar) == len(shipsize) and 
    (MIN_SHIP_SIZE <= shipsize <= MAX_SHIP_SIZE)
    >>> validate_character_count([[EMPTY,'a','b'],[EMPTY, EMPTY,'b'],[EMPTY, EMPTY, EMPTY],['d','d','d']], ['a','b','d'],[1,2,3])
    True
    >>> validate_character_count([[EMPTY,'a','b','c'],[EMPTY, EMPTY, 'b','c'],[EMPTY, EMPTY, EMPTY, 'c'],['d','d','d',EMPTY]], ['a','b','c','d'],[1,2,3,3])
    True
    >>> validate_character_count([['a','a','b','c'],[EMPTY, EMPTY, 'b','c'],[EMPTY, EMPTY, 'b','c'],['d','d','d',EMPTY]], ['a','b','c','d'],[1,2,3,3])
    False
    """
    for i in range(len(schar)):
        ship_count = 0
        empty_count = 0
        for row in fleet:
            ship_count = ship_count + row.count(schar[i])
            empty_count = empty_count + row.count(EMPTY)
        if not ship_count == shipsize[i]:
            return False
    return True

def validate_ship_positions(fleet: List[List[str]], schar: List[str],
                            shipsize: List[int]) -> bool:
    """
    Return True if and only if the grid contains each ship aligned
    completely in a row or column. It should check that each ship is contained
    completely in consecutive cells all in the same row, or all in
    the same column, depending on if it is oriented horizontally
    or vertically (no other orientation)
    Precondition: len(ship_char) == len(sizes)
    >>> validate_ship_positions([[EMPTY,'b',EMPTY], [EMPTY,'b',EMPTY], ['a','a','a']],['a', 'b'],[3, 2])
    True
    >>> validate_ship_positions([[EMPTY,'a',EMPTY,'b'],[EMPTY,'a',EMPTY,'b'],[EMPTY,'a',EMPTY,EMPTY]],['a','b'],[3,2])
    True
    >>> validate_ship_positions([['a','a',EMPTY,'b'],[EMPTY,EMPTY,EMPTY,'b'],['c','c','c',EMPTY]],['a','b','c'],[2,2,3])
    True
    >>> validate_ship_positions([['a','a',EMPTY,'b'],[EMPTY,EMPTY,EMPTY,'b'],['c','c','c',EMPTY]],['a','b','c'],[1,1,1])
    False
    """
    rowcol = []
    for i in range(len(schar)):
        contains_ship = True
        for row, col in rowcol:
            if has_ship(fleet, row, col, schar[i], shipsize[i]) ==\
               contains_ship:
                contains_ship = True
            elif has_ship(fleet, row, col, schar[i], shipsize[i]) != \
                 contains_ship:
                contains_ship = False
    return contains_ship    
    
    #newrowcol = []
    #for row in range(len(fleet)):
        #for col in range(len(fleet[row])):
            #newrowcol.append([row, col])
            
    #for i in range(len(shipsize)):
        #for row, col in newrowcol:
            #if has_ship(fleet, row, col, schar[i], shipsize[i]):
                #return True
            #if not has_ship(fleet, row, col, schar[i], shipsize[i]):
                #return False
    #return True
        
def validate_fleet_grid(fleet: List[List[str]], schar: List[str],\
                        shipsize: List[int]) -> bool: 
    """
    Return True if and if the potential fleet grid is a valid fleet grid.
    >>> validate_fleet_grid([[EMPTY,'a',EMPTY,'b'],[EMPTY,'a',EMPTY,'b'],[EMPTY,'a',EMPTY,EMPTY]], ['a','b'],[3,2])
    True
    >>> validate_fleet_grid([['a','a',EMPTY,'b'],[EMPTY,EMPTY,EMPTY,'b'],['c','c','c',EMPTY]],['a','b','c'],[2,2,3])
    True
    >>> validate_fleet_grid([['d','a',EMPTY,'b'],['d',EMPTY,EMPTY,'b'],['c','c','c',EMPTY]],['a','b','c','d'],[2,2,3,1])
    False
    """
    return validate_ship_positions(fleet, schar, shipsize) and\
           validate_character_count(fleet, schar, shipsize)

def is_valid_cell(row_a: int, col_a: int, gridsize: int) -> bool: 
    """
    Precondition: gridsize <= MAX_GRID_SIZE
    Returns True if and only if the cell specified by the row and the 
    column is a valid cell inside a square grid of that size 
    >>> is_valid_cell(2, 3, 6)
    True
    >>> is_valid_cell(1, 5, 4)
    False
    >>> is_valid_cell(7, 6, 8)
    True
    """
    if gridsize > MAX_GRID_SIZE:
        return False
    return (row_a and col_a) <= gridsize

def is_not_given_char(row: int, col: int, gridsize: List[List[str]],\
                      char: str) -> bool: 
    """
    Returns True iff the cell specified by the row and column is not the 
    given character.
    
    >>> is_not_given_char(1,2,[['a','b','d',EMPTY,EMPTY],[EMPTY,EMPTY,'e',EMPTY,EMPTY],['c',EMPTY,EMPTY,EMPTY,EMPTY],['c',EMPTY,EMPTY,EMPTY,EMPTY]],'a')
    True
    >>> is_not_given_char(0,1,[['a','b','d',EMPTY,EMPTY],[EMPTY,EMPTY,'e',EMPTY,EMPTY],['c',EMPTY,EMPTY,EMPTY,EMPTY],['c',EMPTY,EMPTY,EMPTY,EMPTY]],'b')
    False
    >>> is_not_given_char(0,2,[['a','b','d',EMPTY,EMPTY],[EMPTY,EMPTY,'e',EMPTY,EMPTY],['c',EMPTY,EMPTY,EMPTY,EMPTY],['c',EMPTY,EMPTY,EMPTY,EMPTY]],'d')
    False
    """
    return gridsize[row][col] != char

def update_fleet_grid(row: int, col: int, fleet: List[List[str]],\
                      schar: List[str], shipsize: List[int], \
                      hits: List[int]) -> None: 
    """
    This function is called when there is a hit in the cell specified by the 
    row and column. 
    This function updates the fleet grid (by converting the ship character in 
    the cell to upper-case),and also the hits list to indicate that 
    there has been a hit.
    Precondition: len(schar) == len(shipsize) == len(hits)
    >>> fleet =  [['.', 'a'], ['.', 'a']]
    >>> hits = [0]
    >>> update_fleet_grid(0,1,fleet, ['a'],[2],hits)
    >>> fleet = [['.', 'A'], ['.', 'a']]
    >>> hits = [1]
    >>> fleet = [EMPTY, 'a', EMPTY, 'b'],[EMPTY,'c', 'c', 'b'],[EMPTY,EMPTY,EMPTY,EMPTY]
    >>> hits = [0,0,0]
    >>> update_fleet_grid(0,3,fleet, ['a','b','c'],[1,2,2],hits)
    >>> fleet = [EMPTY, 'a', EMPTY, 'B'],[EMPTY,'c', 'c', 'b'],[EMPTY,EMPTY,EMPTY,EMPTY]
    >>> hits = [0,1,0]
    >>> update_fleet_grid(1,3,fleet, ['a','b','c'],[1,2,2],hits)
    >>> fleet = (['.', 'a', '.', 'B'], ['.', 'c', 'c', 'B'], ['.', '.', '.', '.'])
    >>> hits = [0,2,0]
    
    """
    pos = 0
    if not fleet[row][col] == EMPTY and not \
       fleet[row][col].isupper():
        fleet[row][col] = fleet[row][col].upper()
        pos = schar.index(fleet[row][col].lower())
        hits[pos] = hits[pos] + 1
    if schar[pos] == hits[pos]:
        print_sunk_message(shipsize[pos], schar[pos])
        
def update_target_grid(row: int, col: int, target: List[List[str]],\
                       fleet: List[List[str]]) -> None:
    """
    Sets the element of the specified cell in the target grid to HIT or MISS 
    using the information from the corresponding cell from the fleet grid
    >>> target = [UNKNOWN,UNKNOWN,UNKNOWN,UNKNOWN],[UNKNOWN,UNKNOWN,UNKNOWN,UNKNOWN],[UNKNOWN,UNKNOWN,UNKNOWN,UNKNOWN],[UNKNOWN,UNKNOWN,UNKNOWN,UNKNOWN]
    >>> fleet = ([['a','a','b','d'], [EMPTY,EMPTY,EMPTY,'d'],['c',EMPTY,EMPTY,EMPTY],['c',EMPTY,EMPTY,EMPTY]]) 
    >>> update_target_grid(0,1,target,fleet)
    >>> target = [UNKNOWN,HIT,UNKNOWN,UNKNOWN],[UNKNOWN,UNKNOWN,UNKNOWN,UNKNOWN],[UNKNOWN,UNKNOWN,UNKNOWN,UNKNOWN],[UNKNOWN,UNKNOWN,UNKNOWN,UNKNOWN]
    >>> update_target_grid(1,1,target,fleet)
    >>> target = [HIT,UNKNOWN,UNKNOWN,UNKNOWN],[UNKNOWN,MISS,UNKNOWN,UNKNOWN],[UNKNOWN,UNKNOWN,UNKNOWN,UNKNOWN],[UNKNOWN,UNKNOWN,UNKNOWN,UNKNOWN]
    """
    if fleet[row][col] == EMPTY:
        target[row][col] = MISS
    elif fleet[row][col] != EMPTY:
        target[row][col] = HIT 
        
def is_win(shipsize: List[int], hits: List[int]) -> bool: 
    """
    Precondition: len(shipsize) == len(hits) 
    Returns True iff the number of hits for each ship in the hits list is
    the same as the size of each ship, i.e., if each ship has been sunk 
    >>> is_win([5,4,3,2,1],[5,4,3,2,1]) 
    True
    >>> is_win([5, 2, 2, 3, 1], [4, 2, 1, 2, 1])
    False
    >>> is_win([5,3,2,4,1], [5,4,3,2,1])
    False
    """ 
    for i in range(len(shipsize)): 
        if hits[i] != shipsize[i]:
            return False
    return True
    

def print_sunk_message(ship_size: int, ship_character: str) -> None: # this function calls in update_fleet_grid

    """
    Print a message telling player that a ship_size ship with ship_character
    has been sunk.
    """

    print("The size {0} {1} ship has been sunk!".format(ship_size, \
                                                        ship_character))


if __name__ == "__main__":
    import doctest

    doctest.testmod()     # uncomment this line in order to run the docstring examples

