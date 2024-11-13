"""Functions used to apply chosen constraints, in order of simple -> complicated, to a puzzle"""

from modules.logic.constraints import sole_candidates, hidden_singles, naked_pairs, naked_triples, hidden_pairs, hidden_triples, intersection_removal, intersection_3d
from modules.gui import error_flags

def create_function_list(self):
    """Creates a list of the chosen constraint functions, ordered simple -> complicated"""
    # sole candidates is always enabled
    self.function_list = [sole_candidates]

    # for remaining functions, if checkbox is ticked, add to list
    for i, function in zip(range(1, len(self.var_constr_list)), [hidden_singles, naked_pairs, naked_triples, hidden_pairs, hidden_triples, intersection_removal, intersection_3d]):
        if self.var_constr_list[i].get() == 1:
            self.function_list.append(function)


def full_solve(self):       
    """Applies chosen constraints (simple -> complicated) until the puzzle is solved,
    or until the constraints have been exhausted"""

    create_function_list(self)

    # initialising index- the position of the current constraint  
    index = 0

    # while there are constraints left to try
    while index < len(self.function_list):
        # if current constraint finds next step, go back to checking the simplest constraint
        if self.function_list[index](self):
            index = 0
        # if current constraint doesn't find next step, try the next constraint
        else:
            index += 1
    
    # puzzle if solved if there are no empty squares
    solved = lambda self: 0 not in set([x for xs in self.grid for x in xs])

    if solved(self):
        return True
    else:
        # if puzzle hasn't been solved, display error flag for needing further strategies
        error_flags.flag(self, 4)
        return False

    
def one_step(self):         
    """Applies chosen constraints (simple -> complicated) until the next step is found,
    or until constraints are exhausted"""

    create_function_list(self)

    # initialising index- the position of the current constraint 
    index = 0

    # while there are constraints left to try
    while index < len(self.function_list):
        # if current constraint finds next step, return True
        if self.function_list[index](self):
            return True
        # if current constraint doesn't find next step, try the next constraint
        else:
            index += 1

    # if next step hasn't been found, display error flag for needing further strategies
    error_flags.flag(self, 4)
    return False