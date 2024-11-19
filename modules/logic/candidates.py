"""Functions that handle the creation and updating of candidates for empty squares"""

from collections import defaultdict

from modules.logic import legal

import __main__
if "3d" in __main__.__file__:
    from modules.gui import squares_3d as squares
else:
    from modules.gui import squares_2d as squares

def find_all(self):
    """
    Finds and stores the possible (candidate) numbers for every unfilled square

    Results are stored as two dictionaries:
    - 'self.candidates': maps each unfilled square to a set of valid candidate numbers
    - 'self.cand_locations': maps each number to a set of positions where it can be legally placed
    """
    self.candidates = defaultdict(set)
    self.cand_locations = defaultdict(set)

    # iterate through every square in the grid
    for pos in self.grid_all_squares:
        # empty squares have candidates
        if self.grid[pos[0]][pos[1]] == 0:
                # determine legal numbers 1-9 for the current square and update dictionaries
                for num in range(1,10):
                    if legal.check(self, pos, num):
                        self.candidates[pos].add(num)
                        self.cand_locations[num].add(pos)

    # sort squares by fewest remaining candidates, so solving can prioritise easier squares 
    self.candidates = {pos: cand_list for pos, cand_list in sorted(self.candidates.items(), key= lambda item: len(item[1]))}

    # update visuals to show candidates
    squares.create_candidates(self)
    self.candidates_found = True

def update(self,pos,num):
    """
    Updates the candidate dictionaries when 'pos' is found as 'num'
    """
    # iterate over all unfilled squares
    for pos_sq, cand_list in self.candidates.items():
        # check if the current unfilled square shares a group with 'pos'
        for groups in [self.grid_boxes, self.grid_lines]:
            for group in groups:
                if group.issuperset({pos,pos_sq}):
                    # if 'num' was a potential candidate for the unfilled square, remove it
                    if num in cand_list:
                        self.candidates[pos_sq].remove(num)
                        self.cand_locations[num].remove(pos_sq)
                        squares.remove_candidate(self,pos_sq,num)
    
    # remove all candidate information for 'pos', as it has been found
    for cand in self.candidates[pos]:
        self.cand_locations[cand].remove(pos)
    del self.candidates[pos]