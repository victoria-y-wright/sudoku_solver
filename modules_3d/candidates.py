from collections import defaultdict

from modules_3d import legal, board_set_up

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

    # creating candidate boxes board
    
    self.cand_squares=[[[None]*9 for x in range(9)] for face in self.faces]
    self.shp_cand_square=[[[None]*9 for x in range(9)] for face in self.faces]
    self.lbl_cand_square=[[[None]*9 for x in range(9)] for face in self.faces]
    for pos in self.grid_all_squares:
        i, j = pos[0], pos[1]
        if self.grid[i][j] == 0:
            for num in range(1,10):
                k = num-1
                self.cand_squares[i][j][k] = board_set_up.Face(self.squares[i][j].type, self.squares[i][j].coordinates[k], self.squares[i][j].side_length/3 - 0.5)
                self.shp_cand_square[i][j][k] = self.cnv_board.create_polygon(self.cand_squares[i][j][k].vertices, fill = 'white', outline = '')

                if num in self.candidates[(i,j)]:
                    self.lbl_cand_square[i][j][k] = self.cnv_board.create_text(*self.cand_squares[i][j][k].centre, text = num, font = ('Verdana Pro', 8))
                else:
                    self.lbl_cand_square[i][j][k] = self.cnv_board.create_text(*self.cand_squares[i][j][k].centre, text = '', font = ('Verdana Pro', 8))
    
    for shp_board_line in self.shp_board_lines:
        self.cnv_board.tag_raise(shp_board_line)
    self.candidates_found = True

def remove(self,pos,num):
    self.candidates[pos].remove(num)
    self.cand_locations[num].remove(pos)
    self.cnv_board.itemconfigure(self.lbl_cand_square[pos[0]][pos[1]][num-1], text = '')

def update(self,pos,num):
    box = pos[0]

    for pos_sq, cand_list in self.candidates.items():
        i, j = pos_sq[0], pos_sq[1]
        if i == box:
            if num in cand_list:
                self.candidates[(i,j)].remove(num)
                self.cand_locations[num].remove((i,j))
                self.cnv_board.itemconfigure(self.lbl_cand_square[i][j][num-1], text = '')
        else:
            for grid_row in self.grid_rows:
                if grid_row.issuperset({pos,pos_sq}):
                    if num in cand_list:
                        self.candidates[(i,j)].remove(num)
                        self.cand_locations[num].remove((i,j))
                        self.cnv_board.itemconfigure(self.lbl_cand_square[i][j][num-1], text = '')

    for cand in self.candidates[pos]:
        self.cand_locations[cand].remove(pos)
    del self.candidates[pos]