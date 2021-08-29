# Sudoku

An Overview:  
This sudoku game is my first attempt at a project outside of online courses. The goal was to make a simple sudoku game, using the pygame module, which features extra 
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





Screenshots of the game:  


Main Menu:  
![sudokumainmenu](https://user-images.githubusercontent.com/65714641/131245718-ea57a5b5-12d1-4dfd-9c0e-a8a8822b0105.png)


Instructions page:  
![instructions](https://user-images.githubusercontent.com/65714641/131245743-36dbd7b3-c5c0-440e-b9c5-5a18d37d39e5.png)


In-game models:  
![sudokueasy](https://user-images.githubusercontent.com/65714641/131245752-fa955091-305c-454c-a2cd-5c0c6849ca93.png) (Easy)  


![sudokumedium](https://user-images.githubusercontent.com/65714641/131245909-16392f9c-64fd-45f0-8562-8a7934e04853.png) (Medium)  


![sudokuhard](https://user-images.githubusercontent.com/65714641/131245911-7c93a355-d97c-471e-aa84-595cbbbb787f.png) (Hard)  


Solving algorithm:  
![sudokusolve](https://user-images.githubusercontent.com/65714641/131245761-4db96910-7355-406f-a91b-68c06dcee3af.png)

