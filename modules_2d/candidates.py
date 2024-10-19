import tkinter as tk
from collections import defaultdict

from modules_2d import legal

def find_all(self):
    self.candidates = defaultdict(set)
    self.cand_locations = defaultdict(set)
    for i in range(9):
        for j in range(9):
            if self.grid[i][j] == 0:
                    for num in range(1,10):
                        if legal.check(self, i, j, num):
                            self.candidates[(i,j)].add(num)
                            self.cand_locations[num].add((i,j))

    # sorting squares by fewest remaining candidates
    self.candidates = {pos: cand_list for pos, cand_list in sorted(self.candidates.items(), key= lambda item: len(item[1]))}

    # creating candidate boxes board
    self.frm_cand_square=[[None]*9 for x in range(9)]
    self.lbl_cand_squares=[[[None]*9 for x in range(9)] for y in range(9)]
    for i in range(9):
        for j in range(9):
            self.frm_cand_square[i][j] = tk.Frame(master=self.frm_square[i][j], relief = 'sunken', bd = -2)
            if self.grid[i][j] == 0:
                self.ent_number[i][j].pack_forget()
                for num in range(1,10):
                    k = num-1
                    if num in self.candidates[(i,j)]:
                        self.lbl_cand_squares[i][j][k] = tk.Label(master=self.frm_cand_square[i][j], text=num, font = ('Verdana Pro', 8), bd = -2, bg = 'white', width = 1, pady = 0, padx = 3)
                    else:
                        self.lbl_cand_squares[i][j][k] = tk.Label(master=self.frm_cand_square[i][j], text='', font = ('Verdana Pro', 8), bd = -2, bg = 'white', width = 1, pady = 0, padx = 3)
                    self.lbl_cand_squares[i][j][k].grid(row = k//3, column = k%3)
                self.frm_cand_square[i][j].pack(fill="none", expand=True)
    
    self.candidates_found = True

def remove(self,pos,num):
    self.candidates[pos].remove(num)
    self.cand_locations[num].remove(pos)
    self.lbl_cand_squares[pos[0]][pos[1]][num-1].configure(text='')

def update(self,row,col,num):
    for pos, cand_list in self.candidates.items():
        i, j = pos[0], pos[1]
        if any([i == row, j == col, ((i//3 == row//3) and (j//3 == col//3))]):
            if num in cand_list:
                self.candidates[(i,j)].remove(num)
                self.cand_locations[num].remove((i,j))
                self.lbl_cand_squares[i][j][num-1].configure(text='')
    for cand in self.candidates[(row,col)]:
        self.cand_locations[cand].remove((row,col))
    del self.candidates[(row,col)]