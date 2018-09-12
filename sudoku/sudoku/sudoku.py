import numpy as np
from numpy import genfromtxt
import tkinter as tk
from tkinter import filedialog
import os
from enum import Enum
import random
import copy

class PuzzleState(Enum):
    SOLVED =    0
    UNSOLVED =  1
    INVALID =   2

VALID_SET = {1,2,3,4,5,6,7,8,9}
SUB_MATRIX_CENTERS = [(1,1), (1,4), (1,7), (4,1), (4,4), (4,7), (7,1), (7,4), (7,7)]

VALID_INDEXES = {(x,y) for x in range(9) for y in range(9)}

class PuzzleSolver:

    def __init__(self):
       self.puzzle = None
       self.solvedSet = {}
       self.unsolvedSet = {}
       self.guessList = {}
       self.oldGuessList = {}
       self.currentGuess = None
       self.solvedStateSnapshot = None
       self.unsolvedStateSnapshot = None

    def createOrRestoreSnapshot(self):
        if not self.solvedStateSnapshot:
           self.solvedStateSnapshot = copy.deepcopy(self.solvedSet)
           self.unsolvedStateSnapshot = copy.deepcopy(self.unsolvedSet)
        else:
           self.solvedSet = copy.deepcopy(self.solvedStateSnapshot)
           self.unsolvedSet = copy.deepcopy(self.unsolvedStateSnapshot)

    def updateSnapshot(self):
        self.solvedStateSnapshot = copy.deepcopy(self.solvedSet)
        self.unsolvedStateSnapshot = copy.deepcopy(self.unsolvedSet) 

    def loadPuzzle(self):
        """ load the puzzle from a file """
        root = tk.Tk().withdraw() 
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="select a csv file containing sudoku puzzle")
        if not file_path:
            exit()

        my_data = genfromtxt(file_path, delimiter=',', filling_values=0)
        self.puzzle = my_data.astype(int)
        self.initializeSolvedSet()
        print(self.puzzle)

    def loadPuzzleDebug(self):
        """ load debug variant of the puzzle """
        my_data = genfromtxt("easy2.csv", delimiter=',', filling_values=0)
        self.puzzle = my_data.astype(int)
        self.initializeSolvedSet()
        print(self.puzzle)

    def runSolver(self):     
        puzzleStatus = PuzzleState.UNSOLVED
        hasChangedSinceLastIteration = True

        while hasChangedSinceLastIteration and puzzleStatus != PuzzleState.INVALID  :
            hasChangedSinceLastIteration = False
            unsolvedCells = VALID_INDEXES.difference(self.solvedSet.keys())
            for loc in unsolvedCells:
                candidateSet = self.solveCell(self.puzzle, loc)
                optionSize = len(candidateSet)

                if optionSize == 0:
                    puzzleStatus = PuzzleState.INVALID
                    break;

                if optionSize == 1:
                    # update the solver
                    value = candidateSet.pop()
                    self.setSolvedCellValue(loc, value)
                    if loc in self.unsolvedSet.keys():
                        self.unsolvedSet.pop(loc)
                    hasChangedSinceLastIteration = True
                else:
                    self.unsolvedSet[loc] = list(candidateSet)

            if not unsolvedCells:
                puzzleStatus = PuzzleState.SOLVED
                break

            if not hasChangedSinceLastIteration:
                puzzleStatus = PuzzleState.UNSOLVED 
                break;

        if not PuzzleSolver.isPuzzleValid(self.puzzle):
            puzzleStatus = PuzzleState.INVALID

        if PuzzleSolver.isPuzzleSolved(self.puzzle):
           puzzleStatus = PuzzleState.SOLVED

        return puzzleStatus

    def updatePuzzle(self):
        self.puzzle = np.zeros((9,9), dtype=np.int)
        for key, value in self.solvedSet.items():
            self.puzzle[key[0], key[1]] = value[0]

    def applyNextGuess(self):
            self.guessList = PuzzleSolver.getGuessList(self.unsolvedSet)
            if self.currentGuess is not None:
                self.guessList.remove(self.currentGuess)
                      
            guess = random.choice(self.guessList)
            cell = guess[0]
            guessedValue = guess[1]
            self.setSolvedCellValue(cell, guessedValue)
            print("applying guess ", end = " ")
            self.printCell(cell, guessedValue)
            self.currentGuess = guess


    def processValidGuessAlternative(self):
        """ undoes an invalid guess """
        if self.currentGuess is not None:
            guess = self.currentGuess
            cell = guess[0]
            invalidGuessValue = guess[1]
            #update unsolvedSet
            possibleValues = self.unsolvedSet[cell]
            possibleValues.remove(invalidGuessValue)

            if len(possibleValues) == 1:
                self.setSolvedCellValue(cell, possibleValues[0])
                print("***resolved guess !!! ", end = " ")
                self.printCell(cell, possibleValues[0])
                print("number of solved cells = {0}".format(len(self.solvedSet)))
            else:
                self.unsolvedSet[cell] = possibleValues

            # reset current guess and list of previous guesses
            self.currentGuess = None
            self.oldGuessList.clear()


    def setSolvedCellValue(self, cell, value):
        self.solvedSet[cell] = [value]
        self.puzzle[cell[0], cell[1]] = value
        self.unsolvedSet.pop(cell, None)

    def initializeSolvedSet(self):
        """ returns a dictionary. key = cell index, value = cell value """
        self.solvedSet =  { (x,y) : [self.puzzle[x,y]] for x in range(9) for y in range(9) if self.puzzle[x,y] > 0 }


    @staticmethod
    def getGuessList(unsolvedSet):
        """ returns a list of guesses"""
        guessList = []
        for loc in unsolvedSet:
            if len(unsolvedSet[loc]) == 2:
                for item in unsolvedSet[loc]:
                    guessList.append((loc, item))

        random.shuffle(guessList)

        for loc in unsolvedSet:
            if len(unsolvedSet[loc]) == 3:
                for item in unsolvedSet[loc]:
                    guessList.append((loc, item))

        for loc in unsolvedSet:
            if len(unsolvedSet[loc]) > 3:
                for item in unsolvedSet[loc]:
                    guessList.append((loc, item))
    
        return guessList

    @staticmethod
    def getMissingNumbers(myList):
        """ returns the set of missing sudoku numbers in the input list """
        return VALID_SET.difference(set(myList))

    @staticmethod
    def isSolvedSet(myList):
        return len(PuzzleSolver.getMissingNumbers(myList)) == 0

    @staticmethod
    def isValidSet(myList):
        """  removes 0s and then checks for duplicates in the list """
        filledSet = [x for x in myList if x != 0]
        return len(filledSet) == len(set(filledSet))

    @staticmethod
    def isPuzzleValid(puzzle):
        """ iterates through the puzzle and verifies that it is valid"""
        rows, cols = puzzle.shape
        for i in range(rows):
            if not PuzzleSolver.isValidSet(puzzle[i, :]):
                return False
        for i in range(cols):
            if not PuzzleSolver.isValidSet(puzzle[:,i]):
                return False
        for loc in SUB_MATRIX_CENTERS:
            if not PuzzleSolver.isValidSet(PuzzleSolver.getSubmatrix(puzzle, loc)):
                return False
        return True

    @staticmethod
    def isPuzzleSolved(puzzle):
        """ iterates through the puzzle and verifies that it is solved"""
        rows, cols = puzzle.shape
        for i in range(rows):
            if not PuzzleSolver.isSolvedSet(puzzle[i, :]):
                return False
        for i in range(cols):
            if not PuzzleSolver.isSolvedSet(puzzle[:,i]):
                return False
        for loc in SUB_MATRIX_CENTERS:
            if not PuzzleSolver.isSolvedSet(PuzzleSolver.getSubmatrix(puzzle, loc)):
                return False

        return True

    @staticmethod
    def getSubmatrixRange(x):  
        """ given a cell location, returns the bounds for the corresponding 3x3 submatrix """
        begin = 0
        if 0 <= x <= 2:
            begin = 0    
        if 3 <= x <= 5:
            begin = 3
        if 6 <= x <= 8:
            begin = 6
   
        return begin, begin + 3

    @staticmethod
    def getSubmatrix(puzzle, loc):
        x_begin, x_end = PuzzleSolver.getSubmatrixRange(loc[0])
        y_begin, y_end = PuzzleSolver.getSubmatrixRange(loc[1])
        sub_matrix = puzzle[x_begin:x_end, y_begin:y_end]
        return sub_matrix.ravel()
    


    @staticmethod
    def printCell(loc, value):
        print("({0}, {1}) = {2}".format(loc[0], loc[1], value))

    @staticmethod
    def solveCell(puzzle, loc):
        """ main solver algorithm for sudoku puzzle returns the
        viable candidates for a given cell"""
        # evaluate rows and columns
        rowSet = PuzzleSolver.getMissingNumbers(puzzle[loc[0], :])
        colSet = PuzzleSolver.getMissingNumbers(puzzle[:, loc[1]])
        tempSet = rowSet.intersection(colSet)
        submatrixSet = PuzzleSolver.getMissingNumbers(PuzzleSolver.getSubmatrix(puzzle, loc))
        candidateSet = tempSet.intersection(submatrixSet)
        return candidateSet


    @staticmethod
    def setCellValue(puzzle, cell, value):
        """ cell is a tuple of the x,y indexes of the 2D array. This methods updates the specifies cell in the puzzle"""
        puzzle[cell[0], cell[1]] = value


    def solve(self):
       
        while True:
            status = self.runSolver()
           
            if status == PuzzleState.SOLVED:
                print("Congratulations ! puzzle is solved !!")
                break

            if status == PuzzleState.UNSOLVED:    
                print("puzzle is in unsolved state") 
                self.createOrRestoreSnapshot()
                self.updatePuzzle()
                self.applyNextGuess()
                      
            if status == PuzzleState.INVALID:
                print("puzzle is in invalid state")
                self.createOrRestoreSnapshot()
                self.processValidGuessAlternative()
                self.updateSnapshot()
                self.updatePuzzle()
                                 
        print(self.puzzle)
        
 
def main():
    p = PuzzleSolver()
    p.loadPuzzle()
    p.solve()
  
if __name__ == "__main__":
    main()