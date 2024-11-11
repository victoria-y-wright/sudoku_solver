import tkinter as tk    

def create(self):
    top_widgets(self)
    board_widgets(self)
    window_1_widgets(self)
    window_2_widgets(self)
    window_3_widgets(self)
    solved_widgets(self)
    no_solution_widgets(self)


def top_widgets(self):
    self.frm_top = tk.Frame()
    lbl_title = tk.Label(master=self.frm_top, text='Sudoku Solver', font = ('TkDefaultFont', 15))
    lbl_title.pack()


def board_widgets(self):
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
            self.frm_square[i][j] = tk.Frame(master=self.frm_board, relief = 'sunken', bd = 1, bg = 'white', height = 43, width = 43)
            self.frm_square[i][j].pack_propagate(False)

            if i in [2,5] and j in [2,5]:
                self.frm_square[i][j].grid(row=i,column=j,padx=(0,1),pady=(0,1),sticky = 'nsew')
            elif i in [2,5]:
                self.frm_square[i][j].grid(row=i,column=j,pady=(0,1), sticky = 'nsew')
            elif j in [2,5]:
                self.frm_square[i][j].grid(row=i,column=j,padx=(0,1), sticky = 'nsew')
            else:
                self.frm_square[i][j].grid(row=i,column=j, sticky = 'nsew')
            
            self.ent_number[i][j] = tk.Entry(master=self.frm_square[i][j], width = 3, justify= "center", textvariable= self.entry_text[i][j], font = ('TkDefaultFont', 27, 'bold'), relief = 'flat')
            self.ent_number[i][j].pack()

            for key in ['<Left>', '<Right>', '<Up>', '<Down>']:
                self.ent_number[i][j].bind_class('Entry', key, keybinding)


def window_1_widgets(self):
    # type entry controls
    self.frm_controls = tk.Frame(pady = 0)

    self.btn_start = tk.Button(master=self.frm_controls, text="Start", font=('TkDefaultFont', 10))
    self.btn_start.pack()
    self.btn_start.bind("<Button-1>", self.puzzle_entered)

    # paste entry controls
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
    self.btn_start_paste.pack(pady=5)
    self.btn_start_paste.bind("<Button-1>", self.puzzle_entered)

def window_2_widgets(self):
    self.frm_body_buttons = tk.Frame(pady = 0)
    
    # candidates
    self.btn_candidates = tk.Button(master=self.frm_body_buttons, text="Find candidates", font=('TkDefaultFont', 10), command = self.find_candidates)    
    self.btn_candidates.grid(row = 0, column = 0, padx = (0,70))
    
    # brute force
    self.btn_brute_force = tk.Button(master=self.frm_body_buttons, text="Solve with brute force", font=('TkDefaultFont', 10), command = self.solve_with_brute_force)
    self.btn_brute_force.grid(row = 0, column = 1, padx = (60,0))

    self.var_show_iterating = tk.IntVar()
    self.chk_show_iterating = tk.Checkbutton(master = self.frm_body_buttons, text = "show backtracking", variable = self.var_show_iterating, onvalue = 1, offvalue = 0)
    self.chk_show_iterating.select()
    self.chk_show_iterating.grid(row = 1, column = 1, padx = (60,0))

    # constraints
    self.frm_constr = tk.Frame(master = self.frm_body_buttons)

    self.btn_apply_constr = tk.Button(master=self.frm_constr, text="Apply constraints", font=('TkDefaultFont', 10), command = self.solve_by_applying_constraints)
    self.btn_apply_constr.grid(row = 0, column = 0, columnspan= 3)

    self.var_step_by_step = tk.IntVar()
    self.chk_step_by_step = tk.Checkbutton(master = self.frm_constr, text = "step-by-step", variable = self.var_step_by_step, onvalue = 1, offvalue = 0)
    self.chk_step_by_step.grid(row = 1, column = 0, columnspan= 3, pady = (0, 5))

    constr_text_list = ["sole candidates", "hidden singles", "naked pairs", "naked triples", "hidden pairs", "hidden triples"]
    constr_colour_list = ['darkolivegreen1', 'darkslategray1', 'orchid1', 'tan1', 'palevioletred1', 'mediumpurple1']
    constr_grid_list = [(2,0), (3,0), (2,1), (3,1), (2,2), (3,2)]

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

    self.frm_constr.grid(row = 2, column = 0, columnspan=2, pady = (10))

def window_3_widgets(self):
    self.frm_iterating = tk.Frame(pady=25)

    self.var_speed_up = tk.IntVar()
    self.chk_speed_up = tk.Checkbutton(master = self.frm_iterating, text = 'Speed up?', font=('TkDefaultFont', 10), variable = self.var_speed_up, onvalue = 1, offvalue = 0)
    self.chk_speed_up.pack(pady=(0,50))

    lbl_show_iterating = tk.Label(master=self.frm_iterating, text="Solving via backtracking", font=('TkDefaultFont', 12))
    lbl_show_iterating.pack(pady=25)
        
def solved_widgets(self):
    self.frm_solved = tk.Frame()

    self.lbl_sol = tk.Label(master=self.frm_solved, text="Solved", font=('TkDefaultFont', 14, 'bold'))
    self.lbl_sol.pack(pady=(0,30))

    self.btn_back_to_initial = tk.Button(master=self.frm_solved, text="Back", font=('TkDefaultFont', 8), command = self.back_to_initial)
    self.btn_back_to_initial.pack(pady=25)

def no_solution_widgets(self):
    self.frm_no_sol = tk.Frame()

    self.lbl_no_sol = tk.Label(master=self.frm_no_sol, text="No solution", font=('TkDefaultFont', 14, 'bold'))
    self.lbl_no_sol.pack()