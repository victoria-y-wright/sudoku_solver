# 3D Sudoku (Tredoku) Solver
***A tool to help fans of 3D Sudoku/ Tredoku (as found in the Times) improve their solving skills.***

![Board creation](<images/creating_board.gif>) ![Solving in action](<images/solving_in_action.gif>)

[Click here to skip to key information](#key-information)

## What's the point of a Sudoku solver?

On the surface, Sudoku solvers seem like a simple way to show off computing power. After all, they can provide the full solution to a Sudoku in the time a person takes to write in the first number. But as anyone who enjoys Sudokus knows, we don't fill them out just to *see* the answer- or we may as well just flick to the back of the puzzle book or wait for the next newspaper edition to arive with the solutions. The fun, and the whole point, of Sudokus is the *process* of puzzling through the logic to work out the solution for yourself. So how is a computer program written to solve Sudokus at all relevant to people who want to do the puzzles themselves?

The best Sudoku solving programs don't just spit out answers (although this is something they should do- so you can check finished puzzle, or unpick a mistake), but they assist with and improve the hand-solving experience. The ideal Sudoku solver is a tool used for help if you get stuck, making solving more fun and less frustrating, and also used to improve your skills by learning more complex solving strategies. 

<br/><br/> 

## Classic (2D) Sudoku Solver

There are countless brilliant Sudoku solving programs already out there- notable web-based resources include the [SudokuWiki solver](https://www.sudokuwiki.org/Sudoku.htm) and [Sudoku.coach](https://sudoku.coach/en/solver). When setting out to make a 3D Sudoku solver (see below), a useful first step was programming my own version of the simpler, classic 2D solver. It has a clean, simple GUI which takes in user-inputted puzzles (either typed into the grid, or pasted in as a string of 81 numbers, with empty squares as 0). The user chooses which (combination of)strategies the solver should use, and strategies are demonstrated visually as they are applied to the puzzle.  

## 3D Sudoku (Tredoku) Solver

The 3D Sudoku (or Tredoku) is a variant of the original puzzle, where the grid is 3D- represented by faces of isometric cubes- so that the traditional 9-square rows and columns cross over surfaces of different orientations and overlap in different ways. Tredoku puzzles are published weekly in the Times, and they are a fun extension to the traditional game; further variety comes from the fact that the three-dimensional boards can take many different shapes. I love doing these 3D Sudokus, but I couldn't find any solve-assisting tools like those online for classic Sudoku. 

In this project, I have created a 3D Sudoku solver with a GUI, where users can build the shape of their specific 3D board (checked for validity), enter in the starting numbers, choose which methods the program should apply, and see a visualisation of the solving process. 


# Key information

## Dependencies

No dependencies are needed outside the standard Python Library (packages/ modules used include tkinter, itertools, collections, copy and math).

## Download link

[Click here to download the repository as zipped folder.](https://github.com/victoria-y-wright/sudoku_solver/archive/refs/heads/main.zip)

<br/><br/> 

## Solving strategies

The Sudoku solver can take two differing routes in solving a puzzle, described below:

### Brute force

The first method is by brute force, filling in the board with guessed values until the rules are violated, and then backtracking and guessing a new set of values. This is done by recursion- starting with one square, we try numbers until we find one that is allowed by the sudoku rules. We then do the same for the next square, and so on. But if at any point we get to a square where none of the numbers 1-9 are allowed, we know that the numbers we've filled in are wrong, so we **backtrack**. This means we go back to the last square and change that number to a different one- if there aren't any other valid numbers for the last square, we go back another square and change that number, and so on. As well-written Sudokus only have one solution, when we get to the point where the whole puzzle has been filled in and the board follows all of the rules, we have found the solution.  

This method is fairly simple to code but no person would ever try to solve a *whole* Sudoku this way. So brute forcing a Sudoku doesn't help the user with their actual solving, but it will (generally) return a solved puzzle in the blink of an eye- useful for checking, at least. One redeeming quality is that the brute-force method provides a very interesting visualisation of recursive backtracking. The user can also play around with improving the rate of brute forcing the puzzle by finding candidates (squares with fewest candidates will be guessed first, reducing the amount of backtracking necessary).

(An interesting note is that the brute force method is susceptible to failure- in the worst-case scenario of a puzzle *specifically designed* to be the last set of numbers a brute-force solver will try, it will have to cycle through the ludicrously large set of *all* possible number combinations and can run into timeout erros.)

### Adding constraints

The solver offers users a choice of which strategies to apply; each strategy is visualised uniquely so users can follow the deductions being made. So far, the Solver covers the set of basic strategies commonly found in puzzles (full list below); the plan is to add strategies of increasing complexity in the future.    

The strategies currently added include:
- Sole candidates (by default)
- Hidden singles
- Naked pairs
- Hidden pairs
- Naked triplets
- Hidden triplets

Excellent descriptions of these Sudoku solving strategies (and many others) can be found at [SudokuWiki](https://www.sudokuwiki.org/Strategy_Families).

<br/><br/> 

## Next Steps
[] Adding intersection removal strategy (particularly common for 3D Sudokus due to their board configuration)

[] Adding a step-by-step button for adding of constraints
