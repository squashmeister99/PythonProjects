"""sudoku puzzle solver."""
import numpy as np
from numpy import genfromtxt
import tkinter as tk
from tkinter import filedialog
import os
from enum import Enum
import random
import copy


class PuzzleState(Enum):
    """Possible states of sudoku puzzle."""

    SOLVED = 0
    UNSOLVED = 1
    INVALID = 2


VALID_SET = {x for x in range(1, 10)}
SUB_MATRIX_CENTERS = [(1, 1), (1, 4), (1, 7), (4, 1), (4, 4), (4, 7),
                      (7, 1), (7, 4), (7, 7)]
VALID_INDEXES = {(x, y) for x in range(9) for y in range(9)}
IS_MAIN_PROGRAM = False
MAX_LOOPS = 300


def getGuessList(unsolvedDict):
    """Return a list of guesses."""
    guessList = []
    for loc in unsolvedDict:
        if len(unsolvedDict[loc]) == 2:
            for item in unsolvedDict[loc]:
                guessList.append((loc, item))
    random.shuffle(guessList)

    for loc in unsolvedDict:
        if len(unsolvedDict[loc]) == 3:
            for item in unsolvedDict[loc]:
                guessList.append((loc, item))

    for loc in unsolvedDict:
        if len(unsolvedDict[loc]) > 3:
            for item in unsolvedDict[loc]:
                guessList.append((loc, item))

    return guessList


def getMissingNumbers(myList):
    """Return the set of missing sudoku numbers in the input list."""
    return VALID_SET.difference(set(myList))


def getSubmatrixRange(x):
    """Return associated 3x3 submatrix range."""
    begin = 0
    if 0 <= x <= 2:
        begin = 0
    if 3 <= x <= 5:
        begin = 3
    if 6 <= x <= 8:
        begin = 6
    return begin, begin + 3


def getSubmatrix(puzzle, loc):
    """Return associated 3x3 submatrix for the cell."""
    x_begin, x_end = getSubmatrixRange(loc[0])
    y_begin, y_end = getSubmatrixRange(loc[1])
    return puzzle[x_begin:x_end, y_begin:y_end].ravel()


def printCell(loc, value):
    """Print current cell value."""
    if IS_MAIN_PROGRAM:
        print("({0}, {1}) = {2}".format(loc[0], loc[1], value))


def solveCell(puzzle, loc):
    """Find viable candidates for a given cell."""
    rowSet = getMissingNumbers(puzzle[loc[0], :])
    colSet = getMissingNumbers(puzzle[:, loc[1]])
    submatrixSet = getMissingNumbers(getSubmatrix(puzzle, loc))
    return rowSet.intersection(colSet).intersection(submatrixSet)


def setCellValue(puzzle, cell, value):
    """Set cell value."""
    puzzle[cell[0], cell[1]] = value


