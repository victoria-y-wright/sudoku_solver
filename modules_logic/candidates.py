from collections import defaultdict

from modules_logic import legal

import __main__
if "2d" in __main__.__file__:
    from modules_gui import squares_2d as squares
else:
    from modules_gui import squares_3d as squares

def find_all(self):
    self.candidates = defaultdict(set)
    self.cand_locations = defaultdict(set)
    for pos in self.grid_all_squares:
        i, j = pos[0], pos[1]
        if self.grid[i][j] == 0:
                for num in range(1,10):
                    if legal.check(self, pos, num):
                        self.candidates[(i,j)].add(num)
                        self.cand_locations[num].add((i,j))

    # sorting squares by fewest remaining candidates
    self.candidates = {pos: cand_list for pos, cand_list in sorted(self.candidates.items(), key= lambda item: len(item[1]))}

    squares.create_candidates(self)
    self.candidates_found = True

def update(self,pos,num):
    for pos_sq, cand_list in self.candidates.items():
        for groups in [self.grid_boxes, self.grid_rows]:
            for group in groups:
                if group.issuperset({pos,pos_sq}):
                    if num in cand_list:
                        self.candidates[pos_sq].remove(num)
                        self.cand_locations[num].remove(pos_sq)
                        squares.remove_candidate(self,pos_sq,num)
                        pass
    for cand in self.candidates[pos]:
        self.cand_locations[cand].remove(pos)
    del self.candidates[pos]