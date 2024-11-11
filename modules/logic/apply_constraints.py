from modules.logic.constraints import sole_candidates, hidden_singles, naked_pairs, naked_triples, hidden_pairs, hidden_triples
from modules.gui import error_flags

def create_function_list(self):
    self.function_list = [sole_candidates]
    for i, function in zip(range(1, len(self.var_constr_list)), [hidden_singles, naked_pairs, naked_triples, hidden_pairs, hidden_triples]):
        if self.var_constr_list[i].get() == 1:
            self.function_list.append(function)

def full_solve(self):       # applying constraints in order of simple -> complicated until puzzle is solved, or can't progress
    create_function_list(self)

    index = 0
    while index < len(self.function_list):
        if self.function_list[index](self):
            index = 0
        else:
            index += 1
    
    solved = lambda self: 0 not in set([x for xs in self.grid for x in xs])
    if solved(self):
        return True
    else:
        error_flags.flag(self, 4)
        return False

    
def one_step(self):         # trying constraints until next step is found
    create_function_list(self)

    index = 0
    while index < len(self.function_list):
        if self.function_list[index](self):
            return True
        else:
            index += 1
    
    error_flags.flag(self, 4)
    return False