class PuzzleSolver:
    """Class for solving puzzle."""

    def __init__(self):
        """Initialize class members."""
        self.puzzle = None
        self.solvedDict = {}
        self.unsolvedDict = {}
        self.guessesDictionary = {}
        self.currentGuess = None
        self.solvedStateSnapshot = None
        self.unsolvedStateSnapshot = None

    def createOrRestoreSnapshot(self):
        """Create or restore a snapshot of valid solved puzzle state."""
        if not self.solvedStateSnapshot:
            self.solvedStateSnapshot = copy.deepcopy(self.solvedDict)
            self.unsolvedStateSnapshot = copy.deepcopy(self.unsolvedDict)
        else:
            self.solvedDict = copy.deepcopy(self.solvedStateSnapshot)
            self.unsolvedDict = copy.deepcopy(self.unsolvedStateSnapshot)

    def updateSnapshot(self):
        """Update the snapshot."""
        self.solvedStateSnapshot = copy.deepcopy(self.solvedDict)
        self.unsolvedStateSnapshot = copy.deepcopy(self.unsolvedDict)

    def loadPuzzle(self, file_path=None):
        """Load puzzle from a file."""
        if not file_path:
            tk.Tk().withdraw()
            file_path = filedialog.askopenfilename(
                                initialdir=os.path.join(os.getcwd(), "puzzles"),
                                title="select puzzle file")
            if not file_path:
                exit()

        my_data = genfromtxt(file_path, delimiter=',', filling_values=0)
        self.puzzle = my_data.astype(int)
        self.initializeSolvedSet()
        if IS_MAIN_PROGRAM:
            print(self.puzzle)

    def runSolver(self):
        """Solver loop."""
        puzzleStatus = PuzzleState.UNSOLVED
        hasChanged = True

        while hasChanged and puzzleStatus != PuzzleState.INVALID:
            hasChanged = False
            unsolvedCells = VALID_INDEXES.difference(self.solvedDict.keys())
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
                    if loc in self.unsolvedDict.keys():
                        self.unsolvedDict.pop(loc)
                    hasChanged = True
                else:
                    self.unsolvedDict[loc] = list(candidateSet)

            if not unsolvedCells:
                puzzleStatus = PuzzleState.SOLVED
                break

            if not hasChanged:
                puzzleStatus = PuzzleState.UNSOLVED
                break

        return puzzleStatus

    def updatePuzzle(self):
        """Update puzzle from the solver."""
        self.puzzle = np.zeros((9, 9), dtype=np.int)
        for key, value in self.solvedDict.items():
            self.puzzle[key[0], key[1]] = value[0]

    def applyNextGuess(self):
        """Apply next guess."""
        self.guessesDictionary = getGuessList(self.unsolvedDict)
        if self.currentGuess is not None:
            self.guessesDictionary.remove(self.currentGuess)

        guess = random.choice(self.guessesDictionary)
        cell = guess[0]
        guessedValue = guess[1]
        self.setSolvedCellValue(cell, guessedValue)
        self.currentGuess = guess
        if IS_MAIN_PROGRAM:
            print("applying guess ", end=" ")
            printCell(cell, guessedValue)

    def processValidGuessAlternative(self):
        """Process invalid guess alternative."""
        if self.currentGuess is not None:
            guess = self.currentGuess
            cell = guess[0]
            invalidGuessValue = guess[1]
            # update unsolvedSet
            possibleValues = self.unsolvedDict[cell]
            possibleValues.remove(invalidGuessValue)

            if len(possibleValues) == 1:
                self.setSolvedCellValue(cell, possibleValues[0])
                if IS_MAIN_PROGRAM:
                    print("***resolved guess !!! ", end=" ")
                    printCell(cell, possibleValues[0])
                    print("# solved cells={0}".format(len(self.solvedDict)))

            # reset current guess and list of previous guesses
            self.currentGuess = None

    def setSolvedCellValue(self, cell, value):
        """Set cell value."""
        self.solvedDict[cell] = [value]
        self.puzzle[cell[0], cell[1]] = value
        self.unsolvedDict.pop(cell, None)

    def initializeSolvedSet(self):
        """Return the dictionary of initial solved cells."""
        self.solvedDict = {(x, y):
                           [self.puzzle[x, y]]
                           for x in range(9)
                           for y in range(9)
                           if self.puzzle[x, y] > 0}

    def solve(self):
        """Solver loop."""
        loopIndex = 0
        while True:
            status = self.runSolver()
            loopIndex += 1

            if status == PuzzleState.SOLVED:
                if IS_MAIN_PROGRAM:
                    print("puzzle solved in {0} iterations".format(loopIndex))
                break

            if status == PuzzleState.UNSOLVED:
                if IS_MAIN_PROGRAM:
                    print("puzzle is in unsolved state")

                self.createOrRestoreSnapshot()
                self.updatePuzzle()
                self.applyNextGuess()

            if status == PuzzleState.INVALID:
                if IS_MAIN_PROGRAM:
                    print("puzzle is in invalid state")

                self.createOrRestoreSnapshot()
                self.processValidGuessAlternative()
                self.updateSnapshot()
                self.updatePuzzle()

            if loopIndex == MAX_LOOPS:
                if IS_MAIN_PROGRAM:
                    print("cannot solve puzzle :-(")
                break

        if IS_MAIN_PROGRAM:
            print(self.puzzle)
        return status


def main():
    """Load and solve a sudoku puzzle."""
    p = PuzzleSolver()
    p.loadPuzzle()
    p.solve()


if __name__ == "__main__":
    IS_MAIN_PROGRAM = True
    main()
