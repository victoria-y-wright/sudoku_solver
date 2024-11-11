from math import sqrt

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
                self.cand_squares[i][j][k] = Face(self.squares[i][j].type, self.squares[i][j].coordinates[k], self.squares[i][j].side_length/3 - 0.5)
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

class Face:
    def __init__(self, type, centre, side_length):
        self.type = type
        self.centre = centre
        self.side_length = side_length
        
        if self.type == 'top':
            dx_prime = (side_length * sqrt(3)/6 , -side_length/6)
            dy_prime =  (side_length * sqrt(3)/6 , side_length/6) 
        elif self.type == 'left':
            dx_prime = (side_length * sqrt(3)/6 , side_length/6)
            dy_prime =  (0, side_length/3)
        elif self.type == 'right':
            dx_prime = (side_length * sqrt(3)/6 , -side_length/6)
            dy_prime =  (0, side_length/3)

        self.vertices = []
        
        for i,j in zip([-3/2,-3/2,+3/2,+3/2],[-3/2,+3/2,+3/2,-3/2]):
            self.vertices.extend([round(centre[0] + i*dx_prime[0] + j*dy_prime[0],2), round(centre[1] + i*dx_prime[1] + j*dy_prime[1],2)])
    
        self.edges = []
        for start, end in zip([0,2,4,6], [2,4,6,0]):
            edge_vertices = sorted([(self.vertices[start], self.vertices[start+1]), (self.vertices[end], self.vertices[end+1])], key = lambda element: (element[0], element[1]))
            self.edges.append(tuple(edge_vertices))
        
        self.coordinates = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                self.coordinates.append((centre[0] + j*dx_prime[0] + i*dy_prime[0], centre[1] + j*dx_prime[1] + i*dy_prime[1]))

        self.grid_lines = []
        for edge,d in zip([self.edges[0],self.edges[3]], [dx_prime, dy_prime]):
            for i in [1,2]:
                self.grid_lines.append(((edge[0][0] + i*d[0], edge[0][1] + i*d[1]), (edge[1][0] + i*d[0], edge[1][1] + i*d[1])))
        
        self.neighbours =  [None,None,None,None]