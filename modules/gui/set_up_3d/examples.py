from modules.gui.set_up_3d import board_creation, puzzle_entry
from modules.gui import squares_3d

def start(self, index):
    lists(self, index)

    self.frm_example.pack_forget()
    self.frm_labels.pack_forget()

    self.faces = []
    self.faces.append(squares_3d.Face('top', (300,150), self.side_length))

    for ef_index, new_type, new_location in zip(self.existing_face_index_list, self.new_type_list, self.new_location_list):
        board_creation.new_face(self, self.faces[ef_index], new_type, new_location)

    for line in self.lines:
        self.cnv_board.delete(line)

    puzzle_entry.create_grid(self)
    puzzle_entry.add_elements(self)
    puzzle_entry.resize_centre_canvas(self)
    
    for pos, num in zip(self.pos_list, self.num_list):
        puzzle_entry.set_number(self, pos, num)

    self.puzzle_entered()

def lists(self, index):
    if index == 1:
        self.existing_face_index_list = [0, 0, 0, 1, 1, 5, 6]
        self.new_type_list = ['left', 'left', 'right', 'left', 'left', 'left', 'top']
        self.new_location_list = ['right above', 'left below', 'right below', 'left', 'right', 'below', 'below']

        self.pos_list = [(0,0), (0,5), (0,6), (1,1), (1,6), (2,0), (2,8), (3,0), (3,2), (3,7), (4,0), (4,1), (4,3), (4,5), (4,6), (4,8), (5,3), (5,7), (6,2), (6,3), (6,5), (6,7), (7,4), (7,8)]
        self.num_list = [1, 9, 3, 8, 2, 5, 4, 9, 1, 5, 2, 6, 1, 5, 9, 3, 6, 1, 4, 5, 8, 9, 6, 2]

    if index == 2:
        self.existing_face_index_list = [0, 0, 2, 2, 1, 5, 6, 6, 7]
        self.new_type_list = ['left', 'right', 'right', 'top', 'top', 'right', 'left', 'top', 'left']
        self.new_location_list = ['left below', 'right below', 'right', 'below', 'below', 'below', 'right', 'below', 'right']

        self.pos_list = [(0,5), (1,3), (1,8), (2,0), (2,2), (2,6), (3,0), (3,2), (3,3), (3,4), (3,6), (3,7), (4,1), (4,2), (4,6), (4,8), (5,3), (5,5), (5,6), (5,8), (6,5), (6,7), (6,8), (7,0), (7,3), (7,7), (8,4), (9,0), (9,2), (9,3), (9,4), (9,6), (9,7)]
        self.num_list = [7, 7, 5, 8, 9, 2, 4, 7, 5, 1, 9, 3, 9, 5, 1, 3, 1, 8, 2, 4, 9, 4, 6, 7, 4, 9, 6, 2, 4, 3, 6, 5, 1]

    if index == 3:
        self.existing_face_index_list = [0, 0, 0, 0, 4, 5, 5, 5, 7]
        self.new_type_list = ['right', 'left', 'top', 'right', 'right', 'right', 'left', 'top', 'top']
        self.new_location_list = ['left above', 'right above', 'left below', 'right below', 'right', 'above', 'right', 'below', 'above']

        self.pos_list = [(0,4), (0,8), (1,0), (1,1), (2,3), (2,8), (3,0), (3,2), (3,3), (3,4), (3,6), (3,7), (4,3), (4,7), (5,3), (5,7), (6,1), (6,2), (6,7), (7,1), (7,2), (8,2), (8,5), (8,6), (8,7), (9,1), (9,2), (9,3), (9,5), (9,7), (9,8)]
        self.num_list = [6, 7, 6, 1, 5, 9, 8, 1, 4, 7, 3, 2, 8, 4, 9, 3, 2, 7, 8, 3, 9, 1, 8, 3, 6, 6, 8, 2, 9, 7, 4]