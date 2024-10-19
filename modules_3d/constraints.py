from itertools import combinations

from modules_3d import candidates

# what happens when a number is found
def found(self, pos, num, method, index = -1):
    box, sq = pos[0], pos[1]
    self.grid[box][sq] = num           # update the grid array with the found number

    if method == 'sc':
        self.cnv_board.itemconfigure(self.shp_cand_square[box][sq][num-1], fill = 'darkolivegreen1')
        self.chk_constr_list[0].configure(bg = 'darkolivegreen1')
        self.window.update()

        self.window.after(300, self.window.update())
        for k in range(9):
            self.cnv_board.itemconfigure(self.shp_cand_square[box][sq][k], state = 'hidden')
            self.cnv_board.itemconfigure(self.lbl_cand_square[box][sq][k], state = 'hidden')

        self.cnv_board.itemconfigure(self.lbl_square[box][sq], text = self.grid[box][sq])
        self.cnv_board.itemconfigure(self.shp_square[box][sq], fill = 'darkolivegreen1')
        self.window.update()

        self.window.after(300, self.window.update())
        self.cnv_board.itemconfigure(self.shp_square[box][sq], fill = 'white')
        # self.window.after(300, self.ent_number[box][sq].configure(bg='white', highlightthickness = 3, highlightbackground = 'darkolivegreen1'))
        self.chk_constr_list[0].configure(bg = '#F0F0F0')

    if 'hs' in method:
        if 'row' in method:
            squares = self.grid_rows[index]
        elif 'box' in method:
            squares = self.grid_boxes[index]
    
        for pos_sq in squares:
            if self.grid[pos_sq[0]][pos_sq[1]] == 0:
                self.cnv_board.itemconfigure(self.shp_cand_square[pos_sq[0]][pos_sq[1]][num-1], fill = '#c2ffff')
            elif self.grid[pos_sq[0]][pos_sq[1]] == num:
                self.cnv_board.itemconfigure(self.shp_cand_square[pos_sq[0]][pos_sq[1]][num-1], fill = 'darkslategray1')
        self.chk_constr_list[1].configure(bg = 'darkslategray1')
        self.window.update()

        self.window.after(300, self.window.update())
        for k in range(9):
            self.cnv_board.itemconfigure(self.shp_cand_square[box][sq][k], state = 'hidden')
            self.cnv_board.itemconfigure(self.lbl_cand_square[box][sq][k], state = 'hidden')

        self.cnv_board.itemconfigure(self.lbl_square[box][sq], text = self.grid[box][sq])
        self.cnv_board.itemconfigure(self.shp_square[box][sq], fill = 'darkslategray1')

        self.window.update()
        
        for pos_sq in squares:
            if self.grid[pos_sq[0]][pos_sq[1]] == 0:
                self.cnv_board.itemconfigure(self.shp_cand_square[pos_sq[0]][pos_sq[1]][num-1], fill = 'white')

        self.window.after(300, self.window.update())
        self.cnv_board.itemconfigure(self.shp_square[box][sq], fill = 'white')
        # self.window.after(300, self.ent_number[box][sq].configure(bg='white', highlightthickness = 3, highlightbackground = 'darkslategray1')       
        self.chk_constr_list[1].configure(bg = '#F0F0F0')

    candidates.update(self, pos, num)
    self.window.update()

