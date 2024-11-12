import unittest
from unittest.mock import Mock

import sys
import os
sys.path.insert(0, os.path.abspath(''))

from modules.logic import legal
from modules.gui.set_up_2d.puzzle_entry import grid_creation

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
    grid_creation(mock_solver)
    return mock_solver

class TestPuzzleValidation(unittest.TestCase):
    def test_board_not_empty(self):
        test_puzzle = create_mock('sc')
        self.assertTrue(legal.board_not_empty(test_puzzle), "Non-empty puzzle input should pass.")

    def test_board_empty(self):
        test_puzzle = create_mock('zeroes')
        self.assertFalse(legal.board_not_empty(test_puzzle), "Empty puzzle input should fail.")

    def test_board_follows_rules(self):
        test_puzzle = create_mock('sc')
        self.assertTrue(legal.board_follows_rules(test_puzzle), "Legal puzzle input should pass.")

    def test_board_repeated_row(self):
        test_puzzle = create_mock('same_row')
        self.assertFalse(legal.board_follows_rules(test_puzzle), "Illegal (repetition in row) puzzle input should fail.")
    
    def test_board_repeated_column(self):
        test_puzzle = create_mock('same_column')
        self.assertFalse(legal.board_follows_rules(test_puzzle), "Illegal (repetition in column) puzzle input should fail.")

    def test_board_repeated_box(self):
        test_puzzle = create_mock('same_box')
        self.assertFalse(legal.board_follows_rules(test_puzzle), "Illegal (repetition in box) puzzle input should fail.")

# Run the tests
if __name__ == '__main__':
    unittest.main()

