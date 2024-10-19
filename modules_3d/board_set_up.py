from math import sqrt


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

def choose_face_to_add(self, event):
    for shp_face in self.shp_face:
        self.cnv_board.itemconfigure(shp_face, fill = 'white')
    
    for line in self.lines:
        self.cnv_board.delete(line)
    
    for button_shape in self.button_shapes:
        self.cnv_buttons.itemconfigure(button_shape, outline = 'black')

    item = self.cnv_board.find_withtag("current")[0]
    self.cnv_board.itemconfigure(item, fill = 'honeydew1')

    self.existing_face = self.faces[self.shp_face.index(item)]
    
    self.lbl_choose_face.pack()
    self.cnv_buttons.pack()

def choose_where_add(self, event):

    self.lbl_choose_where.pack()

    for line in self.lines:
        self.cnv_board.delete(line)

    for button_shape in self.button_shapes:
        self.cnv_buttons.itemconfigure(button_shape, outline = 'black')

    item = self.cnv_buttons.find_withtag("current")[0]
    self.cnv_buttons.itemconfigure(item, outline = 'darkseagreen3')

    self.picked_button = self.buttons[self.button_shapes.index(item)]
    self.new_type = self.picked_button.type
    
    if self.existing_face.type == self.new_type:
        indices = [0,1,2,3]
    elif (set([self.existing_face.type, self.new_type]) == set(['left', 'right'])) or self.new_type == 'left': 
        indices = [0,2]
    else:
        indices = [1,3]

    for index in indices:
        if self.existing_face.neighbours[index] == None:
            self.lines[index] = (self.cnv_board.create_line(self.existing_face.edges[index], width = 4, capstyle = 'round', activefill = 'darkseagreen3'))
            self.cnv_board.tag_bind(self.lines[index], '<Button-1>', self.line_click)

def add_new_face(self, event):
    item = self.cnv_board.find_withtag("current")[0]
    self.cnv_board.itemconfigure(item, fill = 'darkseagreen3')

    index = self.lines.index(item)

    if self.existing_face.type in set(['left', 'right']):
        if index == 0:
            self.new_location =  'left'
        elif index == 1:
            self.new_location =  'below'
        elif index == 2:
            self.new_location =  'right'
        elif index == 3:
            self.new_location =  'above'
            
    elif self.existing_face.type == 'top':
        if index == 0:
            self.new_location =  'left below'
        elif index == 1:
            self.new_location =  'right below'
        elif index == 2:
            self.new_location =  'right above'
        elif index == 3:
            self.new_location =  'left above'
            
    new_face(self, self.existing_face, self.new_type, self.new_location)

    ## reset everything
    self.cnv_board.itemconfigure(self.shp_face[self.faces.index(self.existing_face)], fill = 'white')
    self.cnv_buttons.itemconfigure(self.button_shapes[self.buttons.index(self.picked_button)], outline = 'black')
    self.lbl_choose_face.pack_forget()
    self.cnv_buttons.pack_forget()
    self.lbl_choose_where.pack_forget()
    for line in self.lines:
        self.cnv_board.delete(line)

