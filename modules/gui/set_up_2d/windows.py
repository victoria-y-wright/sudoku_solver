from modules.gui.set_up_2d import puzzle_entry
from modules.gui import visualisation
from copy import deepcopy

def go_to_1(self):
    self.frm_main.grid(row = 0, column= 0, pady=(10,0), padx=15)
    self.frm_controls.grid(row = 0, column = 1, pady=(10,0), padx = (0,15))
    self.candidates_found = False
    puzzle_entry.grid_creation(self)

def leave_1(self):
    self.frm_controls.grid_forget()

def go_to_2(self):
    self.frm_body_buttons.grid(row = 0, column = 1, pady=(10,0), padx = (0,15))

    self.btn_candidates.configure(state='active')
    self.btn_brute_force.configure(relief='raised')

def leave_2(self):
    self.frm_body_buttons.grid_forget()

    if self.candidates_found == True:
        visualisation.reset_board(self)

def go_to_3(self):
    self.frm_iterating.grid(row = 0, column = 1, pady=(10,0), padx = (0,15))

def leave_3(self):
    self.frm_iterating.grid_forget()

def go_to_solved(self):
    self.frm_solved.grid(row = 0, column = 1, pady=(10,0), padx = (0,15))

def leave_solved(self):
    self.frm_solved.grid_forget()

    self.grid = deepcopy(self.initial_grid)
    for i in range(9):
        for j in range(9):
            if self.grid[i][j] == 0:
                self.entry_text[i][j].set('')
    self.candidates_found = False
    self.window.update()

def go_to_no_solution(self):
    self.frm_no_sol.grid(row = 0, column = 1, pady=(10,0), padx = (0,15))
  
def leave_no_solution(self):
    self.frm_no_sol.grid_forget()

