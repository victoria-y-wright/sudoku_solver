import tkinter as tk
from copy import deepcopy

from modules.gui.set_up_3d import board_creation, puzzle_entry, windows, widgets, examples
from modules.logic import legal, brute_force, candidates, apply_constraints
from modules.gui import error_flags, squares_3d


class SudokuSolver3D:
    def __init__(self, window):
        self.window = window
        self.window.title("3D Sudoku Solver")
        self.window.geometry("1050x650")

        widgets.create(self)
        error_flags.set_up(self)
        windows.go_to_1(self)
    
    def example_puzzle(self, event):
        if event.widget == self.btn_ex_1:
            examples.start(self,1)
        elif event.widget == self.btn_ex_2:
            examples.start(self,2)
        elif event.widget == self.btn_ex_3:
            examples.start(self,3)
            
    choose_face_to_add = board_creation.choose_face_to_add
    choose_where_add = board_creation.choose_where_add
    add_new_face = board_creation.add_new_face

    def board_created(self):
        error_flags.reset(self)
        
        if len(self.faces) == 1:
            error_flags.flag(self,5)
        elif not board_creation.check_3d_board_valid(self):
            error_flags.flag(self,6)
        else:
            self.frm_example.pack_forget()
            self.frm_labels.pack_forget()
            puzzle_entry.create_grid(self)
            puzzle_entry.add_elements(self)
            puzzle_entry.resize_centre_canvas(self)

    input_number= puzzle_entry.input_number
    enter_number = puzzle_entry.enter_number

    def puzzle_entered(self):
        error_flags.reset(self)
        
        if legal.board_not_empty(self):
            if legal.board_follows_rules(self):
                puzzle_entry.valid_entered(self)

                windows.leave_1(self)
                windows.go_to_2(self)
            else:
                error_flags.flag(self, 2)
        else:
            error_flags.flag(self, 1)
    
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
                        squares_3d.hide_candidates(self, pos)
                squares_3d.set_value(self, pos, self.grid[pos[0]][pos[1]])
            windows.go_to_solved(self)

        else:
            if self.var_show_iterating.get() == 1:
                windows.leave_3(self)
            windows.go_to_no_solution(self)
        
    def back_to_initial(self):
        windows.leave_solved(self)
        windows.go_to_2(self)

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
    app = SudokuSolver3D(window)
    window.mainloop() 