def new_face(self, existing_face, new_type, new_location):

    side_length = self.side_length        
    existing_type = existing_face.type
    existing_centre = existing_face.centre
    
    if new_type == 'top':
        if existing_type == 'top':
            dx = -(side_length * sqrt(3)/ 2) if 'left' in new_location else (side_length * sqrt(3)/ 2)
            dy = -(side_length/2) if 'above' in new_location else (side_length/2)
        
        elif existing_type == 'left':
            dx = (side_length* sqrt(3)/ 4) if 'above' in new_location else -(side_length* sqrt(3)/ 4)
            dy = -(side_length * 3/4) if 'above' in new_location else (side_length * 3/4)

        elif existing_type == 'right':
            dx = -(side_length* sqrt(3)/ 4) if 'above' in new_location else (side_length* sqrt(3)/ 4)
            dy = -(side_length * 3/4) if 'above' in new_location else (side_length * 3/4)

        self.faces.append(Face('top', (existing_centre[0]+dx, existing_centre[1]+dy), side_length))

    elif new_type == 'left':
        if existing_type == 'top':   
            dx = (side_length* sqrt(3)/ 4) if 'above' in new_location else -(side_length* sqrt(3)/ 4)
            dy = -(side_length * 3/4) if 'above' in new_location else (side_length * 3/4)

        elif existing_type == 'left':
            if new_location in set(['above', 'below']):
                dx = 0
                dy = -side_length if new_location == 'above' else side_length
            elif new_location in set(['left', 'right']):
                dx = -(side_length * sqrt(3)/ 2) if new_location == 'left' else (side_length * sqrt(3)/ 2)
                dy = -(side_length/2) if new_location == 'left' else (side_length/2)

        elif existing_type == 'right':
            dx = -(side_length * sqrt(3)/ 2) if new_location == 'left' else (side_length * sqrt(3)/ 2)
            dy = 0
        
        self.faces.append(Face('left', (existing_centre[0]+dx, existing_centre[1]+dy), side_length))

    elif new_type == 'right':
        if existing_type == 'top':
            dx = -(side_length* sqrt(3)/ 4) if 'above' in new_location else (side_length* sqrt(3)/ 4)
            dy = -(side_length * 3/4) if 'above' in new_location else (side_length * 3/4)
        
        elif existing_type == 'left':
            dx = -(side_length * sqrt(3)/ 2) if new_location == 'left' else (side_length * sqrt(3)/ 2)
            dy = 0

        elif existing_type == 'right':
            if new_location in set(['above', 'below']):
                dx = 0
                dy = -side_length if new_location == 'above' else side_length
            elif new_location in set(['left', 'right']):
                dx = -(side_length * sqrt(3)/ 2) if new_location == 'left' else (side_length * sqrt(3)/ 2)
                dy = (side_length/2) if new_location == 'left' else -(side_length/2)
        
        self.faces.append(Face('right', (existing_centre[0]+dx, existing_centre[1]+dy), side_length))

    self.shp_face.append(self.cnv_board.create_polygon(self.faces[-1].vertices, fill = 'white', outline = 'black', activefill = 'honeydew1'))
    self.cnv_board.tag_bind(self.shp_face[-1], '<Button-1>', self.face_click)

    ## scroll canvas
    self.cnv_board.configure(scrollregion = self.cnv_board.bbox("all"))
    if self.cnv_board.find_overlapping(self.x_offset,self.y_offset, 600 + self.x_offset, self.y_offset):
        self.y_offset += 120
    if self.cnv_board.find_overlapping(self.x_offset, 500 + self.y_offset, 600 + self.x_offset, 500 + self.y_offset):
        self.y_offset -= 120
    if self.cnv_board.find_overlapping(self.x_offset,self.y_offset, self.x_offset, 500 + self.y_offset):
        self.x_offset += 80
    if self.cnv_board.find_overlapping(600 + self.x_offset,self.y_offset, 600 + self.x_offset, 500 + self.y_offset):
        self.x_offset -= 80

    ## update neighbours 
    for face in self.faces[:-1]:
        shared_edges = list(set(self.faces[-1].edges) & set(face.edges))
        if len(shared_edges) == 1:
            self.faces[-1].neighbours[self.faces[-1].edges.index(shared_edges[0])] = self.faces.index(face)
            face.neighbours[face.edges.index(shared_edges[0])] = len(self.faces) - 1

def check_3d_board_valid(self):
    for face_index in range(len(self.faces)):
        face = self.faces[face_index]
        for i in range(4):
            if face.neighbours[i] is not None:
                neighbouring_face_index =  self.faces[face_index].neighbours[i]
                neighbouring_face = self.faces[neighbouring_face_index]
                if (face.neighbours[i-2] is None) == (neighbouring_face.neighbours[neighbouring_face.neighbours.index(face_index)-2] is None):
                    self.cnv_board.itemconfigure(self.shp_face[face_index], fill = 'pink')
                    self.cnv_board.itemconfigure(self.shp_face[neighbouring_face_index], fill = 'pink')
                    return False
    return True

