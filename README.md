# Sudoku

An Overview:  
This sudoku game is my first attempt at a project outside of online courses. The goal was to make a simple sudoku game using the pygame module, which features basic 
functionalities like a solver and a board generator. The project revolves around the usage of recursion and a backtracking algorithm, with some dabbling in OOP.



Files documentation:  
1. sudokusolver.py  
This file features a recursive backtracking algorithm that is able to solve any valid sudoku board. It is the first file created and the backbone of the project.

2. sorted_solver.py  
This file expands upon sudokusolver.py by first implementing a sorting function that sorts each empty box according to the amount of information that they possess.  
Boxes with more information will be filled first by a backtracking algorithm. The goal is to improve the efficiency of the backtracking algorithm by reducing the 
amount of potential backtracking it may do.

3. boardgenerator.py  
This file has two main portions: a board shuffler, and a sudoku board generator.   
Firstly, the board shuffler shuffles the rows and columns of a full and valid sudoku board. This creates new full boards.  
Secondly, the sudoku board generator iterates through a set number of boxes — determined by the user's preferred difficulty — and removes certain numbers. Using the 
sorted solver, it ensures that the generated board has a unique solution.

4. basesudokugame.py  
This file features a basic sudoku game with minimal functionalities like pencil marks and a static board.

5. sudokuwithsolver.py  
This file is the final sudoku game with more functionalities. It features a main menu with 3 levels of board difficulty, pencil marks, board generator, and a solver
GUI.  
  
Run sudokuwithsolver to experience the full game.
