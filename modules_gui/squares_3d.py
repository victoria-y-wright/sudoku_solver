from modules_3d import board_set_up

def set_value(self, pos, value): # used in brute_force
    if value == 0:
        self.cnv_board.itemconfigure(self.lbl_square[pos[0]][pos[1]], text = '')
    else:
        self.cnv_board.itemconfigure(self.lbl_square[pos[0]][pos[1]], text = value)

def create_candidates(self): # used in candidates
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

def remove_candidate(self,pos,num): # used in candidates
    self.cnv_board.itemconfigure(self.lbl_cand_square[pos[0]][pos[1]][num-1], text = '')

def hide_candidates(self, pos): # used in brute_force
    for k in range(9):
        self.cnv_board.itemconfigure(self.lbl_cand_square[pos[0]][pos[1]][k], state = 'hidden')
        self.cnv_board.itemconfigure(self.shp_cand_square[pos[0]][pos[1]][k], state = 'hidden')

def show_candidates(self, pos): # used in brute_force
    for k in range(9):
        self.cnv_board.itemconfigure(self.lbl_cand_square[pos[0]][pos[1]][k], state = 'normal')
        self.cnv_board.itemconfigure(self.shp_cand_square[pos[0]][pos[1]][k], state = 'normal')

def change_cand_colour(self, pos, cand, colour): # used in visualisation
    self.cnv_board.itemconfigure(self.shp_cand_square[pos[0]][pos[1]][cand-1], fill = colour)

def change_square_colour(self, pos, colour): # used in visualisation
    self.cnv_board.itemconfigure(self.shp_square[pos[0]][pos[1]], fill = colour)
