from modules_3d import error_flags

def check(self,pos,num):
    box, sq = pos[0], pos[1]

    for j in range(9):
        if (self.grid[box][j] == num) and (j != sq):
            return False

    for row in self.grid_rows:
        if pos in row:
            row_list = list(row)
            for position in row_list:
                if position != pos:
                    if self.grid[position[0]][position[1]] == num:
                        return False

    return True

def board_is_legal(self):
    contains_values = False
    for pos in self.grid_all_squares:
        i, j = pos[0], pos[1]
        if self.grid[i][j] != 0:
            contains_values = True
    if not contains_values:
        error_flags.flag(self, 1)
        return False
    return True

def board_follows_rules(self):
    for pos in self.grid_all_squares:
        i, j = pos[0], pos[1]
        if (self.grid[i][j] > 0) and (not check(self,(i,j),self.grid[i][j])):
            error_flags.flag(self, 2)
            return False
    return True