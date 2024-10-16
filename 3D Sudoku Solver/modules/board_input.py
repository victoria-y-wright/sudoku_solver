from modules import error_flags
from modules import legal

def is_legal(self):
    contains_values = False
    for pos in self.grid_all_squares:
        i, j = pos[0], pos[1]
        if self.grid[i][j] != 0:
            contains_values = True
    if not contains_values:
        error_flags.flag(self, 1)
        return False
    return True

def follows_rules(self):
    for pos in self.grid_all_squares:
        i, j = pos[0], pos[1]
        if (self.grid[i][j] > 0) and (not legal.check(self,(i,j),self.grid[i][j])):
            error_flags.flag(self, 2)
            return False
    return True