import tkinter as tk

def set_value(self, pos, value): # used in brute_force
    if value == 0:
        self.entry_text[pos[0]][pos[1]].set('')
    else:
        self.entry_text[pos[0]][pos[1]].set(value)

def create_candidates(self): # used in candidates
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

def remove_candidate(self,pos,num): # used in candidates
    self.lbl_cand_squares[pos[0]][pos[1]][num-1].configure(text='')

def hide_candidates(self, pos): # used in brute_force
    self.frm_cand_square[pos[0]][pos[1]].pack_forget()
    self.ent_number[pos[0]][pos[1]].pack()

def show_candidates(self, pos): # used in brute_force
    self.ent_number[pos[0]][pos[1]].pack_forget()
    self.frm_cand_square[pos[0]][pos[1]].pack(side = 'top')

def change_cand_colour(self, pos, cand, colour): # used in visualisation
    self.lbl_cand_squares[pos[0]][pos[1]][cand-1].configure(bg=colour)

def change_cand_fg(self, pos, cand, colour): # used in visualisation
    self.lbl_cand_squares[pos[0]][pos[1]][cand-1].configure(fg=colour)

def change_square_colour(self, pos, colour): # used in visualisation
    self.ent_number[pos[0]][pos[1]].configure(bg=colour)
