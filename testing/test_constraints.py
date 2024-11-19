import unittest
from unittest.mock import Mock

import sys
import os
sys.path.insert(0, os.path.abspath(''))

from modules.logic import candidates, constraints, apply_constraints
from modules.gui import error_flags
from modules.gui.set_up_2d import puzzle_entry, widgets

from sudoku_solver_2d import SudokuSolver

import csv
with open('testing/test_puzzles.csv', 'r') as file:
    reader = csv.reader(file)
    test_puzzles = {row[0]:row[1] for row in reader}

def create_mock(desc):
    num_string = test_puzzles[desc]
    mock_solver = Mock(SudokuSolver)

    mock_solver.grid=[[None]*9 for x in range(9)]
    for i in range(9):
        for j in range(9):
            mock_solver.grid[i][j] = int(num_string[i*9+j])

    mock_solver.window = Mock()      
    widgets.create(mock_solver)
    error_flags.set_up(mock_solver)
    puzzle_entry.grid_creation(mock_solver)
    candidates.find_all(mock_solver)
    return mock_solver

class TestIndividualConstraints(unittest.TestCase):
    def test_sole_candidate(self):
        test_puzzle = create_mock('sc')
        self.assertTrue(constraints.sole_candidates(test_puzzle), "Sole candidate should be found")

    def test_no_sole_candidate(self):
        test_puzzle = create_mock('hs_box')
        self.assertFalse(constraints.sole_candidates(test_puzzle), "No sole candidates should be found")

    def test_hidden_single(self):
        test_puzzle = create_mock('hs_box')
        self.assertTrue(constraints.hidden_singles(test_puzzle), "Hidden single should be found")

    def test_no_hidden_single(self):
        test_puzzle = create_mock('np_box')
        self.assertFalse(constraints.hidden_singles(test_puzzle), "No hidden singles should be found")

    def test_naked_pair(self):
        test_puzzle = create_mock('np_box')
        self.assertTrue(constraints.naked_pairs(test_puzzle), "Naked pair should be found")

    def test_no_naked_pair(self):
        test_puzzle = create_mock('nt_line')
        self.assertFalse(constraints.naked_pairs(test_puzzle), "No naked pairs should be found")

    def test_naked_triple(self):
        test_puzzle = create_mock('nt_line')
        self.assertTrue(constraints.naked_triples(test_puzzle), "Naked triple should be found")

    def test_no_naked_triple(self):
        test_puzzle = create_mock('hp_box')
        self.assertFalse(constraints.naked_triples(test_puzzle), "No naked triples should be found")

    def test_hidden_pair(self):
        test_puzzle = create_mock('hp_box')
        self.assertTrue(constraints.hidden_pairs(test_puzzle), "Hidden pair should be found")

    def test_no_hidden_pair(self):
        test_puzzle = create_mock('ht_line')
        self.assertFalse(constraints.hidden_pairs(test_puzzle), "No hidden pairs should be found")

    def test_hidden_triple(self):
        test_puzzle = create_mock('ht_line')
        self.assertTrue(constraints.hidden_triples(test_puzzle), "Hidden triple should be found")

    def test_no_hidden_triple(self):
        test_puzzle = create_mock('ir_point')
        self.assertFalse(constraints.hidden_triples(test_puzzle), "No hidden triples should be found")

    def test_intersection_removal(self):
        test_puzzle = create_mock('ir_point')
        self.assertTrue(constraints.intersection_removal(test_puzzle), "Intersection removal should be found")

    def test_no_intersection_removal(self):
        test_puzzle = create_mock('y_wing')
        self.assertFalse(constraints.intersection_removal(test_puzzle), "No intersection removals should be found")

class TestOverallSolving(unittest.TestCase):
    def test_full_puzzle_all_constr(self):
        test_puzzle = create_mock('sc')
        
        for i in range(7):
            test_puzzle.var_constr_list[i].get = Mock()
            test_puzzle.var_constr_list[i].get.return_value = 1

        self.assertTrue(apply_constraints.full_solve(test_puzzle), "Puzzle should be solved with all constraints")

    def test_full_puzzle_no_constr(self):
        test_puzzle = create_mock('sc')
        
        for i in range(7):
            test_puzzle.var_constr_list[i].get = Mock()
            test_puzzle.var_constr_list[i].get.return_value = 0

        self.assertFalse(apply_constraints.full_solve(test_puzzle), "Puzzle should not be solved without any constraints")

# Run the tests
if __name__ == '__main__':
    unittest.main()
