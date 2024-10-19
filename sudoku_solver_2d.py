import tkinter as tk
from copy import deepcopy

from modules_2d import error_flags, legal, brute_force, constraints, candidates


class SudokuSolver:
    def __init__(self, window):
        self.window = window
        self.window.title("Sudoku Solver")
        self.window.geometry("450x600")
        self.grid = [[None]*9 for x in range(9)]

        self.set_up_window_1()
        self.grid_locations()
        error_flags.set_up(self)
        self.candidates_found = False

### grid coords ###
    def grid_locations(self):
        self.grid_all_squares = []
        self.grid_rows = []
        self.grid_cols = []
        for i in range(9):
            new_row = set()
            new_col = set()
            for j in range(9):
                new_row.add((i,j))
                new_col.add((j,i))
                self.grid_all_squares.append((i,j))
            self.grid_rows.append(new_row)
            self.grid_cols.append(new_col)

        self.grid_boxes = []
        for box_row in [0,3,6]:
            for box_col in [0,3,6]:
                new_box = set()
                for i in range(3):
                    for j in range(3):
                        new_box.add((box_row+i,box_col+j))
                self.grid_boxes.append(new_box)

### window 1 ###        
    def set_up_window_1(self):
        
        def set_up_top(self):
            self.frm_top = tk.Frame(pady = 5)
            lbl_title = tk.Label(master=self.frm_top, text='Sudoku Solver', font = ('TkDefaultFont', 15))
            lbl_title.pack()
            self.frm_top.pack()
        set_up_top(self)
        
        def set_up_board(self):
            self.frm_board = tk.Frame(bg='black',padx=1,pady=1)

            # keybinding arrows to movement in board
            def keybinding(event):
                entry = event.widget
                if event.keysym in ('Up', 'Down'):
                    info = entry.master.grid_info()
                    if event.keysym == 'Up':
                        row = (info['row'] if info['row'] > 0 else 9) - 1
                    else:
                        row = (info['row'] + 1) % 9
                    self.ent_number[row][info['column']].focus()
                elif event.keysym == 'Left':
                    entry.tk_focusPrev().focus()
                elif event.keysym == 'Right':
                    entry.tk_focusNext().focus()
                return "break"

            # creating sudoku board
            self.frm_square=[[None]*9 for x in range(9)]
            self.ent_number=[[None]*9 for x in range(9)]
            self.entry_text=[[tk.StringVar() for x in range(9)]  for y in range(9)]
            for i in range(9):
                for j in range(9):
                    self.frm_square[i][j] = tk.Frame(master=self.frm_board, relief = 'sunken', bd = 1, bg = 'white', height = 40, width = 40)
                    self.frm_square[i][j].pack_propagate(False)

                    if i in [2,5] and j in [2,5]:
                        self.frm_square[i][j].grid(row=i,column=j,padx=(0,1),pady=(0,1),sticky = 'nsew')
                    elif i in [2,5]:
                        self.frm_square[i][j].grid(row=i,column=j,pady=(0,1), sticky = 'nsew')
                    elif j in [2,5]:
                        self.frm_square[i][j].grid(row=i,column=j,padx=(0,1), sticky = 'nsew')
                    else:
                        self.frm_square[i][j].grid(row=i,column=j, sticky = 'nsew')
                    
                    self.ent_number[i][j] = tk.Entry(master=self.frm_square[i][j], width = 3, justify= "center", textvariable= self.entry_text[i][j], font = ('TkDefaultFont', 25, 'bold'), relief = 'flat')
                    self.ent_number[i][j].pack()

                    for key in ['<Left>', '<Right>', '<Up>', '<Down>']:
                        self.ent_number[i][j].bind_class('Entry', key, keybinding)
                    self.frm_board.pack(fill="none", expand=True)
            
            self.frm_board.pack()
        set_up_board(self)

        def set_up_body(self):
            self.frm_body = tk.Frame(pady = 5)

            self.frm_body_buttons = tk.Frame(pady = 0)
            self.btn_start = tk.Button(master=self.frm_body_buttons, text="Start", font=('TkDefaultFont', 10))
            self.btn_start.pack()
            self.btn_start.bind("<Button-1>", self.start_click)

            self.frm_body_buttons.pack()
            self.frm_body.pack()
        set_up_body(self)

        def set_up_bot(self):
            self.frm_bot = tk.Frame(pady = 5)

            self.lbl_start_paste = tk.Label(master=self.frm_bot, text="OR paste in a puzzle as a string of numbers:", font=('TkDefaultFont', 10))
            self.lbl_start_paste.pack()

            self.ent_start_paste = tk.Entry(master = self.frm_bot, width = 50)
            self.ent_start_paste.pack()

            self.lbl_start_paste_ex = tk.Text(master=self.frm_bot, font=('TkDefaultFont', 8), height = 2, width = 45, relief = 'flat', bg = '#F0F0F0')
            self.lbl_start_paste_ex.insert(1.0, "e.g. 720096003000205000080004020000000060106503807040000000030800090000702000200430018")
            self.lbl_start_paste_ex.pack()
            self.lbl_start_paste_ex.configure(state='disabled')

            self.btn_start_paste = tk.Button(master=self.frm_bot, text="Start from paste", font=('TkDefaultFont', 10))
            self.btn_start_paste.pack()
            self.btn_start_paste.bind("<Button-1>", self.start_click)

            self.frm_bot.pack()
        set_up_bot(self)

