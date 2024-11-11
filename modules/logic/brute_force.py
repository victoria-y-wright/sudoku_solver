from math import log2, ceil

from modules.logic import legal
from modules.gui import visualisation

import __main__
if "2d" in __main__.__file__:
    from modules.gui import squares_2d as squares
else:
    from modules.gui import squares_3d as squares

def solve(self):
    visualisation.reset_board(self)
    if self.candidates_found == True:
        self.candidates = {pos: cand_list for pos, cand_list in sorted(self.candidates.items(), key= lambda item: len(item[1]))}
    self.squares_list = self.grid_all_squares if self.candidates_found == False else list(self.candidates.keys())
    
    self.iterations = 0
    return rec_solve(self, 0)

def rec_solve(self, index):
        # sudoku is solved when all squares are filled
        if index == len(self.squares_list):
            return True
        
        pos = self.squares_list[index]
        
        # move onto next square if current square is already filled
        if self.grid[pos[0]][pos[1]] != 0:            
            return rec_solve(self, index+1)

        cands = range(1,10) if self.candidates_found == False else self.candidates[pos]
        
        for num in cands:
            if legal.check(self, pos, num):
                self.grid[pos[0]][pos[1]] = num

                if self.var_show_iterating.get() == 1:
                    if self.candidates_found == True:
                        squares.hide_candidates(self, pos)                    
                        self.window.update()    

                    squares.set_value(self,pos,num)

                    if self.var_speed_up.get() == 0:
                        self.window.after(10,self.window.update())
                    elif self.iterations % (4 * ceil(log2(self.iterations))) == 0:
                            self.window.after(1,self.window.update())

                if rec_solve(self, index+1):
                    return True
                self.iterations += 1

            self.grid[pos[0]][pos[1]] = 0

            if self.var_show_iterating.get() == 1:
                if self.candidates_found == True:
                    squares.show_candidates(self, pos)
                    self.window.update()    

                squares.set_value(self,pos,0)

                self.window.update() 

        return False