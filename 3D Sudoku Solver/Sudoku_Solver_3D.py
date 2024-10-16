import os
os.chdir("3D Sudoku Solver")


import tkinter as tk
from copy import deepcopy

from modules import board_set_up
from modules import grid_set_up
from modules import error_flags
from modules import legal
from modules import brute_force
from modules import candidates
from modules import constraints
from modules import windows_set_up


class SudokuSolver3D:
    def __init__(self, window):
        self.window = window
        self.window.title("3D Sudoku Solver")
        self.window.geometry("1000x600")

        windows_set_up.window_1(self)
        error_flags.set_up(self)
        self.candidates_found = False


    def start_example_click(self):
        self.frm_example.pack_forget()

        existing_face_index_list = [0, 0, 0, 1, 1, 5, 6]
        new_type_list = ['left', 'left', 'right', 'left', 'left', 'left', 'top']
        new_location_list = ['right above', 'left below', 'right below', 'left', 'right', 'below', 'below']

        for ef_index, new_type, new_location in zip(existing_face_index_list, new_type_list, new_location_list):
            board_set_up.new_face(self, self.faces[ef_index], new_type, new_location)
        
        try: 
            self.cnv_buttons.pack_forget()
        except:
            pass

        for line in self.lines:
            self.cnv_board.delete(line)

        grid_set_up.create_grid(self)
        grid_set_up.add_elements(self)

        pos_list = [(0,0), (0,5), (0,6), (1,1), (1,6), (2,0), (2,8), (3,0), (3,2), (3,7), (4,0), (4,1), (4,3), (4,5), (4,6), (4,8), (5,3), (5,7), (6,2), (6,3), (6,5), (6,7), (7,4), (7,8)]
        num_list = [1, 9, 3, 8, 2, 5, 4, 9, 1, 5, 2, 6, 1, 5, 9, 3, 6, 1, 4, 5, 8, 9, 6, 2]
        for pos, num in zip(pos_list, num_list):
            grid_set_up.set_number(self, pos, num)

        self.start_click()

    def face_click(self,event):
        board_set_up.choose_face_to_add(self,event)

    def button_click(self,event):
        board_set_up.choose_where_add(self,event)

    def line_click(self,event):
        board_set_up.add_new_face(self,event)

    def start_board_click(self):
        error_flags.reset(self)
        self.frm_example.pack_forget()
        try: 
            self.cnv_buttons.pack_forget()
        except:
            pass
        
        if len(self.faces) == 1:
            error_flags.flag(self,5)
        elif not board_set_up.check_3d_board_valid(self):
            error_flags.flag(self,6)
        else:
            grid_set_up.create_grid(self)
            grid_set_up.add_elements(self)

    def square_click(self,event):
        grid_set_up.input_number(self)

    def enter_number_click(self,event):
        grid_set_up.enter_number(self)

    def start_click(self):
        error_flags.reset(self)
        
        if legal.board_is_legal(self):
            if legal.board_follows_rules(self):
                for pos in self.grid_all_squares:
                    i, j = pos[0], pos[1]
                    self.cnv_board.itemconfigure(self.shp_square[i][j], state = tk.DISABLED)
                    self.cnv_board.itemconfigure(self.lbl_square[i][j], state = tk.DISABLED)
                    if self.grid[i][j] != 0:
                        self.cnv_board.itemconfigure(self.shp_square[i][j], fill = '#f0f0f0')
                        self.cnv_board.itemconfigure(self.lbl_square[i][j], fill = '#747578')
                    else:
                        self.cnv_board.itemconfigure(self.shp_square[i][j], fill = 'white')

                self.initial_grid = deepcopy(self.grid)
                self.btn_start.pack_forget()
                windows_set_up.window_2(self)
    
    def brute_force_click(self):
        error_flags.reset(self)

        self.frm_body_buttons.pack_forget()

        lbl_show_iterating = tk.Label(master=self.frm_controls, text="Solving via backtracking", font=('TkDefaultFont', 12))
        lbl_show_iterating.pack()
        
        if self.candidates_found == True:
            self.candidates = {pos: cand_list for pos, cand_list in sorted(self.candidates.items(), key= lambda item: len(item[1]))}
        self.squares_list = self.grid_all_squares if self.candidates_found == False else list(self.candidates.keys())
        
        if brute_force.rec_solve(self, 0):
            for pos in self.grid_all_squares:
                i, j = pos[0], pos[1]
                if self.candidates_found == True:
                    for k in range(9):
                        self.cnv_board.itemconfigure(self.lbl_cand_square[i][j][k], state = 'hidden')
                self.cnv_board.itemconfigure(self.lbl_square[i][j], text = self.grid[i][j])
            
            lbl_show_iterating.pack_forget()
            self.solved_grid = deepcopy(self.grid)
            self.lbl_sol = tk.Label(master=self.frm_controls, text="Solved", font=('TkDefaultFont', 14, 'bold'))
            self.lbl_sol.pack()

            self.btn_back_to_initial.pack()

        else:
            lbl_show_iterating.pack_forget()

            lbl_no_sol = tk.Label(master=self.frm_controls, text="No solution", font=('TkDefaultFont', 14, 'bold'))
            lbl_no_sol.pack()

    def back_to_initial_click(self):
        self.btn_back_to_initial.pack_forget()
        self.lbl_sol.pack_forget()
        self.frm_body_buttons.pack()

        self.candidates_found = False
        self.btn_candidates.configure(state='active')
        self.btn_brute_force.configure(relief='raised')

        self.grid = deepcopy(self.initial_grid)
        for pos in self.grid_all_squares:
            i, j = pos[0], pos[1]
            if self.grid[i][j] == 0:
                self.cnv_board.itemconfigure(self.lbl_square[i][j], text = '')
        self.window.update()

    def candidates_click(self):
        candidates.find_all(self)
        self.btn_candidates.configure(state='disabled')

    def apply_constr_click(self):
        error_flags.reset(self)
        if self.candidates_found == False:
            candidates.find_all(self)
            self.btn_candidates.configure(state='disabled')

        if constraints.solve_constraints(self):
            self.frm_body_buttons.pack_forget()
            self.lbl_sol = tk.Label(master=self.frm_body, text="Solved", font=('TkDefaultFont', 14, 'bold'))
            self.lbl_sol.pack()
            self.btn_back_to_initial.pack()

        else:
            error_flags.flag(self, 4)


if __name__ == "__main__":
    window = tk.Tk()
    app = SudokuSolver3D(window)
    window.mainloop() 

