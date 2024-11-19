"""Functions used for brute-force solving by recursion & backtracking"""

from math import log2, ceil

from modules.logic import legal

import __main__
if "3d" in __main__.__file__:
    from modules.gui import squares_3d as squares
else:
    from modules.gui import squares_2d as squares

def solve(self):
    """Initialises recursive solving, by preparing list of squares to be filled and calling the rec_solve function"""
    
    # sorting the list of squares by fewest candidates, if found, to minimise backtracking 
    if self.candidates_found == True:
        self.candidates = {pos: cand_list for pos, cand_list in sorted(self.candidates.items(), key= lambda item: len(item[1]))}
    
    # setting the list of squares that need to be filled
    self.squares_list = self.grid_all_squares if self.candidates_found == False else list(self.candidates.keys())
    
    self.iterations = 0
    # starting the recursive solving from the first position in 'self.squares_list'
    return rec_solve(self, 0)


def rec_solve(self, index):
    """Recursively solves sudoku puzzle (self.grid) by filling in numbers for all of the positions in self.squares_list"""
    
    # base case: when all squares have been filled, puzzle is solved
    if index == len(self.squares_list):
        return True
    
    # get the current position from the list of all empty square positions
    pos = self.squares_list[index]
    
    # if the current square is already filled, move on to the next square
    if self.grid[pos[0]][pos[1]] != 0:            
        return rec_solve(self, index+1)

    # candidate numbers for the current square- use values 1-9 if candidates haven't been found
    cands = range(1,10) if self.candidates_found == False else self.candidates[pos]
    
    # try each candidate
    for num in cands:
        # check if placing 'num' at 'pos' is legal
        if legal.check(self, pos, num):
            # place the number in the grid
            self.grid[pos[0]][pos[1]] = num

            # optional visual updates, to show trialled number
            if self.var_show_iterating.get() == 1:
                # hide candidates if displayed
                if self.candidates_found == True:
                    squares.hide_candidates(self, pos)                    
                    self.window.update()    

                # display the chosen number
                squares.set_value(self,pos,num)

                # animation delay, adjusted for whether 'speed up?' has been selected
                if self.var_speed_up.get() == 0:
                    self.window.after(10,self.window.update())
                elif self.iterations % (4 * ceil(log2(self.iterations))) == 0:
                        self.window.after(1,self.window.update())

            # attempt to recursively solve the rest of the puzzle
            if rec_solve(self, index+1):
                return True     # solution found
            self.iterations += 1

        # if no solution was found, reset the square to 0 (empty) for backtracking
        self.grid[pos[0]][pos[1]] = 0

        # optional visual updates, to show bakctracking
        if self.var_show_iterating.get() == 1:
            # show candidates again if found
            if self.candidates_found == True:
                squares.show_candidates(self, pos)
                self.window.update()    

            # clear the display of the chosen number
            squares.set_value(self,pos,0)
            self.window.update() 

    # if no solution can be found with any number, return False to trigger backtracking
    return False