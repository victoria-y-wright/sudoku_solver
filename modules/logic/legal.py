from modules.gui import error_flags

def check(self,pos,num):
    for groups in [self.grid_rows, self.grid_boxes]:
        for group in groups:
            if pos in group:
                for position in list(group):
                    if position != pos:
                        if self.grid[position[0]][position[1]] == num:
                            return False
    return True

def board_not_empty(self):
    for pos in self.grid_all_squares:
        i, j = pos[0], pos[1]
        if self.grid[i][j] != 0:
            return True
    return False

def board_follows_rules(self):
    for pos in self.grid_all_squares:
        i, j = pos[0], pos[1]
        if (self.grid[i][j] > 0) and (not check(self,(i,j),self.grid[i][j])):
            return False
    return True

def board_only_numbers(self):
    for i in range(9):
        for j in range(9):
            if (len(self.ent_number[i][j].get()) != 0):
                if not self.ent_number[i][j].get().isdigit():
                    return False
                elif int(self.ent_number[i][j].get()) not in range(1,10):
                    return False
    return True