import tkinter as tk

from modules.gui import squares_3d

def create(self):
    top_widgets(self)
    board_widgets(self)
    window_1_widgets(self)
    window_2_widgets(self)
    window_3_widgets(self)
    solved_widgets(self)

def top_widgets(self):
    self.frm_main = tk.Frame()
    self.frm_top = tk.Frame(master=self.frm_main, height=60, width=400)
    self.frm_top.pack_propagate(False)
    self.frm_top.pack()

    self.lbl_title = tk.Label(master=self.frm_top, text='3D Sudoku Solver', font = ('TkDefaultFont', 15))
    self.lbl_title.pack(side='top')


def board_widgets(self):
    self.frm_board = tk.Frame(master=self.frm_main)

    self.x_offset, self.y_offset = 0, 0
    self.cnv_board = tk.Canvas(master = self.frm_board, bd =2, width = '650', height = '600', closeenough=20)

    self.faces = []
    self.shp_face = []
    self.lines = [[] for x in range(4)] 
    self.side_length = 120

    # starting face
    self.faces.append(squares_3d.Face('top', (300,150), self.side_length))

    self.shp_face.append(self.cnv_board.create_polygon(self.faces[0].vertices, fill = 'white', outline = 'black', activefill='honeydew1'))
    self.cnv_board.tag_bind(self.shp_face[-1], '<Button-1>', self.choose_face_to_add)
    self.cnv_board.pack()

    self.frm_board.pack()


def window_1_widgets(self):
    self.frm_controls = tk.Frame(height = 500, width = 300, highlightbackground='black', highlightthickness=1)
    self.frm_controls.pack_propagate(False)

    # board creation widgets
    self.frm_labels = tk.Frame(master = self.frm_controls)
    self.frm_labels.pack()

    self.lbl_controls = tk.Label(master=self.frm_labels, text="← Click on a face to add its neighbour", font=('TkDefaultFont', 12), pady=10)
    self.lbl_controls.pack()
    self.lbl_choose_face = tk.Label(master=self.frm_labels, text="↓ Choose the type of face to add", font=('TkDefaultFont', 12), pady=5)
    self.lbl_choose_where = tk.Label(master=self.frm_labels, text="← Click on the side it should connect to", font=('TkDefaultFont', 12), pady=5)

    self.cnv_buttons = tk.Canvas(master= self.frm_labels, height = 80, width = 300, closeenough=10)
    self.buttons = [squares_3d.Face('top', (50,40), 50), squares_3d.Face('left', (150,40), 50), squares_3d.Face('right', (250,40), 50)]
    self.button_shapes = []
    for button in self.buttons:
        self.button_shapes.append(self.cnv_buttons.create_polygon(button.vertices, fill = 'white', outline = 'black', activeoutline='darkseagreen3'))
        self.cnv_buttons.tag_bind(self.button_shapes[-1], '<Button-1>', self.choose_where_add)

    self.btn_start_board = tk.Button(master = self.frm_controls, text = "Start with board", font=('TkDefaultFont', 10), command = self.board_created)
    self.btn_start_board.pack(side = 'bottom', pady = (0,5))
    
    # number entry widgets
    self.frm_entry = tk.Frame(master=self.frm_controls)

    self.lbl_entry_click = tk.Label(master=self.frm_controls, text="← Choose a square to input known value", font=('TkDefaultFont', 12), pady=10)
    self.lbl_entry = tk.Label(master = self.frm_entry, text='            → Type in the number: ', font = ('TkDefaultFont', 12))
    self.lbl_entry.grid(row = 0, column = 0)

    self.entry_text = tk.StringVar()
    self.ent_entry = tk.Entry(master=self.frm_entry, width = 3, justify= "center", textvariable= self.entry_text, font = ('TkDefaultFont', 15, 'bold'), relief = 'flat')
    self.ent_entry.grid(row = 0, column = 1)
    self.ent_entry.bind('<Return>', self.enter_number)

    self.btn_start = tk.Button(master = self.frm_controls, text = "Start", font = ('TkDefaultFont', 10), command = self.puzzle_entered)

    # example puzzle widgets
    self.frm_example = tk.Frame(master = self.frm_controls, pady= 20)

    self.lbl_example = tk.Label(master=self.frm_example, text="OR try an example board:", font=('TkDefaultFont', 12))
    self.lbl_example.grid(row = 0, column= 0, columnspan= 2)

    img_ex_1 = tk.PhotoImage(file = 'images/ex1_resized.png')
    self.btn_ex_1 = tk.Button(master=self.frm_example, image=img_ex_1)
    self.btn_ex_1.bind('<Button-1>', self.example_puzzle)
    self.btn_ex_1.image = img_ex_1
    self.btn_ex_1.grid(row = 2, column= 0, padx = 10)

    img_ex_2 = tk.PhotoImage(file = 'images/ex2_resized.png')
    self.btn_ex_2 = tk.Button(master=self.frm_example, image=img_ex_2)
    self.btn_ex_2.bind('<Button-1>', self.example_puzzle)
    self.btn_ex_2.image = img_ex_2
    self.btn_ex_2.grid(row = 2, column= 1, padx = 10)

    img_ex_3 = tk.PhotoImage(file = 'images/ex3_resized.png')
    self.btn_ex_3 = tk.Button(master=self.frm_example, image=img_ex_3)
    self.btn_ex_3.bind('<Button-1>', self.example_puzzle)
    self.btn_ex_3.image = img_ex_3
    self.btn_ex_3.grid(row = 1, column= 0, columnspan = 2, pady = 10)

    self.frm_example.pack(side = 'bottom')


