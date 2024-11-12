import __main__
if "2d" in __main__.__file__:
    from modules.gui import squares_2d as squares
else:
    from modules.gui import squares_3d as squares

def reset_board(self):
    for pos in self.grid_all_squares:
        squares.change_square_colour(self, pos, 'white')
        if self.grid[pos[0]][pos[1]] == 0:
            for cand in range(1,10):
                squares.change_cand_colour(self, pos, cand, 'white')
    for chk_constr in self.chk_constr_list:
        chk_constr.configure(bg = '#F0F0F0')

def value(self, pos, method, group_index): # used in constraints
    num = self.grid[pos[0]][pos[1]]
    reset_board(self)

    if method == 'sc':
        self.chk_constr_list[0].configure(bg = 'darkolivegreen1')

        squares.change_cand_colour(self, pos, num, 'darkolivegreen1')
        self.window.update()
        self.window.after(300, squares.hide_candidates(self, pos))

        squares.set_value(self, pos, num)  
        squares.change_square_colour(self, pos, 'darkolivegreen1')
        self.window.update()
        self.window.after(300,self.window.update())

    if method[:2] == 'hs':

        if 'row' in method:
            pos_sqs = self.grid_rows[group_index]
        elif 'box' in method:
            pos_sqs = self.grid_boxes[group_index]
    
        self.chk_constr_list[1].configure(bg = '#c2ffff')

        for pos_sq in pos_sqs:
            if self.grid[pos_sq[0]][pos_sq[1]] == 0:
                squares.change_cand_colour(self, pos_sq, num, '#c2ffff')
            elif self.grid[pos_sq[0]][pos_sq[1]] == num:
                squares.change_cand_colour(self, pos_sq, num, 'darkslategray1')
        self.window.update()
        self.window.after(300, squares.hide_candidates(self, pos))

        squares.set_value(self, pos, num)      
        squares.change_square_colour(self, pos, 'darkslategray1')
        self.window.update()
        self.window.after(300,self.window.update())


def constraint(self, pos_list, cand_list, remove_list, method, group_index): # used in constraints
    reset_board(self)

    if any([method[:2] =='np', method[:2] =='nt']):
        if method[1] == 'p':
            main_colour = 'orchid1'
            sec_colour = '#ffbdfc'
            index = 2
        elif method[1] == 't':
            main_colour = 'tan1'
            sec_colour = '#ffdebf'
            index = 3

        self.chk_constr_list[index].configure(bg = sec_colour)

        for cand in cand_list:
            for pos in pos_list:
                squares.change_cand_colour(self, pos, cand, main_colour)
            for pos in remove_list:
                if cand in self.candidates[pos]:
                    squares.change_cand_colour(self, pos, cand, sec_colour)
        self.window.update()
        self.window.after(300, self.window.update())

        for cand in cand_list:
            for pos in remove_list:
                if cand in self.candidates[pos]:
                    squares.remove_candidate(self, pos, cand)
        self.window.update()
        self.window.after(300, self.window.update())

    if any([method[:2] =='hp', method[:2] =='ht']):
        if 'row' in method:
            pos_sqs = self.grid_rows[group_index]
        elif 'box' in method:
            pos_sqs = self.grid_boxes[group_index]

        if method[1] == 'p':
            main_colour = '#a8b7ff'
            sec_colour = '#cfd7ff' 
            third_colour = '#e7ebff'
            index = 4
        
        if method[1] == 't':
            main_colour = '#b996ff'
            sec_colour = '#dbcaff'
            third_colour = '#eee6ff'
            index = 5

        self.chk_constr_list[index].configure(bg = sec_colour)

        for pos in pos_sqs:
            if self.grid[pos[0]][pos[1]] == 0:
                if pos in pos_list:
                    for num in range(1,10):
                        if num in cand_list:
                            squares.change_cand_colour(self, pos, num, main_colour)
                        elif num in self.candidates[pos]:
                            squares.change_cand_colour(self, pos, num, sec_colour)
                else:
                    for num in cand_list:
                        squares.change_cand_colour(self, pos, num, third_colour)

        self.window.update()
        self.window.after(500, self.window.update())

        for pos in remove_list:
            for num in range(1,10):
                if num not in cand_list and num in self.candidates[pos]:
                    squares.remove_candidate(self, pos, num)

        self.window.update()
        self.window.after(300, self.window.update())
    
    if method[:2] == 'ir':
        if any(['point' in method, 'box_line' in method]):
            main_colour = '#ffd811'
            sec_colour = '#ffeb86'
            third_colour = '#fff2af'
            index = 6
        elif '3d' in method:
            main_colour = 'palevioletred1'
            sec_colour = '#ffc9db'
            third_colour = '#ffe9f0' 
            index = 7

        if 'point' in method:
            pos_sqs = self.grid_boxes[group_index]
        elif 'box_line' in method or '3d' in method:
            pos_sqs = self.grid_rows[group_index]
            
        self.chk_constr_list[index].configure(bg = sec_colour)

        num = cand_list[0]

        for pos in pos_sqs:
            if pos in pos_list:
                squares.change_cand_colour(self, pos, num, main_colour)
            elif self.grid[pos[0]][pos[1]] == 0:
                squares.change_cand_colour(self, pos, num, third_colour)
        for pos in remove_list:
            squares.change_cand_colour(self, pos, num, sec_colour)
        
        self.window.update()
        self.window.after(300, self.window.update())

        for pos in remove_list:
            squares.remove_candidate(self, pos, num)

        self.window.update()
        self.window.after(300, self.window.update())