def add_constraint(self, pos_list, group_index, cand_list, remove_list, method):
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
                self.cnv_board.itemconfigure(self.shp_cand_square[pos[0]][pos[1]][cand-1], fill = main_colour)
            for pos in remove_list:
                if cand in self.candidates[pos]:
                    self.cnv_board.itemconfigure(self.shp_cand_square[pos[0]][pos[1]][cand-1], fill = sec_colour)
        self.chk_constr_list[index].configure(bg = main_colour)
        self.window.update()

        self.window.after(300, self.window.update())

        for cand in cand_list:
            for pos in remove_list:
                if cand in self.candidates[pos]:
                    candidates.remove(self, pos,cand)
        self.window.update()

        self.window.after(300, self.window.update())
        for cand in cand_list:
            for pos in pos_list:
                self.cnv_board.itemconfigure(self.shp_cand_square[pos[0]][pos[1]][cand-1], fill = 'white')

        self.chk_constr_list[index].configure(bg = '#F0F0F0')

    if any(['hp' in method, 'ht' in method]):
        if 'row' in method:
            squares = self.grid_rows[group_index]
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
                            self.cnv_board.itemconfigure(self.shp_cand_square[pos[0]][pos[1]][num-1], fill = main_colour)
                        elif num in self.candidates[pos]:
                            self.cnv_board.itemconfigure(self.shp_cand_square[pos[0]][pos[1]][num-1], fill = main_colour)
                else:
                    for num in cand_list:
                        self.cnv_board.itemconfigure(self.shp_cand_square[pos[0]][pos[1]][num-1], fill = sec_colour)

        self.chk_constr_list[index].configure(bg = main_colour)
        self.window.update()

        self.window.after(500, self.window.update())

        for pos in remove_list:
            for num in range(1,10):
                if num not in cand_list and num in self.candidates[pos]:
                    candidates.remove(self, pos,num)

        self.window.update()

        self.window.after(300, self.window.update())
        for pos in squares:
            if self.grid[pos[0]][pos[1]] == 0:
                if pos in pos_list:
                    for num in cand_list:
                        self.cnv_board.itemconfigure(self.shp_cand_square[pos[0]][pos[1]][num-1], fill = sec_colour)
                else:
                    for num in cand_list:
                        self.cnv_board.itemconfigure(self.shp_cand_square[pos[0]][pos[1]][num-1], fill = 'white')

        self.chk_constr_list[index].configure(bg = '#F0F0F0')
    

# constraint functions 
def sole_candidates(self):             # find any squares that only have one candidate
    for pos, cand_list in self.candidates.items():
        if self.grid[pos[0]][pos[1]] == 0:
            if len(cand_list) == 1:
                found(self, pos, cand_list.pop(), method='sc')
                return True
    return False

def hidden_singles(self):             # find any squares with a candidate that is unique in its row/column/box   
    for num, pos_list in self.cand_locations.items():
        for method, groups in zip(['hs_box', 'hs_row'], [self.grid_boxes, self.grid_rows]):
            for group in groups:
                shared = group & pos_list
                if len(shared) == 1:
                    pos = shared.pop()
                    if self.grid[pos[0]][pos[1]] == 0:
                        found(self, pos, num, method=method, index = groups.index(group))
                        return True

def naked_pairs(self):             # add constraints from naked pairs 
    for method, groups in zip(['np_box', 'np_row'], [self.grid_boxes, self.grid_rows]):
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
                    add_constraint(self, naked_list, groups.index(group), naked_cands, remove_list, method)
                    return True

def naked_triples(self):             # add constraints from naked triples 
    for method, groups in zip(['nt_box', 'nt_row'], [self.grid_boxes, self.grid_rows]):
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
                    add_constraint(self, naked_list, groups.index(group), naked_cands, remove_list, method)
                    return True                          

def hidden_pairs(self):             # add constraints from hidden pairs 
    for method, groups in zip(['hp_box', 'hp_row'], [self.grid_boxes, self.grid_rows]):
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
                    add_constraint(self, hidden_list, groups.index(group), hidden_cands, remove_list, method)
                    return True                   

def hidden_triples(self):             # add constraints from hidden triples 
    for method, groups in zip(['ht_box', 'ht_row'], [self.grid_boxes, self.grid_rows]):
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
                    add_constraint(self, hidden_list, groups.index(group), hidden_cands, remove_list, method)
                    return True  


# applying constraints recursively 
def solve_constraints(self):
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
    
    return solve(self,0)
