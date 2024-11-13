"""Functions to handle the response when a value or constraint is found"""

from modules.logic import candidates
from modules.gui import visualisation

def value(self, pos, num, method, group_index=-1):
    """Updates board with 'num' at 'pos' and calls candidates.update, calls visualisation"""

    self.grid[pos[0]][pos[1]] = num  

    visualisation.value(self, pos, method, group_index)
    candidates.update(self, pos, num)


def constraint(self, pos_list, cand_list, remove_list, method, group_index):
    """Calls visualisation, removes candidates from the positions in 'remove_list' """

    visualisation.constraint(self, pos_list, cand_list, remove_list, method, group_index)

    # naked pairs/ naked triples
    if any([method[:2] == 'np', method[:2] == 'nt']):
        for cand in cand_list:
            for pos in remove_list:
                if cand in self.candidates[pos]:
                    self.candidates[pos].remove(cand)
                    self.cand_locations[cand].remove(pos)

    # hidden pairs/ hidden triples
    if any([method[:2] == 'hp', method[:2] == 'ht']):
        for pos in remove_list:
            for num in range(1,10):
                if num not in cand_list and num in self.candidates[pos]:
                    self.candidates[pos].remove(num)
                    self.cand_locations[num].remove(pos)

    # (3d) intersection removal
    if method[:2] == 'ir':
        num = cand_list[0]
        for pos in remove_list:
            if num in self.candidates[pos]:
                self.candidates[pos].remove(num)
                self.cand_locations[num].remove(pos)

