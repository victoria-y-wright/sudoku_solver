import os
os.chdir("3D Sudoku Solver")


import tkinter as tk
from copy import deepcopy

from modules import board_set_up
from modules import grid_set_up
from modules import error_flags
from modules import board_input
from modules import brute_force
from modules import candidates
from modules import constraints


class SudokuSolver3D:
    def __init__(self, window):
        self.window = window
        self.window.title("3D Sudoku Solver")
        self.window.geometry("1000x600")

        self.set_up_window_1()
        error_flags.set_up(self)
        self.candidates_found = False


### window 1 ###        
    def set_up_window_1(self):
        
        def set_up_top(self):
            self.frm_top = tk.Frame(pady = 5)
            lbl_title = tk.Label(master=self.frm_top, text='3D Sudoku Solver', font = ('TkDefaultFont', 15))
            lbl_title.pack()
            self.frm_top.grid(row = 0, column= 0, columnspan= 2)
        set_up_top(self)

        def set_up_board(self):
            # creating sudoku board
            self.frm_board = tk.Frame()

            self.x_offset = 0
            self.y_offset = 0
            self.cnv_board = tk.Canvas(master = self.frm_board, bd =2, width = '600', height = '500')

            self.side_length = 120

            self.faces = []
            self.shp_face = []
            self.lines = [[] for x in range(4)] 

            # starting face
            self.faces.append(board_set_up.Face('top', (300,150), self.side_length))

            self.shp_face.append(self.cnv_board.create_polygon(self.faces[0].vertices, fill = 'white', outline = 'black', activefill='honeydew1'))
            self.cnv_board.tag_bind(self.shp_face[-1], '<Button-1>', self.face_click)


            self.cnv_board.pack()
            self.frm_board.grid(row = 1, column= 0, padx = 15, pady = 5)

            self.btn_start_board = tk.Button(master = self.frm_board, text = "Start with board", font=('TkDefaultFont', 10), command = self.start_board_click)
            self.btn_start_board.pack()

        set_up_board(self)

        def set_up_controls(self):
            self.frm_controls = tk.Frame(height = 500, width = 300, highlightbackground='black', highlightthickness=1)
            self.frm_controls.pack_propagate(False)

            self.cnv_buttons = tk.Canvas(master= self.frm_controls, height = 200, width = 300)

            self.buttons = [board_set_up.Face('top', (50,140), 50), board_set_up.Face('left', (150,140), 50), board_set_up.Face('right', (250,140), 50)]

            self.button_shapes = []
            for button in self.buttons:
                self.button_shapes.append(self.cnv_buttons.create_polygon(button.vertices, fill = 'white', outline = 'black', activeoutline='darkseagreen3'))
                self.cnv_buttons.tag_bind(self.button_shapes[-1], '<Button-1>', self.button_click)

            self.frm_controls.grid(row = 1, column = 1, padx = 15)
            
            self.frm_example = tk.Frame(master = self.frm_controls)
            self.lbl_start_example = tk.Label(master=self.frm_example, text="OR try the example:", font=('TkDefaultFont', 10))
            self.lbl_start_example.pack()

            self.btn_start_example = tk.Button(master=self.frm_example, text="Start example", font=('TkDefaultFont', 10), command = self.start_example_click)
            self.btn_start_example.pack()
            self.frm_example.pack()

            self.btn_start = tk.Button(master = self.frm_board, text = "Start", font = ('TkDefaultFont', 10), command = self.start_click)

        set_up_controls(self)

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

        self.start_click(0)

    def face_click(self,event):
        board_set_up.choose_face_to_add(self,event)

    def button_click(self,event):
        board_set_up.choose_where_add(self,event)

    def line_click(self,event):
        board_set_up.add_new_face(self,event)

    def start_board_click(self):

        self.frm_example.pack_forget()

        try: 
            self.cnv_buttons.pack_forget()
        except:
            pass

        error_flags.reset(self)
        
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

    def start_click(self,event):
        error_flags.reset(self)
        
        if board_input.is_legal(self):
            if board_input.follows_rules(self):
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
                self.set_up_window_2()
    
    def set_up_window_2(self):
        try: 
            self.frm_entry.pack_forget()
        except:
            pass

        self.frm_body_buttons = tk.Frame(master=self.frm_controls)

        self.btn_brute_force = tk.Button(master=self.frm_body_buttons, text="Solve with brute force", font=('TkDefaultFont', 10),  command = self.brute_force_click)

        self.var_show_iterating = tk.IntVar()
        self.chk_show_iterating = tk.Checkbutton(master = self.frm_body_buttons, text = "show backtracking", variable = self.var_show_iterating, onvalue = 1, offvalue = 0)
        self.chk_show_iterating.select()

        self.btn_back_to_initial = tk.Button(master=self.frm_controls, text="Back", font=('TkDefaultFont', 8), command = self.back_to_initial_click)

        self.btn_candidates = tk.Button(master=self.frm_body_buttons, text="Find candidates", font=('TkDefaultFont', 10), command = self.candidates_click)
        
        self.frm_constr = tk.Frame(master = self.frm_body_buttons)

        self.btn_apply_constr = tk.Button(master=self.frm_constr, text="Apply constraints", font=('TkDefaultFont', 10), command = self.apply_constr_click)
        self.btn_apply_constr.grid(row = 0, column = 0, columnspan= 2, pady = (0, 5))

        constr_text_list = ["sole candidates", "hidden singles", "naked pairs", "naked triples", "hidden pairs", "hidden triples"]
        constr_colour_list = ['darkolivegreen1', 'darkslategray1', 'orchid1', 'tan1', 'palevioletred1', 'mediumpurple1']
        constr_grid_list = [(1,0), (1,1), (2,0), (2,1), (3,0), (3,1)]

        self.frm_constr_list = []
        self.chk_constr_list = []
        self.var_constr_list = [tk.IntVar() for constr_text in constr_text_list]

        for i in range(len(constr_text_list)):
            self.frm_constr_list.append(tk.Frame(master = self.frm_constr, highlightthickness=3, highlightbackground = constr_colour_list[i]))
            self.chk_constr_list.append(tk.Checkbutton(master = self.frm_constr_list[i], text = constr_text_list[i], variable = self.var_constr_list[i], onvalue = 1, offvalue = 0, bd = -2))
            self.chk_constr_list[i].pack()
            self.frm_constr_list[i].grid(row = constr_grid_list[i][0], column = constr_grid_list[i][1], padx = 10, pady = 15, sticky='EW')

        self.chk_constr_list[0].select()
        self.chk_constr_list[0].configure(state = 'disabled', disabledforeground= 'black')

        self.btn_candidates.grid(row = 0, column = 0, pady = (50,0), padx = 15, sticky = 'W')
        self.btn_brute_force.grid(row = 0, column = 1, pady = (50,0),  padx = 15, sticky = 'E')
        self.chk_show_iterating.grid(row = 1, column = 1)
        self.frm_constr.grid(row = 2, column = 0, columnspan=2, pady = (50,10), padx = 20, sticky = 'EW')

        self.frm_body_buttons.pack()

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

