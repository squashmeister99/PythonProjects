import numpy as np
from numpy import genfromtxt
import tkinter as tk
from tkinter import filedialog
import os
from enum import Enum
import random
import copy


class PuzzleState(Enum):
    SOLVED = 0
    UNSOLVED = 1
    INVALID = 2


VALID_SET = {1, 2, 3, 4, 5, 6, 7, 8, 9}
SUB_MATRIX_CENTERS = [(1, 1), (1, 4), (1, 7), (4, 1), (4, 4), (4, 7),
                      (7, 1), (7, 4), (7, 7)]
VALID_INDEXES = {(x, y) for x in range(9) for y in range(9)}


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


def getMissingNumbers(myList):
    """ returns the set of missing sudoku numbers in the input list """
    return VALID_SET.difference(set(myList))


def isSolvedSet(myList):
    return len(getMissingNumbers(myList)) == 0


def isValidSet(myList):
    """  removes 0s and then checks for duplicates in the list """
    filledSet = [x for x in myList if x != 0]
    return len(filledSet) == len(set(filledSet))


def isPuzzleValid(puzzle):
    """ iterates through the puzzle and verifies that it is valid"""
    rows, cols = puzzle.shape
    for i in range(rows):
        if not isValidSet(puzzle[i, :]):
            return False
    for i in range(cols):
        if not isValidSet(puzzle[:, i]):
            return False
    for loc in SUB_MATRIX_CENTERS:
        if not isValidSet(getSubmatrix(puzzle, loc)):
            return False
    return True


def isPuzzleSolved(puzzle):
    """ iterates through the puzzle and verifies that it is solved"""
    rows, cols = puzzle.shape
    for i in range(rows):
        if not isSolvedSet(puzzle[i, :]):
            return False
    for i in range(cols):
        if not isSolvedSet(puzzle[:, i]):
            return False
    for loc in SUB_MATRIX_CENTERS:
        if not isSolvedSet(getSubmatrix(puzzle, loc)):
            return False

    return True


def getSubmatrixRange(x):
    """ given a cell location, returns the bounds for the
        corresponding 3x3 submatrix """
    begin = 0
    if 0 <= x <= 2:
        begin = 0
    if 3 <= x <= 5:
        begin = 3
    if 6 <= x <= 8:
        begin = 6
    return begin, begin + 3


def getSubmatrix(puzzle, loc):
    x_begin, x_end = getSubmatrixRange(loc[0])
    y_begin, y_end = getSubmatrixRange(loc[1])
    sub_matrix = puzzle[x_begin:x_end, y_begin:y_end]
    return sub_matrix.ravel()


def printCell(loc, value):
    print("({0}, {1}) = {2}".format(loc[0], loc[1], value))


def solveCell(puzzle, loc):
    """ main solver algorithm for sudoku puzzle returns the
        viable candidates for a given cell"""
    # evaluate rows and columns
    rowSet = getMissingNumbers(puzzle[loc[0], :])
    colSet = getMissingNumbers(puzzle[:, loc[1]])
    tempSet = rowSet.intersection(colSet)
    submatrixSet = getMissingNumbers(getSubmatrix(puzzle, loc))
    candidateSet = tempSet.intersection(submatrixSet)
    return candidateSet


def setCellValue(puzzle, cell, value):
    """ cell is a tuple of the x,y indexes of the 2D array.
        This methods updates the specifies cell in the puzzle"""
    puzzle[cell[0], cell[1]] = value


