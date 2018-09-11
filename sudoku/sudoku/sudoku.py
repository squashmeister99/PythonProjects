import numpy as np
from numpy import genfromtxt
import tkinter as tk
from tkinter import filedialog
import os
from enum import Enum
from random import shuffle
import copy

class PuzzleState(Enum):
    SOLVED =    0
    UNSOLVED =  1
    INVALID =   2

VALID_SET = {1,2,3,4,5,6,7,8,9}
SUB_MATRIX_CENTERS = [(1,1), (1,4), (1,7), (4,1), (4,4), (4,7), (7,1), (7,4), (7,7)]

VALID_INDEXES = {(x,y) for x in range(9) for y in range(9)}

def loadPuzzleDebug():
    """ load debug variant of the puzzle """
    my_data = genfromtxt("easy_4.csv", delimiter=',', filling_values=0)
    puzzle = my_data.astype(int)
    print(puzzle)
    return puzzle


def loadPuzzle():
    """ load the puzzle from a file """
    root = tk.Tk().withdraw() 
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="select a csv file containing sudoku puzzle")
    if not file_path:
        exit()

    my_data = genfromtxt(file_path, delimiter=',', filling_values=0)
    puzzle = my_data.astype(int)
    print(puzzle)
    return puzzle


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
        if not isValidSet(puzzle[:,i]):
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
        if not isSolvedSet(puzzle[:,i]):
            return False

    for loc in SUB_MATRIX_CENTERS:
        if not isSolvedSet(getSubmatrix(puzzle, loc)):
            return False

    return True


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


def getSubmatrix(puzzle, loc):
    x_begin, x_end = getSubmatrixRange(loc[0])
    y_begin, y_end = getSubmatrixRange(loc[1])
    sub_matrix = puzzle[x_begin:x_end, y_begin:y_end]
    return sub_matrix.ravel()
    
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
    hasChangedSinceLastIteration = True

    while hasChangedSinceLastIteration and puzzleStatus != PuzzleState.INVALID  :
        hasChangedSinceLastIteration = False
        for loc in unsolvedCells:
            candidateSet = solveCell(puzzle, loc)
            optionSize = len(candidateSet)

            if optionSize == 0:
                puzzleStatus = PuzzleState.INVALID
                break;

            if optionSize == 1:
                value = candidateSet.pop()
                
                # update the solver
                solvedSet[loc] = [value]
                puzzle[loc[0], loc[1]] = value
                if loc in unsolvedSet.keys():
                    unsolvedSet.pop(loc)
                hasChangedSinceLastIteration = True
            else:
                unsolvedSet[loc] = candidateSet

        unsolvedCells = VALID_INDEXES.difference(solvedSet.keys())
        print("unsolved cells size = {0} ".format(len(unsolvedCells)))
        print("solvedSet size = {0} ".format(len(solvedSet)))
        print("unsolvedSet size = {0} ".format(len(unsolvedSet)))

        if not unsolvedCells:
            puzzleStatus = PuzzleState.SOLVED
            break

        if not hasChangedSinceLastIteration:
            puzzleStatus = PuzzleState.UNSOLVED
            print("solved state size = {0}".format(len(solvedSet)))
            break;

    print(""" unsolved cells size """, end = " ")
    print(len(unsolvedCells))
    print(""" unsolvedSet size """, end = " ")
    print(len(unsolvedSet))

    if not isPuzzleValid(puzzle):
        puzzleStatus = PuzzleState.INVALID

    if isPuzzleSolved(puzzle):
       puzzleStatus = PuzzleState.SOLVED

    print(puzzle)
    return puzzleStatus, puzzle, solvedSet, unsolvedSet

def getGuessList(unsolvedSet):
    """ returns a list of guesses"""
    guessList = []
    print(unsolvedSet)
    for loc in unsolvedSet:
        if len(unsolvedSet[loc]) == 2:
            guessList.append((loc, list(unsolvedSet[loc])))
    #shuffle(guessList)

    for loc in unsolvedSet:
        if len(unsolvedSet[loc]) == 3:
            guessList.append((loc, list(unsolvedSet[loc])))

    for loc in unsolvedSet:
        if len(unsolvedSet[loc]) > 3:
            guessList.append((loc, list(unsolvedSet[loc])))
    
    return guessList

def setCellValue(puzzle, cell, value):
    """ cell is a tuple of the x,y indexes of the 2D array. This methods updates the specifies cell in the puzzle"""
    puzzle[cell[0], cell[1]] = value


def getValidGuessAlternative(guessList):
    """ undoes an invalid guess """
    guess = guessList[0]
    cell = guess[0]
    possibleValuesList = guess[1]
    # remove the first guess since it is invalid, and return the rest
    possibleValuesList.pop(0)
    return cell, possibleValuesList
        
def updatePuzzle(solver):
    puzzle = np.zeros((9,9), dtype=np.int)
    for item in solver.keys():
        loc = item
        value = solver[item]
        setCellValue(puzzle, loc, value[0])
    return puzzle
    
   
def main():
    puzzle = loadPuzzle()
    solvedSet = getSolvedSet(puzzle)
    guessList = []
    solvedSet_snapshot = {}
    unsolvedSet_snapshot = {}

    while True:
        status, puzzle, solvedSet, unsolvedSet = runSolver(puzzle, solvedSet)
        print("status = {0}, unsolved set size = {1}".format(status, len(unsolvedSet)))
        
        if status == PuzzleState.SOLVED:
            print("Congratulations ! puzzle is solved !!")
            break

        if status == PuzzleState.UNSOLVED:    
            # build a list of viable guesses
            # save a snapshot
            # update the puzzle from the snapshot state
            # apply the guess
            print("puzzle is in unsolved state") 
            if not solvedSet_snapshot:
                solvedSet_snapshot = copy.deepcopy(solvedSet)
            else:
                solvedSet = copy.deepcopy(solvedSet_snapshot)

            if not unsolvedSet_snapshot:
                unsolvedSet_snapshot = copy.deepcopy(unsolvedSet)
            else:
                unsolvedSet = copy.deepcopy(unsolvedSet_snapshot)

            puzzle = updatePuzzle(solvedSet)
            guessList = getGuessList(unsolvedSet)        
            guess = guessList[0]
            cell = guess[0]
            possibleValues = guess[1]
            guessedValue = possibleValues[0]
            setCellValue(puzzle, cell, guessedValue)
            solvedSet[cell] = [guessedValue]
            print("applying guess ", end = " ")
            printCell(cell, guessedValue)
            
        if status == PuzzleState.INVALID:
            print("puzzle is in invalid state")
            # restore snapsot
            # get correct guess
            # apply guess
            # update snapshot
            solvedSet.clear()
            for key, value in solvedSet_snapshot.items():
                solvedSet[key] = value

            unsolvedSet.clear()
            for key, value in unsolvedSet_snapshot.items():
                unsolvedSet[key] = value

            cell, validGuesses = getValidGuessAlternative(guessList)
            if len(validGuesses) == 1:
                # we can set the cell
                value = validGuesses[0]
                solvedSet[cell] = [value]
                if cell in unsolvedSet.keys():
                    unsolvedSet.pop(cell)
                print("resolved guess", end = " ")
                print(cell, value)
                 
            puzzle = updatePuzzle(solvedSet)
            unsolvedSet_snapshot = copy.deepcopy(unsolvedSet)
            solvedSet_snapshot = copy.deepcopy(solvedSet)

        # cache the status
        previousStatus = status
            
    print(puzzle)
    
if __name__ == "__main__":
    main()