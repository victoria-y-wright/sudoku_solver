from modules_3d import legal

def rec_solve(self, index):
        
        if index == len(self.squares_list):     # if have filled all squares then sudoku is solved
            return True
        
        pos = self.squares_list[index]
        box, sq = pos[0], pos[1]
        
        if self.grid[box][sq] != 0:            # if already filled move on to next square 
            return rec_solve(self, index+1)

        cands = range(1,10) if self.candidates_found == False else self.candidates[(box,sq)]
        for num in cands:
            if legal.check(self, pos, num):
                self.grid[box][sq] = num
                if self.var_show_iterating.get() == 1:
                    if self.candidates_found == True:
                        for k in range(9):
                            self.cnv_board.itemconfigure(self.lbl_cand_square[box][sq][k], state = 'hidden')
                            self.cnv_board.itemconfigure(self.shp_cand_square[box][sq][k], state = 'hidden')
                    self.cnv_board.itemconfigure(self.lbl_square[box][sq], text = self.grid[box][sq])
                    self.window.after(10,self.window.update())

                if rec_solve(self, index+1):
                    return True
            self.grid[box][sq] = 0

            if self.var_show_iterating.get() == 1:
                self.cnv_board.itemconfigure(self.lbl_square[box][sq], text = '')
                if self.candidates_found == True:
                    for k in range(9):
                        self.cnv_board.itemconfigure(self.lbl_cand_square[box][sq][k], state = 'normal')
                self.window.update() 
        return False