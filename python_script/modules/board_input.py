from modules import error_flags
from modules import legal

def is_legal(self):
    contains_values = False
    for i in range(9):
        for j in range(9):
            if (len(self.ent_number[i][j].get()) != 0):
                contains_values = True
                if not self.ent_number[i][j].get().isdigit():
                    error_flags.flag(self, 0)
                    return False
                elif int(self.ent_number[i][j].get()) not in range(1,10):
                    error_flags.flag(self, 0)
                    return False
    if not contains_values:
        error_flags.flag(self, 1)
        return False
    return True

def follows_rules(self):
    for i in range(9):
        for j in range(9):
                if (self.grid[i][j] > 0) and (not legal.check(self, i,j,self.grid[i][j])):
                    error_flags.flag(self, 2)
                    return False
    return True
