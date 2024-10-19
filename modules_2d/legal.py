from modules_2d import error_flags

def check(self,row,col,num):
    for i in range(9):
        if (self.grid[row][i] == num) and (i != col):
            return False
        if (self.grid[i][col] == num) and (i != row):
            return False
    box_row = row - row % 3
    box_col = col - col % 3
    for i in range(box_row, box_row + 3):
        for j in range (box_col, box_col + 3):
            if (self.grid[i][j] == num) and (i != row) and (j != col):
                return False
    return True

def board_is_legal(self):
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

def board_follows_rules(self):
    for i in range(9):
        for j in range(9):
                if (self.grid[i][j] > 0) and (not check(self, i,j,self.grid[i][j])):
                    error_flags.flag(self, 2)
                    return False
    return True
