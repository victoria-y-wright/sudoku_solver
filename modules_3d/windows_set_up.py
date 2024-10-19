import tkinter as tk

from modules_3d import board_set_up


def window_1(self):
    
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
        self.cnv_board = tk.Canvas(master = self.frm_board, bd =2, width = '650', height = '600', closeenough=20)

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

    set_up_board(self)

    def set_up_controls(self):
        self.frm_controls = tk.Frame(height = 500, width = 300, highlightbackground='black', highlightthickness=1)
        self.frm_controls.pack_propagate(False)
        self.frm_controls.grid(row = 1, column = 1, padx = 15)
        
        self.frm_labels = tk.Frame(master = self.frm_controls)
        self.frm_labels.pack()
        self.lbl_controls = tk.Label(master=self.frm_labels, text="← Click on a face to add its neighbour", font=('TkDefaultFont', 12), pady=10)
        self.lbl_controls.pack()
        
        self.lbl_choose_face = tk.Label(master=self.frm_labels, text="↓ Choose the type of face to add", font=('TkDefaultFont', 12), pady=5)

        self.lbl_choose_where = tk.Label(master=self.frm_labels, text="← Click on the side it should connect to", font=('TkDefaultFont', 12), pady=5)

        self.btn_start_board = tk.Button(master = self.frm_controls, text = "Start with board", font=('TkDefaultFont', 10), command = self.start_board_click)

        ## face buttons ##
        self.cnv_buttons = tk.Canvas(master= self.frm_labels, height = 80, width = 300, closeenough=10)

        self.buttons = [board_set_up.Face('top', (50,40), 50), board_set_up.Face('left', (150,40), 50), board_set_up.Face('right', (250,40), 50)]

        self.button_shapes = []
        for button in self.buttons:
            self.button_shapes.append(self.cnv_buttons.create_polygon(button.vertices, fill = 'white', outline = 'black', activeoutline='darkseagreen3'))
            self.cnv_buttons.tag_bind(self.button_shapes[-1], '<Button-1>', self.button_click)

        ## example boards ##
        self.frm_example = tk.Frame(master = self.frm_controls, pady= 20)
        self.lbl_example = tk.Label(master=self.frm_example, text="OR try an example board:", font=('TkDefaultFont', 12))
        self.lbl_example.grid(row = 0, column= 0, columnspan= 2)
        
        img_ex_1 = tk.PhotoImage(file = 'images/ex1_resized.png')
        self.btn_ex_1 = tk.Button(master=self.frm_example, image=img_ex_1)
        self.btn_ex_1.bind('<Button-1>', self.start_example_click)
        self.btn_ex_1.image = img_ex_1
        self.btn_ex_1.grid(row = 2, column= 0, padx = 10)

        img_ex_2 = tk.PhotoImage(file = 'images/ex2_resized.png')
        self.btn_ex_2 = tk.Button(master=self.frm_example, image=img_ex_2)
        self.btn_ex_2.bind('<Button-1>', self.start_example_click)
        self.btn_ex_2.image = img_ex_2
        self.btn_ex_2.grid(row = 2, column= 1, padx = 10)

        img_ex_3 = tk.PhotoImage(file = 'images/ex3_resized.png')
        self.btn_ex_3 = tk.Button(master=self.frm_example, image=img_ex_3)
        self.btn_ex_3.bind('<Button-1>', self.start_example_click)
        self.btn_ex_3.image = img_ex_3
        self.btn_ex_3.grid(row = 1, column= 0, columnspan = 2, pady = 10)

        self.frm_example.pack(side = 'bottom')
        self.btn_start_board.pack(side = 'bottom', pady = (0,5))

        ## number entry ##
        self.frm_entry = tk.Frame(master=self.frm_controls)

        self.lbl_entry_click = tk.Label(master=self.frm_controls, text="← Choose a square to input known value", font=('TkDefaultFont', 12), pady=10)

        self.lbl_entry = tk.Label(master = self.frm_entry, text='            → Type in the number: ', font = ('TkDefaultFont', 12))
        self.lbl_entry.grid(row = 0, column = 0)
        
        self.entry_text = tk.StringVar()
        self.ent_entry = tk.Entry(master=self.frm_entry, width = 3, justify= "center", textvariable= self.entry_text, font = ('TkDefaultFont', 15, 'bold'), relief = 'flat')
        self.ent_entry.grid(row = 0, column = 1)
        self.ent_entry.bind('<Return>', self.enter_number_click)
        
        self.btn_start = tk.Button(master = self.frm_controls, text = "Start", font = ('TkDefaultFont', 10), command = self.start_click)
    set_up_controls(self)


def window_2(self):
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
