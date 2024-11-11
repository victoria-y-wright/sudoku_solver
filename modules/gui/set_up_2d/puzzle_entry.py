from copy import deepcopy
import tkinter as tk

def grid_creation(self):
    self.grid_all_squares = []
    self.grid_rows = []
    for i in range(9):
        new_row = set()
        new_col = set()
        for j in range(9):
            new_row.add((i,j))
            new_col.add((j,i))
            self.grid_all_squares.append((i,j))
        self.grid_rows.append(new_row)
        self.grid_rows.append(new_col)

    self.grid_boxes = []
    for box_row in [0,3,6]:
        for box_col in [0,3,6]:
            new_box = set()
            for i in range(3):
                for j in range(3):
                    new_box.add((box_row+i,box_col+j))
            self.grid_boxes.append(new_box)

def from_grid(self):
    for i in range(9):
        for j in range(9):
            if len(self.ent_number[i][j].get()) != 0:
                    self.grid[i][j]=int(self.ent_number[i][j].get())
            else:
                self.grid[i][j] = 0

def from_paste(self, paste_list):
    for i in range(9):
        for j in range(9):
            self.grid[i][j] = int(paste_list[i*9+j])
            if self.grid[i][j] != 0:
                self.entry_text[i][j].set(self.grid[i][j])
            else:
                self.entry_text[i][j].set('')

def valid_entered(self):
    for i in range(9):
        for j in range(9):
            if self.grid[i][j] != 0:
                    self.ent_number[i][j].config(state=tk.DISABLED)
            else:
                self.entry_text[i][j].set('')
    self.initial_grid = deepcopy(self.grid)