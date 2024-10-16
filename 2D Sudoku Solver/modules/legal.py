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