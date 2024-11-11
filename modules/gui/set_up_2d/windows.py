from modules.gui.set_up_2d import puzzle_entry
from modules.gui import visualisation
from copy import deepcopy

def go_to_1(self):
    self.frm_top.pack(pady=5)
    self.frm_board.pack()
    self.frm_controls.pack(pady=(5,20))
    self.frm_bot.pack()

    self.candidates_found = False
    puzzle_entry.grid_creation(self)

def leave_1(self):
    self.frm_controls.pack_forget()
    self.frm_bot.pack_forget()

def go_to_2(self):
    self.frm_body_buttons.pack()

    self.btn_candidates.configure(state='active')
    self.btn_brute_force.configure(relief='raised')

def leave_2(self):
    self.frm_body_buttons.pack_forget()
    visualisation.reset_board(self)

def go_to_3(self):
    self.frm_iterating.pack()

def leave_3(self):
    self.frm_iterating.pack_forget()

def go_to_solved(self):
    self.frm_solved.pack()

def leave_solved(self):
    self.frm_solved.pack_forget()

    self.grid = deepcopy(self.initial_grid)
    for i in range(9):
        for j in range(9):
            if self.grid[i][j] == 0:
                self.entry_text[i][j].set('')
    self.window.update()

def go_to_no_solution(self):
    self.frm_no_sol.pack()
  
def leave_no_solution(self):
    self.frm_no_sol.pack_forget()

