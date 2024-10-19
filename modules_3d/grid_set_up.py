from modules_3d import board_set_up, error_flags

def create_grid(self):
    self.grid = [[0 for x in range(9)] for i in range(len(self.faces))] ## creating the grid

    self.grid_boxes, self.grid_rows = [], []
    self.grid_all_squares = []

    for i in range(len(self.faces)):
        new_box = set()
        for j in range(9):
            new_box.add((i,j))
            self.grid_all_squares.append((i,j))
        self.grid_boxes.append(new_box)

        face = self.faces[i]
        
        # for middle faces
        if any([(face.neighbours[x] is not None) and (face.neighbours[y] is not None) for x,y in zip([0,1],[2,3])]):
            for j in range(3):
                new_row = set()
                if (face.neighbours[0] is not None) and (face.neighbours[2] is not None):
                    new_row.update([(i,3*j), (i,3*j+1), (i,3*j+2)])
                    i_nb_a, i_nb_b = face.neighbours[0], face.neighbours[2]
                    f_nb_a, f_nb_b = self.faces[i_nb_a], self.faces[i_nb_b]

                    if (f_nb_a.neighbours[0] == i) or (f_nb_a.neighbours[2] == i):
                        new_row.update([(i_nb_a,3*j), (i_nb_a,3*j+1), (i_nb_a,3*j+2)])
                    elif (f_nb_a.neighbours[1] == i) or (f_nb_a.neighbours[3] == i):
                        new_row.update([(i_nb_a,j), (i_nb_a,j+3), (i_nb_a,j+6)])

                    if (f_nb_b.neighbours[0] == i) or (f_nb_b.neighbours[2] == i):
                        new_row.update([(i_nb_b,3*j), (i_nb_b,3*j+1), (i_nb_b,3*j+2)])
                    elif (f_nb_b.neighbours[1] == i) or (f_nb_b.neighbours[3] == i):
                        new_row.update([(i_nb_b,j), (i_nb_b,j+3), (i_nb_b,j+6)])

                    self.grid_rows.append(new_row)

                new_row = set()
                if (face.neighbours[1] is not None) and (face.neighbours[3] is not None):
                    new_row.update([(i,j), (i,j+3), (i,j+6)])
                    i_nb_a, i_nb_b = face.neighbours[1], face.neighbours[3]
                    f_nb_a, f_nb_b = self.faces[i_nb_a], self.faces[i_nb_b]

                    if (f_nb_a.neighbours[0] == i) or (f_nb_a.neighbours[2] == i):
                        new_row.update([(i_nb_a,3*j), (i_nb_a,3*j+1), (i_nb_a,3*j+2)])
                    elif (f_nb_a.neighbours[1] == i) or (f_nb_a.neighbours[3] == i):
                        new_row.update([(i_nb_a,j), (i_nb_a,j+3), (i_nb_a,j+6)])

                    if (f_nb_b.neighbours[0] == i) or (f_nb_b.neighbours[2] == i):
                        new_row.update([(i_nb_b,3*j), (i_nb_b,3*j+1), (i_nb_b,3*j+2)])
                    elif (f_nb_b.neighbours[1] == i) or (f_nb_b.neighbours[3] == i):
                        new_row.update([(i_nb_b,j), (i_nb_b,j+3), (i_nb_b,j+6)])

                    self.grid_rows.append(new_row)



def add_elements(self):
    self.btn_start_board.pack_forget()
    self.cnv_board.configure(closeenough=1)
    self.squares = [[None]*9 for face in self.faces]
    self.shp_square = [[None]*9 for face in self.faces]
    
    self.lbl_square = [[None]*9 for face in self.faces]

    for i in range(len(self.faces)):
        face = self.faces[i]
        for j in range(9):
            self.squares[i][j] = board_set_up.Face(face.type, face.coordinates[j], face.side_length/3)
            self.shp_square[i][j] = self.cnv_board.create_polygon(self.squares[i][j].vertices, fill = 'white', outline = '', activefill = 'honeydew1')
            self.cnv_board.tag_bind(self.shp_square[i][j], '<Button-1>', self.square_click)
            self.lbl_square[i][j] = self.cnv_board.create_text(*face.coordinates[j], text = '', font = ('TkDefaultFont', 25, 'bold'))        
            self.cnv_board.tag_bind(self.lbl_square[i][j], '<Button-1>', self.square_click)

    for shp_face in self.shp_face:
        self.cnv_board.delete(shp_face)

    self.shp_board_lines = []
    for face in self.faces:
        for i in range(4):
            self.shp_board_lines.append(self.cnv_board.create_line(face.edges[i], width = 2, capstyle = 'round'))
            self.shp_board_lines.append(self.cnv_board.create_line(face.grid_lines[i], width = 1, capstyle = 'round'))
    
    self.lbl_entry_click.pack()
    self.btn_start.pack(pady=30, side = 'bottom')
    
def input_number(self):
    
    for pos in self.grid_all_squares:
        i, j = pos[0], pos[1]
        self.cnv_board.itemconfigure(self.shp_square[i][j], fill = 'white')

    item = self.cnv_board.find_withtag("current")[0]

    self.current_pos = [(box, square.index(item)) for box,square in enumerate(self.shp_square) if item in square]
    if len(self.current_pos) == 0:
        self.current_pos = [(box, square.index(item)) for box,square in enumerate(self.lbl_square) if item in square][0]
    else:
        self.current_pos = self.current_pos[0]
    
    i, j = self.current_pos[0], self.current_pos[1]

    self.cnv_board.itemconfigure(self.shp_square[i][j], fill = 'honeydew1')

    self.frm_entry.pack()
    if self.grid[i][j] != 0:
        self.entry_text.set(self.grid[i][j])
        self.ent_entry.icursor(1)
    else:
        self.entry_text.set('')

    self.ent_entry.focus()

def enter_number(self):
    i, j = self.current_pos[0], self.current_pos[1]

    error_flags.reset(self)
    entry = self.ent_entry.get()
    if len(entry) != 0:
        if entry.isdigit():
            if int(entry) in range(1,10):
                set_number(self,(i,j), int(entry))
                self.frm_entry.pack_forget()
            else:
                error_flags.flag(self,0)
        else:
            error_flags.flag(self,0)
    else: 
        self.cnv_board.itemconfigure(self.lbl_square[i][j], text = '')
        self.grid[i][j] = 0

def set_number(self, pos, num):
    i,j = pos[0], pos[1]
    self.cnv_board.itemconfigure(self.lbl_square[i][j], text = num)
    self.grid[i][j] = int(num)
    self.cnv_board.itemconfigure(self.shp_square[i][j], fill = 'white')
    self.entry_text.set('')
