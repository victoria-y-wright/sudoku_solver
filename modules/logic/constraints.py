"""Functions for individual constraints/ Sudoku solving strategies"""

from itertools import combinations

from modules.logic import found

def sole_candidates(self):             
    """Checks through the board to see if there is a square with only one possible candidate
    and identifies it as found"""

    # iterates through all empty squares
    for pos, cand_list in self.candidates.items():
        # checks if only one candidate
        if len(cand_list) == 1:
            num = list(cand_list)[0]
            # calls found.value to update the board
            found.value(self, pos, num, method='sc')
            return True
    return False


def hidden_singles(self):               
    """Checks through the board to see if there are any groups where a candidate is unique 
    (showing up in only one square) and identifies it as found"""

    # iterates through all numbers and the positions where they could be
    for num, pos_list in self.cand_locations.items():

        # checks all groups- both boxes and lines (i.e. rows and columns)
        for method, groups in zip(['hs_box', 'hs_line'], [self.grid_boxes, self.grid_lines]):
            for group in groups:

                # finds the positions in the current group where 'num' could be
                # and checks if there is only one
                pos_in_group = group & pos_list
                if len(pos_in_group) == 1:
                    pos = pos_in_group.pop()
                    # calls found.value to update the board
                    found.value(self, pos, num, method, groups.index(group))
                    return True
    return False


def naked_pairs(self):             
    """Checks through the board to see if any groups contain naked pairs
    - where two squares can only take the two same candidate values-
    then removes these numbers as candidates for other squares in the group """

    # checks all groups- both boxes and lines (i.e. rows and columns)
    for method, groups in zip(['np_box', 'np_line'], [self.grid_boxes, self.grid_lines]):
        for group in groups:
            
            # creates a set of all candidates in the current group
            candidates_in_group = set()
            for pos in list(group):
                if self.grid[pos[0]][pos[1]] == 0:
                    candidates_in_group.update(self.candidates[pos])

            # generates all possible two-number combinations in the group
            naked_combinations = list(combinations(list(candidates_in_group), 2))

            # iterates through all two-number combinations to check for that naked pair
            for naked_cands in naked_combinations:
                naked_list = []     
                remove_list = []    

                for pos in list(group):
                    # naked pairs only contain numbers in the combination
                    if self.grid[pos[0]][pos[1]] == 0 and len((set(range(1,10)) - set(naked_cands)) & self.candidates[pos]) ==  0: 
                        naked_list.append(pos)
                    
                    # other squares in the group with the naked candidates should have them removed
                    elif self.grid[pos[0]][pos[1]] == 0 and len(set(naked_cands) & self.candidates[pos]) != 0:     
                        remove_list.append(pos)
                
                # if there is a naked pair and other squares where candidates should be removed
                if len(naked_list) == 2 and len(remove_list) != 0:
                    # calls found.constraint to update the board
                    found.constraint(self, naked_list, naked_cands, remove_list, method, groups.index(group))
                    return True
    return False


def naked_triples(self):             
    """Checks through the board to see if any groups contain naked triples
    - where three squares can only some combination of the three same candidate values-
    then removes these numbers as candidates for other squares in the group """

    # checks all groups- both boxes and lines (i.e. rows and columns)
    for method, groups in zip(['nt_box', 'nt_line'], [self.grid_boxes, self.grid_lines]):
        for group in groups:

            # creates a set of all candidates in the current group
            candidates_in_group = set()
            for pos in list(group):
                if self.grid[pos[0]][pos[1]] == 0:
                    candidates_in_group.update(self.candidates[pos])

            # generates all possible three-number combinations in the group
            naked_combinations = list(combinations(list(candidates_in_group), 3))

            # iterates through all three-number combinations to check for that naked triple 
            for naked_cands in naked_combinations:
                naked_list = []
                remove_list = []

                for pos in list(group):
                    # naked triples only contain numbers in the combination
                    if self.grid[pos[0]][pos[1]] == 0 and len((set(range(1,10)) - set(naked_cands)) & self.candidates[pos]) ==  0: # only contains numbers in the combination
                        naked_list.append(pos)

                    # other squares in the group with the naked candidates should have them removed
                    elif self.grid[pos[0]][pos[1]] == 0 and len(set(naked_cands) & self.candidates[pos]) != 0:     # other squares with the numbers in
                        remove_list.append(pos)

                # if there is a naked triple and other squares where candidates should be removed
                if len(naked_list) == 3 and len(remove_list) != 0:
                    # calls found.constraint to update the board
                    found.constraint(self, naked_list, naked_cands, remove_list, method, groups.index(group))
                    return True                          
    return False


