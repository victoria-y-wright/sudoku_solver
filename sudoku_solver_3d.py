import tkinter as tk
from copy import deepcopy

from modules_3d import windows_set_up, examples, board_set_up, grid_set_up, error_flags, legal, brute_force, candidates, constraints


class SudokuSolver3D:
    def __init__(self, window):
        self.window = window
        self.window.title("3D Sudoku Solver")
        self.window.geometry("1050x650")

        windows_set_up.window_1(self)
        error_flags.set_up(self)
        self.candidates_found = False
        self.grid_all_squares = []


    def start_example_click(self, event):
        if event.widget == self.btn_ex_1:
            examples.start(self,1)
        elif event.widget == self.btn_ex_2:
            examples.start(self,2)
        elif event.widget == self.btn_ex_3:
            examples.start(self,3)
            
    def face_click(self,event):
        board_set_up.choose_face_to_add(self,event)

    def button_click(self,event):
        board_set_up.choose_where_add(self,event)

    def line_click(self,event):
        board_set_up.add_new_face(self,event)

    def start_board_click(self):
        error_flags.reset(self)
        
        if len(self.faces) == 1:
            error_flags.flag(self,5)
        elif not board_set_up.check_3d_board_valid(self):
            error_flags.flag(self,6)
        else:
            self.frm_example.pack_forget()
            self.frm_labels.pack_forget()
            grid_set_up.create_grid(self)
            grid_set_up.add_elements(self)

            ## resize canvas
            region = self.cnv_board.bbox("all")
            self.cnv_board.configure(width = region[2]-region[0]+30, height=region[3]-region[1])
            self.window.maxsize(region[2]-region[0]+420, 650)

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
                self.lbl_entry_click.pack_forget()
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

