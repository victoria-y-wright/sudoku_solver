import __main__
if "2d" in __main__.__file__:
    from modules.gui import squares_2d as squares
else:
    from modules.gui import squares_3d as squares

def value(self, pos, method, group_index): # used in constraints
    
    num = self.grid[pos[0]][pos[1]]

    if method == 'sc':
        self.chk_constr_list[0].configure(bg = 'darkolivegreen1')

        squares.change_cand_colour(self, pos, num, 'darkolivegreen1')
        self.window.update()
        self.window.after(300, squares.hide_candidates(self, pos))

        squares.set_value(self, pos, num)  
        squares.change_square_colour(self, pos, 'darkolivegreen1')
        self.window.update()
        self.window.after(300, squares.change_square_colour(self, pos, 'white'))

        self.chk_constr_list[0].configure(bg = '#F0F0F0')

    if 'hs' in method:

        if 'row' in method:
            pos_sqs = self.grid_rows[group_index]
        elif 'box' in method:
            pos_sqs = self.grid_boxes[group_index]
    
        self.chk_constr_list[1].configure(bg = 'darkslategray1')

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
        for pos_sq in pos_sqs:
            if self.grid[pos_sq[0]][pos_sq[1]] == 0:
                squares.change_cand_colour(self, pos_sq, num, 'white')
        self.window.after(300, squares.change_square_colour(self, pos, 'white'))

        self.chk_constr_list[1].configure(bg = '#F0F0F0')


def constraint(self, pos_list, cand_list, remove_list, method, group_index): # used in constraints

    if any(['np' in method, 'nt' in method]):
        if 'np' in method:
            main_colour = 'orchid1'
            sec_colour = '#ffbdfc'
            index = 2
        elif 'nt' in method:
            main_colour = 'tan1'
            sec_colour = '#ffdebf'
            index = 3

        self.chk_constr_list[index].configure(bg = main_colour)

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

        for cand in cand_list:
            for pos in pos_list:
                squares.change_cand_colour(self, pos, cand,'white')
            for pos in remove_list:
                if cand in self.candidates[pos]:
                    squares.change_cand_colour(self, pos, cand, 'white')


        self.chk_constr_list[index].configure(bg = '#F0F0F0')

    if any(['hp' in method, 'ht' in method]):
        if 'row' in method:
            pos_sqs = self.grid_rows[group_index]
        elif 'box' in method:
            pos_sqs = self.grid_boxes[group_index]

        if 'hp' in method:
            main_colour = 'palevioletred1'
            sec_colour = '#ffc9db'
            index = 4
        
        if 'ht' in method:
            main_colour = 'mediumpurple1'
            sec_colour = '#dbcaff'
            index = 5

        self.chk_constr_list[index].configure(bg = main_colour)

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
                        squares.change_cand_colour(self, pos, num, sec_colour)

        self.window.update()
        self.window.after(500, self.window.update())

        for pos in remove_list:
            for num in range(1,10):
                if num not in cand_list and num in self.candidates[pos]:
                    squares.remove_candidate(self, pos, num)

        self.window.update()

        self.window.after(300, self.window.update())
        for pos in pos_sqs:
            if self.grid[pos[0]][pos[1]] == 0:
                for num in cand_list:
                    squares.change_cand_colour(self, pos, num,'white')
        
        for pos in remove_list:
            for num in range(1,10):
                if num not in cand_list and num in self.candidates[pos]:
                    squares.change_cand_colour(self, pos, num,'white')

        self.chk_constr_list[index].configure(bg = '#F0F0F0')
