from itertools import combinations

from modules.logic import found

def sole_candidates(self):             # find any squares that only have one candidate
    for pos, cand_list in self.candidates.items():
        if self.grid[pos[0]][pos[1]] == 0:
            if len(cand_list) == 1:
                found.value(self, pos, cand_list.pop(), method='sc')
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
                        found.value(self, pos, num, method, groups.index(group))
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
                    found.constraint(self, naked_list, naked_cands, remove_list, method, groups.index(group))
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
                    found.constraint(self, naked_list, naked_cands, remove_list, method, groups.index(group))
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
                    found.constraint(self, hidden_list, hidden_cands, remove_list, method, groups.index(group))
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
                    found.constraint(self, hidden_list, hidden_cands, remove_list, method, groups.index(group))
                    pass
                    return True  