### start ###
    def start_click(self,event):
        error_flags.reset(self)
        
        board_legal = False
        if event.widget == self.btn_start: #start button
            if legal.board_is_legal(self):
                board_legal = True
                for i in range(9):
                    for j in range(9):
                        if len(self.ent_number[i][j].get()) != 0:
                                self.grid[i][j]=int(self.ent_number[i][j].get())
                        else:
                            self.grid[i][j] = 0
        elif event.widget == self.btn_start_paste: #paste start button
            paste_list = self.ent_start_paste.get().strip()
            if paste_list.isdigit() and len(paste_list) == 81:
                board_legal = True
                for i in range(9):
                    for j in range(9):
                        self.grid[i][j] = int(paste_list[i*9+j])
                        if self.grid[i][j] != 0:
                            self.entry_text[i][j].set(self.grid[i][j])
                        else:
                            self.entry_text[i][j].set('')
            else:
                error_flags.flag(self, 3)
    
        if board_legal == True:
            if legal.board_follows_rules(self):
                    for i in range(9):
                        for j in range(9):
                            if self.grid[i][j] != 0:
                                    self.ent_number[i][j].config(state=tk.DISABLED)
                            else:
                                self.entry_text[i][j].set('')
                    self.initial_grid = deepcopy(self.grid)
                    
                    self.btn_start.pack_forget()
                    self.btn_start_paste.pack_forget()
                    self.frm_bot.pack_forget()
                    self.set_up_window_2()

