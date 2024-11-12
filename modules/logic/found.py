from modules.logic import candidates
from modules.gui import visualisation

def value(self, pos, num, method, group_index=-1):
    self.grid[pos[0]][pos[1]] = num  
    visualisation.value(self, pos, method, group_index)
    candidates.update(self, pos, num)

def constraint(self, pos_list, cand_list, remove_list, method, group_index):
    visualisation.constraint(self, pos_list, cand_list, remove_list, method, group_index)
    if any([method[:2] == 'np', method[:2] == 'nt']):
        for cand in cand_list:
            for pos in remove_list:
                if cand in self.candidates[pos]:
                    self.candidates[pos].remove(cand)
                    self.cand_locations[cand].remove(pos)
    if any([method[:2] == 'hp', method[:2] == 'ht']):
        for pos in remove_list:
            for num in range(1,10):
                if num not in cand_list and num in self.candidates[pos]:
                    self.candidates[pos].remove(num)
                    self.cand_locations[num].remove(pos)
    if method[:2] == 'ir':
        num = cand_list[0]
        for pos in remove_list:
            if num in self.candidates[pos]:
                self.candidates[pos].remove(num)
                self.cand_locations[num].remove(pos)

