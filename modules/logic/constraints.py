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
        for method, groups in zip(['hs_box', 'hs_line'], [self.grid_boxes, self.grid_lines]):
            for group in groups:
                pos_in_group = group & pos_list
                if len(pos_in_group) == 1:
                    pos = pos_in_group.pop()
                    if self.grid[pos[0]][pos[1]] == 0:
                        found.value(self, pos, num, method, groups.index(group))
                        return True
    return False

def naked_pairs(self):             # remove candidates using naked pairs 
    for method, groups in zip(['np_box', 'np_line'], [self.grid_boxes, self.grid_lines]):
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
    return False

def naked_triples(self):             # remove candidates using naked triples 
    for method, groups in zip(['nt_box', 'nt_line'], [self.grid_boxes, self.grid_lines]):
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
    return False

def hidden_pairs(self):             # remove candidates using hidden pairs 
    for method, groups in zip(['hp_box', 'hp_line'], [self.grid_boxes, self.grid_lines]):
        for group in groups:
            candidates_in_group = set()
            for pos in list(group):
                if self.grid[pos[0]][pos[1]] == 0:
                    candidates_in_group.update(self.candidates[pos])
            hidden_combinations = list(combinations(list(candidates_in_group), 2))
            for hidden_cands in hidden_combinations:
                hidden_list = []
                remove_list = []
                for pos in list(group):
                    if self.grid[pos[0]][pos[1]] == 0 and len((set(hidden_cands)) & self.candidates[pos]) !=  0: # contains numbers in the combination
                        hidden_list.append(pos)
                        if len((set(range(1,10)) - set(hidden_cands)) & self.candidates[pos]) !=  0: # also contains other numbers
                            remove_list.append(pos)
                if len(hidden_list) == 2 and len(remove_list) > 0:
                    found.constraint(self, hidden_list, hidden_cands, remove_list, method, groups.index(group))
                    pass
                    return True                   
    return False

def hidden_triples(self):             # remove candidates using hidden triples 
    for method, groups in zip(['ht_box', 'ht_line'], [self.grid_boxes, self.grid_lines]):
        for group in groups:
            candidates_in_group = set()
            for pos in list(group):
                if self.grid[pos[0]][pos[1]] == 0:
                    candidates_in_group.update(self.candidates[pos])
            hidden_combinations = list(combinations(list(candidates_in_group), 3))
            for hidden_cands in hidden_combinations:
                hidden_list = []
                remove_list = []
                for pos in list(group):
                    if self.grid[pos[0]][pos[1]] == 0 and len((set(hidden_cands)) & self.candidates[pos]) !=  0: # contains numbers in the combination
                        hidden_list.append(pos)
                        if len((set(range(1,10)) - set(hidden_cands)) & self.candidates[pos]) !=  0: # also contains other numbers
                            remove_list.append(pos)
                if len(hidden_list) == 3 and len(remove_list) > 0:
                    found.constraint(self, hidden_list, hidden_cands, remove_list, method, groups.index(group))
                    return True  
    return False

def intersection_removal(self):                 # remove candidates using pointing pairs/triples or box-line intersection
    for num, pos_list in self.cand_locations.items():
        for method, main_groups, intersecting_groups in zip(['ir_point', 'ir_box_line'],[self.grid_boxes, self.grid_lines], [self.grid_lines, self.grid_boxes]):
            for main_group in main_groups:
                pos_in_main = main_group & pos_list
                if len(pos_in_main) == 2 or len(pos_in_main) == 3:
                    for intersecting_group in intersecting_groups:
                        if intersecting_group.issuperset(pos_in_main):
                            pos_in_intersecting = intersecting_group & pos_list
                            if len(pos_in_intersecting) > len(pos_in_main):
                                remove_list = list(pos_in_intersecting - pos_in_main)
                                intersection_list = list(pos_in_main)
                                found.constraint(self, intersection_list, [num], remove_list, method, main_groups.index(main_group))
                                return True
    return False

def intersection_3d(self):
    for num, pos_list in self.cand_locations.items():
        for line in self.grid_lines:
            pos_in_line = pos_list & line
            if len(pos_in_line) == 2:
                intersecting_lines = [other_line for other_line in self.grid_lines if len(pos_in_line & other_line) == 1]
                if len(intersecting_lines) == 2:
                    common = (intersecting_lines[0] & intersecting_lines[1])
                    if len(common) != 0:
                        remove_pos = common.pop()
                        if remove_pos in pos_list:
                            intersection_list = list(pos_in_line)
                            found.constraint(self, intersection_list, [num], [remove_pos], 'ir_3d', self.grid_lines.index(line))
                            return True
    return False