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