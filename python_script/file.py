import tkinter as tk
from copy import deepcopy
from collections import defaultdict
from itertools import combinations

class SudokuSolver:
    def __init__(self, window):
        self.window = window
        self.window.title("Sudoku Solver")
        self.window.geometry("450x600")
        self.grid = [[None]*9 for x in range(9)]

        self.set_up_window_1()
        self.grid_locations()
        self.set_up_err_flags()
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
            self.lbl_start_paste_ex.insert(1.0, "e.g. 306508400520000000087000031003010080900863005050090600130000250000000074005206300")
            self.lbl_start_paste_ex.pack()
            self.lbl_start_paste_ex.configure(state='disabled')

            self.btn_start_paste = tk.Button(master=self.frm_bot, text="Start from paste", font=('TkDefaultFont', 10))
            self.btn_start_paste.pack()
            self.btn_start_paste.bind("<Button-1>", self.start_click)

            self.frm_bot.pack()
        set_up_bot(self)
      
### err_flags ###
    def set_up_err_flags(self):
        err_flags_text = ["Only digits 1-9 are valid inputs", 
                            "Enter starting digits in the grid", 
                            "Numbers can't repeat in the same row, column or square", 
                            "Paste a list of 81 digits 1-9 (blank space= 0)",
                            "Try adding another strategy to solve"]
        self.err_flags = [False for i in range(len(err_flags_text))]
        self.lbl_err_flags = []
        for i in range(len(err_flags_text)):
            self.lbl_err_flags.append(tk.Label(master=self.frm_top, text=err_flags_text[i], bg = 'pink', font=('TkDefaultFont', 12), width=60, justify = "center"))
    
    def err_flag_reset(self):
        for i in range(len(self.err_flags)):
            if self.err_flags[i] == True:
                self.lbl_err_flags[i].pack_forget()

    def err_flag(self,index):
        self.lbl_err_flags[index].pack()
        self.err_flags[index] = True 

### start ###
    def start_click(self,event):
        self.err_flag_reset()
        
        legal = False
        if event.widget == self.btn_start: #start button
            if self.board_input_legal():
                legal = True
                for i in range(9):
                    for j in range(9):
                        if len(self.ent_number[i][j].get()) != 0:
                                self.grid[i][j]=int(self.ent_number[i][j].get())
                        else:
                            self.grid[i][j] = 0
        elif event.widget == self.btn_start_paste: #paste start button
            paste_list = self.ent_start_paste.get().strip()
            if paste_list.isdigit() and len(paste_list) == 81:
                legal = True
                for i in range(9):
                    for j in range(9):
                        self.grid[i][j] = int(paste_list[i*9+j])
                        if self.grid[i][j] != 0:
                            self.entry_text[i][j].set(self.grid[i][j])
                        else:
                            self.entry_text[i][j].set('')
            else:
                self.err_flag(3)
    
        if legal == True:
            if self.board_follows_rules():
                    for i in range(9):
                        for j in range(9):
                            if self.grid[i][j] != 0:
                                    self.ent_number[i][j].config(state=tk.DISABLED)
                            if self.grid[i][j] == 0:
                                self.entry_text[i][j].set('')
                    self.initial_grid = deepcopy(self.grid)
                    
                    self.btn_start.pack_forget()
                    self.btn_start_paste.pack_forget()
                    self.frm_bot.pack_forget()
                    self.set_up_window_2()
    
    def board_input_legal(self):
        contains_values = False
        for i in range(9):
            for j in range(9):
                if (len(self.ent_number[i][j].get()) != 0):
                    contains_values = True
                    if not self.ent_number[i][j].get().isdigit():
                        self.err_flag(0)
                        return False
                    elif int(self.ent_number[i][j].get()) not in range(1,10):
                        self.err_flag(0)
                        return False
        if not contains_values:
            self.err_flag(1)
            return False
        return True

    def board_follows_rules(self):
        for i in range(9):
            for j in range(9):
                    if (self.grid[i][j] > 0) and (not self.legal(i,j,self.grid[i][j])):
                        self.err_flag(2)
                        return False
        return True


