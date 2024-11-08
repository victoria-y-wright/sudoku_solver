from itertools import combinations

from modules_logic import candidates
from modules_gui import visualisation

def found_value(self, pos, num, method, group_index=-1):
    self.grid[pos[0]][pos[1]] = num  
    visualisation.value(self, pos, method, group_index)
    candidates.update(self, pos, num)

def found_constraint(self, pos_list, cand_list, remove_list, method, group_index):
    visualisation.constraint(self, pos_list, cand_list, remove_list, method, group_index)
    if any(['np' in method, 'nt' in method]):
        for cand in cand_list:
            for pos in remove_list:
                if cand in self.candidates[pos]:
                    self.candidates[pos].remove(cand)
                    self.cand_locations[cand].remove(pos)
    if any(['hp' in method, 'ht' in method]):
        for pos in remove_list:
            for num in range(1,10):
                if num not in cand_list and num in self.candidates[pos]:
                    self.candidates[pos].remove(num)
                    self.cand_locations[num].remove(pos)

# constraint functions 
def sole_candidates(self):             # find any squares that only have one candidate
    for pos, cand_list in self.candidates.items():
        if self.grid[pos[0]][pos[1]] == 0:
            if len(cand_list) == 1:
                found_value(self, pos, cand_list.pop(), method='sc')
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
                        found_value(self, pos, num, method, groups.index(group))
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
                    found_constraint(self, naked_list, naked_cands, remove_list, method, groups.index(group))
                    pass
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
                    found_constraint(self, naked_list, naked_cands, remove_list, method, groups.index(group))
                    pass
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
                    found_constraint(self, hidden_list, hidden_cands, remove_list, method, groups.index(group))
                    pass
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
                    found_constraint(self, hidden_list, hidden_cands, remove_list, method, groups.index(group))
                    pass
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
