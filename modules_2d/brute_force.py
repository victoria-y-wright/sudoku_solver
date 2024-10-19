from modules_2d import legal

def rec_solve(self, index):
        
        if index == len(self.squares_list):     # if have filled all squares then sudoku is solved
            return True
        
        pos = self.squares_list[index]
        row, col = pos[0], pos[1]
        
        if self.grid[row][col] != 0:            # if already filled move on to next square 
            return rec_solve(self, index+1)

        cands = range(1,10) if self.candidates_found == False else self.candidates[(row,col)]
        for num in cands:
            if legal.check(self, row, col, num):
                self.grid[row][col] = num
                if self.var_show_iterating.get() == 1:
                    self.entry_text[row][col].set(self.grid[row][col])
                    if self.candidates_found == True:
                        self.frm_cand_square[row][col].pack_forget()
                        self.ent_number[row][col].pack()
                        self.window.update()
                    self.window.after(10,self.window.update())
                if rec_solve(self, index+1):
                    return True
            self.grid[row][col] = 0
            if self.var_show_iterating.get() == 1:
                self.entry_text[row][col].set('')
                if self.candidates_found == True:
                    self.ent_number[row][col].pack_forget()
                    self.frm_cand_square[row][col].pack(side = 'top')
                    self.window.update()
                self.window.update() 
        return False