### window 2 ###
    def set_up_window_2(self):

        self.btn_brute_force = tk.Button(master=self.frm_body_buttons, text="Solve with brute force", font=('TkDefaultFont', 10))
        self.btn_brute_force.bind("<Button-1>", self.brute_force_click)

        self.var_show_iterating = tk.IntVar()
        self.chk_show_iterating = tk.Checkbutton(master = self.frm_body_buttons, text = "show backtracking", variable = self.var_show_iterating, onvalue = 1, offvalue = 0)
        self.chk_show_iterating.select()

        self.btn_back_to_initial = tk.Button(master=self.frm_body, text="Back", font=('TkDefaultFont', 8))
        self.btn_back_to_initial.bind("<Button-1>", self.back_to_initial_click)

        self.btn_candidates = tk.Button(master=self.frm_body_buttons, text="Find candidates", font=('TkDefaultFont', 10))
        self.btn_candidates.bind("<Button-1>", self.candidates_click)    
        
        self.frm_constr = tk.Frame(master = self.frm_body_buttons)

        self.btn_apply_constr = tk.Button(master=self.frm_constr, text="Apply constraints", font=('TkDefaultFont', 10))
        self.btn_apply_constr.bind("<Button-1>", self.apply_constr_click)
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
    def brute_force_click(self, event):
        self.err_flag_reset()

        self.frm_body_buttons.pack_forget()
        self.frm_body.pack()

        lbl_show_iterating = tk.Label(master=self.frm_body, text="Solving via backtracking", font=('TkDefaultFont', 12))
        lbl_show_iterating.pack()
        
        if self.candidates_found == True:
            self.candidates = {pos: cand_list for pos, cand_list in sorted(self.candidates.items(), key= lambda item: len(item[1]))}
        self.squares_list = self.grid_all_squares if self.candidates_found == False else list(self.candidates.keys())
        
        if self.rec_solve(0):
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

    def legal(self,row,col,num):
        for i in range(9):
            if (self.grid[row][i] == num) and (i != col):
                return False
            if (self.grid[i][col] == num) and (i != row):
                return False
        box_row = row - row % 3
        box_col = col - col % 3
        for i in range(box_row, box_row + 3):
            for j in range (box_col, box_col + 3):
                if (self.grid[i][j] == num) and (i != row) and (j != col):
                    return False
        return True

    def rec_solve(self, index):
            
            if index == len(self.squares_list):     # if have filled all squares then sudoku is solved
                return True
            
            pos = self.squares_list[index]
            row, col = pos[0], pos[1]
            
            if self.grid[row][col] != 0:            # if already filled move on to next square 
                return self.rec_solve(index+1)

            cands = range(1,10) if self.candidates_found == False else self.candidates[(row,col)]
            for num in cands:
                if self.legal(row, col, num):
                    self.grid[row][col] = num
                    if self.var_show_iterating.get() == 1:
                        self.entry_text[row][col].set(self.grid[row][col])
                        if self.candidates_found == True:
                            self.frm_cand_square[row][col].pack_forget()
                            self.ent_number[row][col].pack()
                            self.window.update()
                        self.window.after(10,self.window.update())
                    if self.rec_solve(index+1):
                        return True
                self.grid[row][col] = 0
                if self.var_show_iterating.get() == 1:
                    self.entry_text[row][col].set('')
                    if self.candidates_found == True:
                        self.ent_number[row][col].pack_forget()
                        self.frm_cand_square[row][col].pack(side = 'top')
                        self.window.update()
                    self.window.update() 
            return False

    def back_to_initial_click(self, event):
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
    def candidates_click(self, event):
        self.find_all_candidates()
        self.btn_candidates.configure(state='disabled')

    def find_all_candidates(self):
        self.candidates = defaultdict(set)
        self.cand_locations = defaultdict(set)
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                        for num in range(1,10):
                            if self.legal(i, j, num):
                                self.candidates[(i,j)].add(num)
                                self.cand_locations[num].add((i,j))

        # sorting squares by fewest remaining candidates
        self.candidates = {pos: cand_list for pos, cand_list in sorted(self.candidates.items(), key= lambda item: len(item[1]))}

        # creating candidate boxes board
        self.frm_cand_square=[[None]*9 for x in range(9)]
        self.lbl_cand_squares=[[[None]*9 for x in range(9)] for y in range(9)]
        for i in range(9):
            for j in range(9):
                self.frm_cand_square[i][j] = tk.Frame(master=self.frm_square[i][j], relief = 'sunken', bd = -2)
                if self.grid[i][j] == 0:
                    self.ent_number[i][j].pack_forget()
                    for num in range(1,10):
                        k = num-1
                        if num in self.candidates[(i,j)]:
                            self.lbl_cand_squares[i][j][k] = tk.Label(master=self.frm_cand_square[i][j], text=num, font = ('Verdana Pro', 8), bd = -2, bg = 'white', width = 1, pady = 0, padx = 3)
                        else:
                            self.lbl_cand_squares[i][j][k] = tk.Label(master=self.frm_cand_square[i][j], text='', font = ('Verdana Pro', 8), bd = -2, bg = 'white', width = 1, pady = 0, padx = 3)
                        self.lbl_cand_squares[i][j][k].grid(row = k//3, column = k%3)
                    self.frm_cand_square[i][j].pack(fill="none", expand=True)
        
        self.candidates_found = True

    def apply_constr_click(self, event):

        self.err_flag_reset()
        if self.candidates_found == False:
            self.find_all_candidates()
            self.btn_candidates.configure(state='disabled')

        # what happens when a number is found
        def found(row, col, num, method):
            self.grid[row][col] = num           # update the grid array with the found number

            if method == 'sc':
                self.lbl_cand_squares[row][col][num-1].configure(bg='darkolivegreen1')
                self.chk_constr_list[0].configure(bg = 'darkolivegreen1')
                self.window.update()

                self.window.after(300, self.frm_cand_square[row][col].pack_forget())
                self.entry_text[row][col].set(self.grid[row][col])
                self.ent_number[row][col].configure(bg='darkolivegreen1')
                self.ent_number[row][col].pack()
                self.window.update()

                self.window.after(300, self.window.update())
                self.ent_number[row][col].configure(bg='white')
                # self.window.after(300, self.ent_number[row][col].configure(bg='white', highlightthickness = 3, highlightbackground = 'darkolivegreen1'))
                self.chk_constr_list[0].configure(bg = '#F0F0F0')

            if 'hs' in method:
                if 'row' in method:
                    squares = self.grid_rows[row]
                elif 'col' in method:
                        squares = self.grid_cols[col]
                elif 'box' in method:
                        squares = self.grid_boxes[3*(row//3) + col//3]
            
                for pos in squares:
                    if self.grid[pos[0]][pos[1]] == 0:
                        self.lbl_cand_squares[pos[0]][pos[1]][num-1].configure(bg='#c2ffff')
                    elif self.grid[pos[0]][pos[1]] == num:
                        self.lbl_cand_squares[pos[0]][pos[1]][num-1].configure(bg='darkslategray1')
                self.chk_constr_list[1].configure(bg = 'darkslategray1')
                self.window.update()

                self.window.after(300, self.frm_cand_square[row][col].pack_forget())
                self.entry_text[row][col].set(self.grid[row][col])
                self.ent_number[row][col].configure(bg='darkslategray1')
                self.ent_number[row][col].pack()

                self.window.update()
                
                for pos in squares:
                    if self.grid[pos[0]][pos[1]] == 0:
                        self.lbl_cand_squares[pos[0]][pos[1]][num-1].configure(bg='white')

                self.window.after(300, self.window.update())
                self.ent_number[row][col].configure(bg='white')
                # self.window.after(300, self.ent_number[row][col].configure(bg='white', highlightthickness = 3, highlightbackground = 'darkslategray1')       
                self.chk_constr_list[1].configure(bg = '#F0F0F0')

            self.update_candidates(row, col, num)
            self.window.update()

        def add_constraint(pos_list, group_index, cand_list, remove_list, method):
            if any(['np' in method, 'nt' in method]):

                if 'np' in method:
                    main_colour = 'orchid1'
                    sec_colour = '#ffbdfc'
                    index = 2
                elif 'nt' in method:
                    main_colour = 'tan1'
                    sec_colour = '#ffdebf'
                    index = 3
                
                for cand in cand_list:
                    for pos in pos_list:
                        self.lbl_cand_squares[pos[0]][pos[1]][cand-1].configure(bg=main_colour)
                    for pos in remove_list:
                        if cand in self.candidates[pos]:
                            self.lbl_cand_squares[pos[0]][pos[1]][cand-1].configure(bg = sec_colour)
                self.chk_constr_list[index].configure(bg = main_colour)
                self.window.update()

                self.window.after(300, self.window.update())

                for cand in cand_list:
                    for pos in remove_list:
                        if cand in self.candidates[pos]:
                            self.remove_candidates(pos,cand)
                self.window.update()

                self.window.after(300, self.window.update())
                for cand in cand_list:
                    for pos in pos_list:
                        self.lbl_cand_squares[pos[0]][pos[1]][cand-1].configure(bg='white')

                self.chk_constr_list[index].configure(bg = '#F0F0F0')
 
            if any(['hp' in method, 'ht' in method]):
                if 'row' in method:
                    squares = self.grid_rows[group_index]
                elif 'col' in method:
                    squares = self.grid_cols[group_index]
                elif 'box' in method:
                    squares = self.grid_boxes[group_index]

                if 'hp' in method:
                    main_colour = 'palevioletred1'
                    sec_colour = '#ffc9db'
                    index = 4
                
                if 'ht' in method:
                    main_colour = 'mediumpurple1'
                    sec_colour = '#dbcaff'
                    index = 5

                for pos in squares:
                    if self.grid[pos[0]][pos[1]] == 0:
                        if pos in pos_list:
                            for num in range(1,10):
                                if num in cand_list:
                                    self.lbl_cand_squares[pos[0]][pos[1]][num-1].configure(bg = main_colour)
                                elif num in self.candidates[pos]:
                                    self.lbl_cand_squares[pos[0]][pos[1]][num-1].configure(fg = main_colour)
                        else:
                            for num in cand_list:
                                self.lbl_cand_squares[pos[0]][pos[1]][num-1].configure(bg = sec_colour)

                self.chk_constr_list[index].configure(bg = main_colour)
                self.window.update()

                self.window.after(500, self.window.update())

                for pos in remove_list:
                    for num in range(1,10):
                        if num not in cand_list and num in self.candidates[pos]:
                            self.remove_candidates(pos,num)


                self.window.update()

                self.window.after(300, self.window.update())
                for pos in squares:
                    if self.grid[pos[0]][pos[1]] == 0:
                        if pos in pos_list:
                            for num in cand_list:
                                self.lbl_cand_squares[pos[0]][pos[1]][num-1].configure(bg='white')
                        else:
                            for num in cand_list:
                                self.lbl_cand_squares[pos[0]][pos[1]][num-1].configure(bg = 'white')


                self.chk_constr_list[index].configure(bg = '#F0F0F0')
            

        # constraint functions 
        def sole_candidates(self):             # find any squares that only have one candidate
            for pos, cand_list in self.candidates.items():
                if self.grid[pos[0]][pos[1]] == 0:
                    if len(cand_list) == 1:
                        found(pos[0], pos[1], cand_list.pop(), method='sc')
                        return True
            return False
        
        def hidden_singles(self):             # find any squares with a candidate that is unique in its row/column/box   
            for num, pos_list in self.cand_locations.items():
                for method, groups in zip(['hs_row', 'hs_col', 'hs_box'], [self.grid_rows, self.grid_cols, self.grid_boxes]):
                    for group in groups:
                        shared = group & pos_list
                        if len(shared) == 1:
                            pos = shared.pop()
                            if self.grid[pos[0]][pos[1]] == 0:
                                found(pos[0], pos[1], num, method=method)
                                return True
       
        def naked_pairs(self):             # add constraints from naked pairs 
            for method, groups in zip(['np_row', 'np_col', 'np_box'], [self.grid_rows, self.grid_cols, self.grid_boxes]):
                for group in groups:
                    candidates_in_group = set()
                    for pos in list(group):
                        if self.grid[pos[0]][pos[1]] == 0:
                            candidates_in_group.update(self.candidates[pos])
                    naked_combinations = list(combinations(list(candidates_in_group), 2))
                    for naked_cands in naked_combinations:
                        naked_list = []
                        remove_list = []
                        for pos in list(group):
                            if self.grid[pos[0]][pos[1]] == 0 and len((set(range(1,10)) - set(naked_cands)) & self.candidates[pos]) ==  0: # only contains numbers in the combination
                                naked_list.append(pos)
                            elif self.grid[pos[0]][pos[1]] == 0 and len(set(naked_cands) & self.candidates[pos]) != 0:     # other squares with the numbers in
                                remove_list.append(pos)
                        if len(naked_list) == 2 and len(remove_list) != 0:
                            add_constraint(naked_list, groups.index(group), naked_cands, remove_list, method)
                            return True

        def naked_triples(self):             # add constraints from naked triples 
            for method, groups in zip(['nt_row', 'nt_col', 'nt_box'], [self.grid_rows, self.grid_cols, self.grid_boxes]):
                for group in groups:
                    candidates_in_group = set()
                    for pos in list(group):
                        if self.grid[pos[0]][pos[1]] == 0:
                            candidates_in_group.update(self.candidates[pos])
                    naked_combinations = list(combinations(list(candidates_in_group), 3))
                    for naked_cands in naked_combinations:
                        naked_list = []
                        remove_list = []
                        for pos in list(group):
                            if self.grid[pos[0]][pos[1]] == 0 and len((set(range(1,10)) - set(naked_cands)) & self.candidates[pos]) ==  0: # only contains numbers in the combination
                                naked_list.append(pos)
                            elif self.grid[pos[0]][pos[1]] == 0 and len(set(naked_cands) & self.candidates[pos]) != 0:     # other squares with the numbers in
                                remove_list.append(pos)
                        if len(naked_list) == 3 and len(remove_list) != 0:
                            add_constraint(naked_list, groups.index(group), naked_cands, remove_list, method)
                            return True                          
  
        def hidden_pairs(self):             # add constraints from hidden pairs 
            for method, groups in zip(['hp_row', 'hp_col', 'hp_box'], [self.grid_rows, self.grid_cols, self.grid_boxes]):
                for group in groups:
                    candidates_in_group = set()
                    for pos in list(group):
                        if self.grid[pos[0]][pos[1]] == 0:
                            candidates_in_group.update(self.candidates[pos])
                    hidden_combinations = list(combinations(list(candidates_in_group), 2))
                    for hidden_cands in hidden_combinations:
                        hidden_list = []
                        naked_list = []
                        remove_list = []
                        for pos in list(group):
                            if self.grid[pos[0]][pos[1]] == 0 and len((set(range(1,10)) - set(hidden_cands)) & self.candidates[pos]) !=  0 and len((set(hidden_cands)) & self.candidates[pos]) !=  0: # only contains numbers in the combination
                                hidden_list.append(pos)
                                remove_list.append(pos)
                            elif self.grid[pos[0]][pos[1]] == 0 and len(set(hidden_cands) & self.candidates[pos]) != 0:     # other squares with the numbers in
                                hidden_list.append(pos)
                                naked_list.append(pos)
                        if len(hidden_list) == 2 and len(naked_list) < 2:
                            add_constraint(hidden_list, groups.index(group), hidden_cands, remove_list, method)
                            return True                   
       
        def hidden_triples(self):             # add constraints from hidden triples 
            for method, groups in zip(['ht_row', 'ht_col', 'ht_box'], [self.grid_rows, self.grid_cols, self.grid_boxes]):
                for group in groups:
                    candidates_in_group = set()
                    for pos in list(group):
                        if self.grid[pos[0]][pos[1]] == 0:
                            candidates_in_group.update(self.candidates[pos])
                    hidden_combinations = list(combinations(list(candidates_in_group), 3))
                    for hidden_cands in hidden_combinations:
                        hidden_list = []
                        naked_list = []
                        remove_list = []
                        for pos in list(group):
                            if self.grid[pos[0]][pos[1]] == 0 and len((set(range(1,10)) - set(hidden_cands)) & self.candidates[pos]) !=  0 and len((set(hidden_cands)) & self.candidates[pos]) !=  0: # only contains numbers in the combination
                                hidden_list.append(pos)
                                remove_list.append(pos)
                            elif self.grid[pos[0]][pos[1]] == 0 and len(set(hidden_cands) & self.candidates[pos]) != 0:     # other squares with the numbers in
                                hidden_list.append(pos)
                                naked_list.append(pos)
                        if len(hidden_list) == 3 and len(naked_list) < 3:
                            add_constraint(hidden_list, groups.index(group), hidden_cands, remove_list, method)
                            return True                   
       
       # applying constraints recursively 

        self.function_list = [None, sole_candidates]
        for i, function in zip(range(1, len(self.var_constr_list)), [hidden_singles, naked_pairs, naked_triples, hidden_pairs, hidden_triples]):
            if self.var_constr_list[i].get() == 1:
                self.function_list.append(function)


        def create_func_loop(index):
            def func_loop(self):
                loop, last_change = 0, 0
                while last_change == loop:
                    loop += 1

                    if self.function_list[index-1]:
                        self.method_list[index-2](self)

                    if self.function_list[index](self):
                        last_change = loop
            return func_loop
        
        self.method_list = [create_func_loop(index) for index in range(1,len(self.function_list))]
        self.method_list.append(None)
        
        solved = lambda self: 0 not in set([x for xs in self.grid for x in xs])

        def solve(self, index):
            self.method_list[index](self)

            if solved(self):
                return True

            elif self.method_list[index+1]:
                return solve(self,index+1)

            else:
                return False

        if solve(self,0):
            self.frm_body_buttons.pack_forget()
            self.lbl_sol = tk.Label(master=self.frm_body, text="Solved", font=('TkDefaultFont', 14, 'bold'))
            self.lbl_sol.pack()
            self.btn_back_to_initial.pack()

        else:
            self.err_flag(4)


    def remove_candidates(self,pos,num):
        self.candidates[pos].remove(num)
        self.cand_locations[num].remove(pos)
        self.lbl_cand_squares[pos[0]][pos[1]][num-1].configure(text='')

    def update_candidates(self,row,col,num):
        for pos, cand_list in self.candidates.items():
            i, j = pos[0], pos[1]
            if any([i == row, j == col, ((i//3 == row//3) and (j//3 == col//3))]):
                if num in cand_list:
                    self.candidates[(i,j)].remove(num)
                    self.cand_locations[num].remove((i,j))
                    self.lbl_cand_squares[i][j][num-1].configure(text='')
        for cand in self.candidates[(row,col)]:
            self.cand_locations[cand].remove((row,col))
        del self.candidates[(row,col)]

if __name__ == "__main__":
    window = tk.Tk()
    app = SudokuSolver(window)
    window.mainloop() 