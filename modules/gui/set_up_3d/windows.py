from copy import deepcopy
from modules.gui import visualisation

def go_to_1(self):
    self.frm_main.grid(row = 0, column= 0, pady=(10,0), padx = 15)
    self.frm_controls.grid(row = 0, column = 1, pady=(10,0), padx = 15)

    self.candidates_found = False
    self.grid_all_squares = []

def leave_1(self):
    self.frm_controls.grid_forget()

def go_to_2(self):
    self.frm_body_buttons.grid(row = 0, column = 1, pady=(10,0), padx = 15)
    self.btn_candidates.configure(state='active')
    self.btn_brute_force.configure(relief='raised')

def leave_2(self):
    self.frm_body_buttons.grid_forget()
    
    if self.candidates_found == True:
        visualisation.reset_board(self)
def go_to_3(self):
    self.frm_iterating.grid(row = 0, column = 1, pady=(10,0), padx = 15)
  
def leave_3(self):
    self.frm_iterating.grid_forget()

def go_to_solved(self):
    self.frm_solved.grid(row = 0, column = 1, pady=(10,0), padx = 15)
  
def leave_solved(self):
    self.frm_solved.grid_forget()

    self.grid = deepcopy(self.initial_grid)
    for pos in self.grid_all_squares:
        i, j = pos[0], pos[1]
        if self.grid[i][j] == 0:
            self.cnv_board.itemconfigure(self.lbl_square[i][j], text = '')
    self.candidates_found = False
    self.window.update()
    
def go_to_no_solution(self):
    self.frm_no_sol.grid(row = 0, column = 1, pady=(10,0), padx = 15)
  
def leave_no_solution(self):
    self.frm_no_sol.grid_forget()
