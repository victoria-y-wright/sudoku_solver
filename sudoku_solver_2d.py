import tkinter as tk

from modules.gui import error_flags, squares_2d
from modules.gui.set_up_2d import widgets, windows, puzzle_entry
from modules.logic import legal, brute_force, candidates, apply_constraints

class SudokuSolver:
    def __init__(self, window):
        self.window = window
        self.window.title("Sudoku Solver")
        self.window.geometry("750x480")
        self.grid = [[None]*9 for x in range(9)]

        widgets.create(self)
        error_flags.set_up(self)
        windows.go_to_1(self)


    def puzzle_entered(self,event):
        error_flags.reset(self)
        
        input_valid = False
        if event.widget == self.btn_start: #start button
            if legal.board_only_numbers(self):
                input_valid = True
                puzzle_entry.from_grid(self)
            else:
                error_flags.flag(self, 0)

        elif event.widget == self.btn_start_paste: #paste start button
            paste_list = self.ent_start_paste.get().strip()
            if paste_list.isdigit() and len(paste_list) == 81:
                input_valid = True
                puzzle_entry.from_paste(self, paste_list)
            else:
                error_flags.flag(self, 3)
    
        if input_valid == True:
            if legal.board_not_empty(self):
                if legal.board_follows_rules(self):
                    puzzle_entry.valid_entered(self)
                    
                    windows.leave_1(self)
                    windows.go_to_2(self)
                else:
                    error_flags.flag(self, 2)
            else:
                error_flags.flag(self, 1)


### brute force ###
    def solve_with_brute_force(self):
        error_flags.reset(self)

        windows.leave_2(self)
        if self.var_show_iterating.get() == 1:
            windows.go_to_3(self)
        
        if brute_force.solve(self):
            if self.var_show_iterating.get() == 1:
                windows.leave_3(self)
            else:
                for pos in self.grid_all_squares:
                    if self.candidates_found == True:
                        squares_2d.hide_candidates(self, pos)
                squares_2d.set_value(self, pos, self.grid[pos[0]][pos[1]])
            windows.go_to_solved(self)

        else:
            if self.var_show_iterating.get() == 1:
                windows.leave_3(self)
            windows.go_to_no_solution(self)


    def back_to_initial(self):
        windows.leave_solved(self)
        windows.go_to_2(self)


### constraints ###
    def find_candidates(self):
        candidates.find_all(self)
        
        self.btn_candidates.configure(state='disabled')

    def solve_by_applying_constraints(self):
        error_flags.reset(self)

        if self.candidates_found == False:
            self.find_candidates()
        
        solved = False
        if self.var_step_by_step.get() == 0:
            solved = apply_constraints.full_solve(self)
        else:
            solved = (apply_constraints.one_step(self)) and (0 not in set([x for xs in self.grid for x in xs]))
 
        if solved is True:
            windows.leave_2(self)
            windows.go_to_solved(self)

        
if __name__ == "__main__":
    window = tk.Tk()
    app = SudokuSolver(window)
    window.mainloop() 