class PuzzleSolver:

    def __init__(self):
        self.puzzle = None
        self.solvedSet = {}
        self.unsolvedSet = {}
        self.guessList = {}
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
        tk.Tk().withdraw()
        file_path = filedialog.askopenfilename(
                            initialdir=os.getcwd(),
                            title="select a csv file containing sudoku puzzle")
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
        hasChanged = True

        while hasChanged and puzzleStatus != PuzzleState.INVALID:
            hasChanged = False
            unsolvedCells = VALID_INDEXES.difference(self.solvedSet.keys())
            for loc in unsolvedCells:
                candidateSet = solveCell(self.puzzle, loc)
                optionSize = len(candidateSet)

                if optionSize == 0:
                    puzzleStatus = PuzzleState.INVALID
                    break

                if optionSize == 1:
                    # update the solver
                    value = candidateSet.pop()
                    self.setSolvedCellValue(loc, value)
                    if loc in self.unsolvedSet.keys():
                        self.unsolvedSet.pop(loc)
                    hasChanged = True
                else:
                    self.unsolvedSet[loc] = list(candidateSet)

            if not unsolvedCells:
                puzzleStatus = PuzzleState.SOLVED
                break

            if not hasChanged:
                puzzleStatus = PuzzleState.UNSOLVED
                break

        if not isPuzzleValid(self.puzzle):
            puzzleStatus = PuzzleState.INVALID

        if isPuzzleSolved(self.puzzle):
            puzzleStatus = PuzzleState.SOLVED
        return puzzleStatus

    def updatePuzzle(self):
        self.puzzle = np.zeros((9, 9), dtype=np.int)
        for key, value in self.solvedSet.items():
            self.puzzle[key[0], key[1]] = value[0]

    def applyNextGuess(self):
            self.guessList = getGuessList(self.unsolvedSet)
            if self.currentGuess is not None:
                self.guessList.remove(self.currentGuess)

            guess = random.choice(self.guessList)
            cell = guess[0]
            guessedValue = guess[1]
            self.setSolvedCellValue(cell, guessedValue)
            print("applying guess ", end=" ")
            printCell(cell, guessedValue)
            self.currentGuess = guess

    def processValidGuessAlternative(self):
        """ undoes an invalid guess """
        if self.currentGuess is not None:
            guess = self.currentGuess
            cell = guess[0]
            invalidGuessValue = guess[1]
            # update unsolvedSet
            possibleValues = self.unsolvedSet[cell]
            possibleValues.remove(invalidGuessValue)

            if len(possibleValues) == 1:
                self.setSolvedCellValue(cell, possibleValues[0])
                print("***resolved guess !!! ", end=" ")
                self.printCell(cell, possibleValues[0])
                print("# of solved cells= {0}".format(len(self.solvedSet)))
            else:
                self.unsolvedSet[cell] = possibleValues

            # reset current guess and list of previous guesses
            self.currentGuess = None

    def setSolvedCellValue(self, cell, value):
        self.solvedSet[cell] = [value]
        self.puzzle[cell[0], cell[1]] = value
        self.unsolvedSet.pop(cell, None)

    def initializeSolvedSet(self):
        """ returns a dictionary. key = cell index, value = cell value """
<<<<<<< HEAD
        self.solvedSet = {(x, y):
                          [self.puzzle[x, y]]
                          for x in range(9)
                          for y in range(9)
                          if self.puzzle[x, y] > 0}
=======
        self.solvedSet =  { (x,y) : [self.puzzle[x,y]] for x in range(9) for y in range(9) if self.puzzle[x,y] > 0 }


    @staticmethod
    def getGuessList(unsolvedSet):
        """ returns a list of guesses"""
        guessList = []
        print(unsolvedSet)
        for loc in unsolvedSet:
            if len(unsolvedSet[loc]) == 2:
                guessList.append((loc, list(unsolvedSet[loc])))

        random.shuffle(guessList)

        for loc in unsolvedSet:
            if len(unsolvedSet[loc]) == 3:
                guessList.append((loc, list(unsolvedSet[loc])))

        for loc in unsolvedSet:
            if len(unsolvedSet[loc]) > 3:
                guessList.append((loc, list(unsolvedSet[loc])))
    
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
    
<<<<<<< HEAD
def getSolvedSet(puzzle):
    """ returns a dictionary. key = cell index, value = cell value """
    return { (x,y) : [puzzle[x,y]] for x in range(9) for y in range(9) if puzzle[x,y] > 0 }


def printCell(loc, value):
    print("({0}, {1}) = {2}".format(loc[0], loc[1], value))


def solveCell(puzzle, loc):
    """ main solver algorithm for sudoku puzzle returns the
    viable candidates for a given cell"""
    # evaluate rows and columns
    rowSet = getMissingNumbers(puzzle[loc[0], :])
    colSet = getMissingNumbers(puzzle[:, loc[1]])
    tempSet = rowSet.intersection(colSet)
    submatrixSet = getMissingNumbers(getSubmatrix(puzzle, loc))
    candidateSet = tempSet.intersection(submatrixSet)
    return candidateSet

def runSolver(puzzle, solvedSet):
    unsolvedSet = {}
    unsolvedCells = VALID_INDEXES.difference(solvedSet.keys())
    puzzleStatus = PuzzleState.UNSOLVED

    while len(solvedSet) != puzzle.size and puzzleStatus != PuzzleState.INVALID  :
        oldSize = len(unsolvedCells)
        for loc in unsolvedCells:
            candidateSet = solveCell(puzzle, loc)

            if len(candidateSet) == 0:
                puzzleStatus = PuzzleState.INVALID
                break;

            if len(candidateSet) == 1:
                value = candidateSet.pop()             
                # move the current cell to solved and update the puzzle
                solvedSet[loc] = [value]
                setCellValue(puzzle, loc, value)
                if loc in unsolvedSet:
                    unsolvedSet.pop(loc)

            else:
                unsolvedSet[loc] = candidateSet

        unsolvedCells = VALID_INDEXES.difference(solvedSet.keys())

        if(len(unsolvedCells) == oldSize):
            puzzleStatus = PuzzleState.UNSOLVED
            print("solved state size = {0}".format(len(solvedSet)))
            break;

    if isPuzzleSolved(puzzle):
       puzzleStatus = PuzzleState.SOLVED

    if not isPuzzleValid(puzzle):
       puzzleStatus = PuzzleState.INVALID

    print(puzzle)
    print("solved size = {0}, unsolved cells = {1}, unsolved set = {2}".format(len(solvedSet), len(unsolvedCells), len(unsolvedSet)))
    #assert(len(unsolvedCells) == len(unsolvedSet))
    return puzzleStatus, unsolvedSet