def hidden_pairs(self):             
    """Checks through the board to see if any groups contain hidden pairs
    - where two candidate values only appear within two squares-
    then removes other candidates from these two squares"""

    # checks all groups- both boxes and lines (i.e. rows and columns)
    for method, groups in zip(['hp_box', 'hp_line'], [self.grid_boxes, self.grid_lines]):
        for group in groups:

            # creates a set of all candidates in the current group
            candidates_in_group = set()
            for pos in list(group):
                if self.grid[pos[0]][pos[1]] == 0:
                    candidates_in_group.update(self.candidates[pos])

            # generates all possible two-number combinations in the group
            hidden_combinations = list(combinations(list(candidates_in_group), 2))

            # iterates through all two-number combinations to check for that hidden pair 
            for hidden_cands in hidden_combinations:
                hidden_list = []
                remove_list = []

                for pos in list(group):
                    # collects all squares that contain numbers in the combination                    
                    if self.grid[pos[0]][pos[1]] == 0 and len((set(hidden_cands)) & self.candidates[pos]) !=  0:
                        hidden_list.append(pos)

                        # if there are other candidates in the hidden pair squares, they should be removed
                        if len((set(range(1,10)) - set(hidden_cands)) & self.candidates[pos]) !=  0:
                            remove_list.append(pos)
                
                # if there is a hidden pair (exactly 2 squares containing the 2 numbers) and other candidates to remove 
                if len(hidden_list) == 2 and len(remove_list) > 0:
                    # calls found.constraint to update the board
                    found.constraint(self, hidden_list, hidden_cands, remove_list, method, groups.index(group))
                    return True                   
    return False


def hidden_triples(self):             
    """Checks through the board to see if any groups contain hidden triples
    - where three candidate values only appear within three squares-
    then removes other candidates from these three squares""" 

    # checks all groups- both boxes and lines (i.e. rows and columns)
    for method, groups in zip(['ht_box', 'ht_line'], [self.grid_boxes, self.grid_lines]):
        for group in groups:

            # creates a set of all candidates in the current group
            candidates_in_group = set()
            for pos in list(group):
                if self.grid[pos[0]][pos[1]] == 0:
                    candidates_in_group.update(self.candidates[pos])

            # generates all possible three-number combinations in the group
            hidden_combinations = list(combinations(list(candidates_in_group), 3))
            for hidden_cands in hidden_combinations:
                hidden_list = []
                remove_list = []

                for pos in list(group):
                    # collects all squares that contain numbers in the combination                    
                    if self.grid[pos[0]][pos[1]] == 0 and len((set(hidden_cands)) & self.candidates[pos]) !=  0: # contains numbers in the combination
                        hidden_list.append(pos)
                        
                        # if there are other candidates in the hidden triple squares, they should be removed
                        if len((set(range(1,10)) - set(hidden_cands)) & self.candidates[pos]) !=  0: # also contains other numbers
                            remove_list.append(pos)

                # if there is a hidden triple (exactly 3 squares containing the 3 numbers) and other candidates to remove 
                if len(hidden_list) == 3 and len(remove_list) > 0:
                    # calls found.constraint to update the board
                    found.constraint(self, hidden_list, hidden_cands, remove_list, method, groups.index(group))
                    return True  
    return False


def intersection_removal(self):                
    """Checks through the board to see if any intersection removal is possible
    - where the only squares containing a candidate in one group are all also in an intersecting group-
    then removes the candidate from other squares in the intersecting group""" 

    # iterates through all numbers and the positions where they could be
    for num, pos_list in self.cand_locations.items():

        # checks both boxes & intersecting lines (pointing pairs/tripes), and lines & intersecting boxes (box-line reduction)
        for method, main_groups, intersecting_groups in zip(['ir_point', 'ir_box_line'],[self.grid_boxes, self.grid_lines], [self.grid_lines, self.grid_boxes]):
            for main_group in main_groups:

                # finds the positions in the current main group where 'num' could be
                pos_in_main = main_group & pos_list

                # if there are only 2 or 3 positions
                if len(pos_in_main) == 2 or len(pos_in_main) == 3:

                    # check if all of the positions are in any of the intersecting groups
                    for intersecting_group in intersecting_groups:
                        if intersecting_group.issuperset(pos_in_main):

                            # finds the positions in the intersecting group where 'num' could be
                            pos_in_intersecting = intersecting_group & pos_list

                            # 'num' can be removed as a candidate from other positions the intersecting group
                            if len(pos_in_intersecting) > len(pos_in_main):
                                remove_list = list(pos_in_intersecting - pos_in_main)
                                intersection_list = list(pos_in_main)
                                
                                # calls found.constraint to update the board
                                found.constraint(self, intersection_list, [num], remove_list, method, main_groups.index(main_group))
                                return True
    return False


def intersection_3d(self):
    """Checks through the board to see if any 3d-intersection removal is possible
    - where a number can only be placed at two positions in a line, and the intersecting lines
    at each position both share a third square- and removes the candidate from the third square"""

    # iterates through all numbers and the positions where they could be
    for num, pos_list in self.cand_locations.items():

        # checks through each line
        for line in self.grid_lines:

            # finds the positions in the line where 'num' could be
            pos_in_line = pos_list & line

            # if there are exactly 2 positions
            if len(pos_in_line) == 2:

                # finds the intersecting lines at both positions
                intersecting_lines = [other_line for other_line in self.grid_lines if len(pos_in_line & other_line) == 1]
                if len(intersecting_lines) == 2:

                    # checks if the intersecting lines share a square 
                    common = (intersecting_lines[0] & intersecting_lines[1])
                    if len(common) != 0:
                        remove_pos = common.pop()

                        # if 'num' is a candidate of the shared square it should be removed
                        if remove_pos in pos_list:
                            intersection_list = list(pos_in_line)
                            
                            # calls found.constraint to update the board
                            found.constraint(self, intersection_list, [num], [remove_pos], 'ir_3d', self.grid_lines.index(line))
                            return True
    return False