### window 2 ###
    def set_up_window_2(self):

        self.btn_brute_force = tk.Button(master=self.frm_body_buttons, text="Solve with brute force", font=('TkDefaultFont', 10), command = self.brute_force_click)

        self.var_show_iterating = tk.IntVar()
        self.chk_show_iterating = tk.Checkbutton(master = self.frm_body_buttons, text = "show backtracking", variable = self.var_show_iterating, onvalue = 1, offvalue = 0)
        self.chk_show_iterating.select()

        self.btn_back_to_initial = tk.Button(master=self.frm_body, text="Back", font=('TkDefaultFont', 8), command = self.back_to_initial_click)

        self.btn_candidates = tk.Button(master=self.frm_body_buttons, text="Find candidates", font=('TkDefaultFont', 10), command = self.candidates_click)    
        
        self.frm_constr = tk.Frame(master = self.frm_body_buttons)

        self.btn_apply_constr = tk.Button(master=self.frm_constr, text="Apply constraints", font=('TkDefaultFont', 10), command = self.apply_constr_click)
        self.btn_apply_constr.grid(row = 0, column = 0, columnspan= 3, pady = (0, 5))

        constr_text_list = ["sole candidates", "hidden singles", "naked pairs", "naked triples", "hidden pairs", "hidden triples"]
        constr_colour_list = ['darkolivegreen1', 'darkslategray1', 'orchid1', 'tan1', 'palevioletred1', 'mediumpurple1']
        constr_grid_list = [(1,0), (2,0), (1,1), (2,1), (1,2), (2,2)]

        self.frm_constr_list = []
        self.chk_constr_list = []
        self.var_constr_list = [tk.IntVar() for constr_text in constr_text_list]

        for i in range(len(constr_text_list)):
            self.frm_constr_list.append(tk.Frame(master = self.frm_constr, highlightthickness=3, highlightbackground = constr_colour_list[i]))
            self.chk_constr_list.append(tk.Checkbutton(master = self.frm_constr_list[i], text = constr_text_list[i], variable = self.var_constr_list[i], onvalue = 1, offvalue = 0, bd = -2))
            self.chk_constr_list[i].pack()
            self.frm_constr_list[i].grid(row = constr_grid_list[i][0], column = constr_grid_list[i][1], padx = 10, pady = 5)

        self.chk_constr_list[0].select()
        self.chk_constr_list[0].configure(state = 'disabled', disabledforeground= 'black')

        self.btn_candidates.grid(row = 0, column = 0, padx = (0,70))
        self.btn_brute_force.grid(row = 0, column = 1, padx = (60,0))
        self.chk_show_iterating.grid(row = 1, column = 1, padx = (60,0))
        self.frm_constr.grid(row = 2, column = 0, columnspan=2, pady = (20,10))

### brute force ###
    def brute_force_click(self):
        error_flags.reset(self)

        self.frm_body_buttons.pack_forget()
        self.frm_body.pack()

        lbl_show_iterating = tk.Label(master=self.frm_body, text="Solving via backtracking", font=('TkDefaultFont', 12))
        lbl_show_iterating.pack()
        
        if self.candidates_found == True:
            self.candidates = {pos: cand_list for pos, cand_list in sorted(self.candidates.items(), key= lambda item: len(item[1]))}
        self.squares_list = self.grid_all_squares if self.candidates_found == False else list(self.candidates.keys())
        
        if brute_force.rec_solve(self, 0):
            for i in range(9):
                for j in range(9):
                    if self.candidates_found == True:
                        self.frm_cand_square[i][j].pack_forget()
                        self.ent_number[i][j].pack()
                    self.entry_text[i][j].set(self.grid[i][j])
            
            lbl_show_iterating.pack_forget()
            self.solved_grid = deepcopy(self.grid)
            self.lbl_sol = tk.Label(master=self.frm_body, text="Solved", font=('TkDefaultFont', 14, 'bold'))
            self.lbl_sol.pack()

            self.btn_back_to_initial.pack()

        else:
            lbl_show_iterating.pack_forget()

            lbl_no_sol = tk.Label(master=self.frm_body, text="No solution", font=('TkDefaultFont', 14, 'bold'))
            lbl_no_sol.pack()

    def back_to_initial_click(self):
        self.btn_back_to_initial.pack_forget()
        self.lbl_sol.pack_forget()
        self.frm_body.pack_forget()
        self.frm_body_buttons.pack()

        self.candidates_found = False
        self.btn_candidates.configure(state='active')
        self.btn_brute_force.configure(relief='raised')

        self.grid = deepcopy(self.initial_grid)
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    self.entry_text[i][j].set('')
        self.window.update()

### constraints ###
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
    app = SudokuSolver(window)
    window.mainloop() 