def getGuessList(unsolvedSet):
    """ returns a list of guesses"""
    guessList = []
    for loc in unsolvedSet:
        if len(unsolvedSet[loc]) == 2:
            guessList.append((loc, list(unsolvedSet[loc])))
    shuffle(guessList)

    for loc in unsolvedSet:
        if len(unsolvedSet[loc]) == 3:
            guessList.append((loc, list(unsolvedSet[loc])))

    for loc in unsolvedSet:
        if len(unsolvedSet[loc]) > 3:
            guessList.append((loc, list(unsolvedSet[loc])))

    print("guess list size = {0}".format(len(guessList)))
    return guessList

def setCellValue(puzzle, cell, value):
    """ cell is a tuple of the x,y indexes of the 2D array. This methods updates the specifies cell in the puzzle"""
    puzzle[cell[0], cell[1]] = value

def saveOrRestoreSnapshot(solvedSet, solver_snapshot):
    if solver_snapshot is None:
        solver_snapshot = solvedSet.copy()
    else:
        solvedSet = solver_snapshot.copy()


def updateSnapshot(solvedSet, solvedSet_snapshot):
    solvedSet_snapshot = solvedSet.copy()

def applyGuess(puzzle, solvedSet,  guessList):
    """ applies the first guess from the guess list """
    guess = guessList[0]
    cell = guess[0]
    possibleValues = guess[1]
    guessedValue = possibleValues[0]
    setCellValue(puzzle, cell, guessedValue)
    solvedSet[cell] = [guessedValue]

def getValidGuessAlternative(guessList):
    """ undoes an invalid guess """
    guess = guessList[0]
    cell = guess[0]
    possibleValuesList = guess[1]
    # remove the first guess since it is invalid, and return the rest
    possibleValuesList.pop(0)
    return cell, possibleValuesList
        
def updatePuzzle(puzzle, solver):
    puzzle = np.zeros((9,9), dtype=np.int)
    for item in solver.keys():
        loc = item
        value = solver[item]
        setCellValue(puzzle, loc, value[0])
    
   
def main():
    puzzle = loadPuzzle()
    solvedSet = getSolvedSet(puzzle)
    guessList = []
    solver_snapshot = None
=======

>>>>>>> 4f1a7352860864d2dc978ce7f588107ef2f40362

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

>>>>>>> 3c6b6af7521bb19fc0ec4c6225bc0b58ef635160

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
<<<<<<< HEAD


=======
        
<<<<<<< HEAD
        if status == PuzzleState.SOLVED:
            print("Congratulations ! puzzle is solved !!")
            break

        if status == PuzzleState.UNSOLVED:    
            # build a list of viable guesses
            # save a snapshot
            # update the puzzle from the snapshot state
            # apply the guess
            print("puzzle is in unsolved state")
            guessList = getGuessList(unsolvedSet)
            saveOrRestoreSnapshot(solvedSet, solver_snapshot)
            updatePuzzle(puzzle, solvedSet)
            applyGuess(puzzle, solvedSet, guessList)
            
        if status == PuzzleState.INVALID:
            print("puzzle is in invalid state")
            # restore snapsot
            # get correct guess
            # apply guess
            # update snapshot
            saveOrRestoreSnapshot(solvedSet, solver_snapshot)
            cell, validGuesses = getValidGuessAlternative(guessList)
            if len(validGuesses) == 1:
                # we can set the cell
                value = validGuesses[0]
                solvedSet[cell] = [value]
                print("resolved guess", end = " ")
                print(cell, value)
                 
            updatePuzzle(puzzle, solvedSet)
            updateSnapshot(solvedSet, solver_snapshot)
            
    print(puzzle)
    
=======
 
>>>>>>> 3c6b6af7521bb19fc0ec4c6225bc0b58ef635160
def main():
    p = PuzzleSolver()
    p.loadPuzzle()
    p.solve()
<<<<<<< HEAD


=======
  
>>>>>>> 4f1a7352860864d2dc978ce7f588107ef2f40362
>>>>>>> 3c6b6af7521bb19fc0ec4c6225bc0b58ef635160
if __name__ == "__main__":
    main()
