# 3D Sudoku (Tredoku) Solver
***A tool to help fans of 3D Sudoku/ Tredoku (as found in the Times) improve their solving skills.***

![Board creation](<3D Sudoku Solver/images/creating_board.gif>) ![Solving in action](<3D Sudoku Solver/images/solving_in_action.gif>)

[Click here to skip to key information](#key-information)

## What's the point of a Sudoku solver?
At their simplest, Sudoku solving programs are demonstrative of the immense power of computing, outpacing even the best human solver. However, those who enjoy Sudokus recognise that their appeal lies in neither determining whether a solution exists, or in merely seeing that solution (after all, any valid Sudoku must be solvable and answers can typically be found in the next newspaper edition or the back of a puzzle book). The charm is instead found in the *process* of puzzling through the logic to uncover that solution. At their best, Sudoku solving programs are tools to assist with the hand-solving process, allowing users to check their solutions, obtain guidance when stuck and improve their understanding of more complex solving strategies. 

## Classic (2D) Sudoku Solver and 3D Sudoku (Tredoku) Solver
Many brilliant Sudoku solvers exist, but the slightly more complex (from both puzzle-solving and coding perspectives) 3D Sudoku/ Tredoku hasn't recieved this treatment. Having failed to find such a tool, I decided to create a 3D Sudoku solving program, designed to take in a user's Tredokus and visualise the application of Sudoku strategies used to find its solution.  

As the 3D version of Sudoku takes its underlying logic from the classic puzzle, programming a 2D Sudoku solver served as a useful initial step for the full project. This tool is by no means unique- impressive creations such as the [SudokuWiki solver](https://www.sudokuwiki.org/Sudoku.htm) boast highly developed GUIs and more advanced strategies- but my version of the 2D solver has been included for reference. In making it, I focused particularly on creating a clean, simple GUI which visualises the user's choice of solving strategies in an appealing and informative manner. 


# Key information
## Dependencies
Only the standard Python Library is needed to run the solvers (packages/ modules used include tkinter, itertools, collections, copy, os and math).

## Solving strategies

The Sudoku solver can take two differing routes in solving a puzzle. 
The first method is by brute force, filling in the board with by iterating through numbers and backtracking when a set of numbers is found to be wrong. This method is relatively simple to code but (taken alone) is entirely divorced from any human Sudoku-solving strategy. It is also susceptible to failure (in the worst case scenario it will have to cycle through the ludicrously large set of *all* possible number combinations), but it does provide a fun visual. 

Contrastingly, the second method mirrors the approach of a human solving a Sudoku- the intrinsic logic of the puzzle is used to constrain (or limit) the values which different squares can take. Through the application of various Sudoku strategies, possible candidates for each square are reduced until only the correct number remains; when this process has been completed across the board, the puzzle is solved. The solvers offer a choice of which strategies to apply, and the user can also choose to apply the reduction of possibilities achieved through adding constraints to improve the rate of brute force solving. 

The strategies currently added include:
- Sole candidates (by default)
- Hidden singles
- Naked pairs
- Hidden pairs
- Naked triplets
- Hidden triplets

Some strategies have yet to be implemented, including intersection removal, X-wing and Y-wing.

Excellent descriptions of Sudoku solving strategies can be found at [SudokuWiki](https://www.sudokuwiki.org/Strategy_Families).