def window_2_widgets(self):
    self.frm_body_buttons = tk.Frame(height = 500, width = 300, highlightbackground='black', highlightthickness=1)
    self.frm_body_buttons.pack_propagate(False)

    # candidates
    self.btn_candidates = tk.Button(master=self.frm_body_buttons, text="Find candidates", font=('TkDefaultFont', 10), command = self.find_candidates)    
    self.btn_candidates.pack(pady=20)

    # brute force
    self.btn_brute_force = tk.Button(master=self.frm_body_buttons, text="Solve with brute force", font=('TkDefaultFont', 10), command = self.solve_with_brute_force)
    self.btn_brute_force.pack(pady=(20,0))

    self.var_show_iterating = tk.IntVar()
    self.chk_show_iterating = tk.Checkbutton(master = self.frm_body_buttons, text = "show backtracking", variable = self.var_show_iterating, onvalue = 1, offvalue = 0)
    self.chk_show_iterating.select()
    self.chk_show_iterating.pack(pady=(0,20))

    # constraints    
    self.frm_constr = tk.Frame(master = self.frm_body_buttons)

    self.btn_solve_with_constr = tk.Button(master=self.frm_constr, text="Solve with constraints", font=('TkDefaultFont', 10), command = self.solve_by_applying_constraints)
    self.btn_solve_with_constr.grid(row = 0, column = 0, columnspan= 2)

    self.var_step_by_step = tk.IntVar()
    self.chk_step_by_step = tk.Checkbutton(master = self.frm_constr, text = "step by step", variable = self.var_step_by_step, onvalue = 1, offvalue = 0)
    self.chk_step_by_step.grid(row = 1, column = 0, columnspan= 2, pady = (0, 5))

    constr_text_list = ["sole candidates", "hidden singles", "naked pairs", "naked triples", "hidden pairs", "hidden triples", "intersection removal", "3d intersection removal"]
    constr_colour_list = ['darkolivegreen1', 'darkslategray1', 'orchid1', 'tan1', '#a8b7ff', '#b996ff', '#ffd811', 'palevioletred1']
    constr_grid_list = [(2,0), (2,1), (3,0), (3,1), (4,0), (4,1), (5,0), (6,0)]

    self.frm_constr_list = []
    self.chk_constr_list = []
    self.var_constr_list = [tk.IntVar() for constr_text in constr_text_list]

    for i in range(len(constr_text_list)):
        self.frm_constr_list.append(tk.Frame(master = self.frm_constr, highlightthickness=3, highlightbackground = constr_colour_list[i]))
        self.chk_constr_list.append(tk.Checkbutton(master = self.frm_constr_list[i], text = constr_text_list[i], variable = self.var_constr_list[i], onvalue = 1, offvalue = 0, bd = -2))
        self.chk_constr_list[i].pack(fill='both')
        if i in range(6):
            self.frm_constr_list[i].grid(row = constr_grid_list[i][0], column = constr_grid_list[i][1], padx = 10, pady = 10, sticky='EW')
        else:
            self.frm_constr_list[i].grid(row = constr_grid_list[i][0], column = constr_grid_list[i][1], padx = 10, pady = 10, columnspan = 2)

    self.frm_constr.columnconfigure(list(range(2)), weight = 1)

    self.chk_constr_list[0].select()
    self.chk_constr_list[0].configure(state = 'disabled', disabledforeground= 'black')

    self.frm_constr.pack(pady=20, fill='x')

def window_3_widgets(self):
    self.frm_iterating = tk.Frame(height = 500, width = 300, highlightbackground='black', highlightthickness=1)
    self.frm_iterating.pack_propagate(False)

    lbl_show_iterating = tk.Label(master=self.frm_iterating, text="Solving via backtracking", font=('TkDefaultFont', 12))
    lbl_show_iterating.pack(pady=20)

    self.var_speed_up = tk.IntVar()
    self.chk_speed_up = tk.Checkbutton(master = self.frm_iterating, text = 'Speed up?', font=('TkDefaultFont', 10), variable = self.var_speed_up, onvalue = 1, offvalue = 0)
    self.chk_speed_up.pack()

def solved_widgets(self):
    self.frm_solved = tk.Frame(height = 500, width = 300, highlightbackground='black', highlightthickness=1)
    self.frm_solved.pack_propagate(False)

    self.lbl_sol = tk.Label(master=self.frm_solved, text="Solved", font=('TkDefaultFont', 14, 'bold'))
    self.lbl_sol.pack(pady=20)
    self.btn_back_to_initial = tk.Button(master=self.frm_solved, text="Back", font=('TkDefaultFont', 10), command = self.back_to_initial)
    self.btn_back_to_initial.pack(pady=25)

def no_solution_widgets(self):
    self.frm_no_sol = tk.Frame(height = 500, width = 300, highlightbackground='black', highlightthickness=1)
    self.frm_no_sol.pack_propagate(False)

    self.lbl_no_sol = tk.Label(master=self.frm_no_sol, text="No solution", font=('TkDefaultFont', 14, 'bold'))
    self.lbl_no_sol.pack()

