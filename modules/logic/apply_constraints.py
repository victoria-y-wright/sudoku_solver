from modules.logic.constraints import sole_candidates, hidden_singles, naked_pairs, naked_triples, hidden_pairs, hidden_triples

# applying constraints recursively 
def until_solved(self):
    self.function_list = [None, sole_candidates]
    for i, function in zip(range(1, len(self.var_constr_list)), [hidden_singles, naked_pairs, naked_triples, hidden_pairs, hidden_triples]):
        if self.var_constr_list[i].get() == 1:
            self.function_list.append(function)

    def create_func_loop(index):
        def func_loop(self):
            loop, last_change = 0, 0
            while last_change == loop:
                loop += 1

                if self.function_list[index-1]:
                    self.method_list[index-2](self)

                if self.function_list[index](self):
                    last_change = loop
        return func_loop

    self.method_list = [create_func_loop(index) for index in range(1,len(self.function_list))]
    self.method_list.append(None)

    solved = lambda self: 0 not in set([x for xs in self.grid for x in xs])

    def solve(self, index):
        self.method_list[index](self)

        if solved(self):
            return True

        elif self.method_list[index+1]:
            return solve(self,index+1)

        else:
            return False
        
    return solve(self,0)
