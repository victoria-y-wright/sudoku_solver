from math import log2, ceil

from modules_logic import legal

import __main__
if "2d" in __main__.__file__:
    from modules_gui import squares_2d as squares
else:
    from modules_gui import squares_3d as squares


def rec_solve(self, index):
        
        # sudoku is solved when all squares are filled
        if index == len(self.squares_list):
            return True
        
        pos = self.squares_list[index]
        i, j = pos[0], pos[1]
        
        # move onto next square if current square is already filled
        if self.grid[i][j] != 0:            
            return rec_solve(self, index+1)

        cands = range(1,10) if self.candidates_found == False else self.candidates[(i,j)]
        
        for num in cands:
            if legal.check(self, pos, num):
                self.grid[i][j] = num

                if self.var_show_iterating.get() == 1:
                    if self.candidates_found == True:
                        squares.hide_candidates(self,pos)                    
                        self.window.update()    

                    squares.set_value(self,pos,num)

                    if self.var_speed_up.get() == 0:
                        self.window.after(10,self.window.update())
                    elif self.iterations % (4 * ceil(log2(self.iterations))) == 0:
                            self.window.after(1,self.window.update())

                if rec_solve(self, index+1):
                    return True
                self.iterations += 1

            self.grid[i][j] = 0

            if self.var_show_iterating.get() == 1:
                if self.candidates_found == True:
                    squares.show_candidates(pos)
                    self.window.update()    

                squares.set_value(self,pos,0)

                self.window.update() 

        return False