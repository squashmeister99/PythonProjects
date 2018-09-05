import numpy as np
from numpy import genfromtxt
import tkinter as tk
from tkinter import filedialog

VALID_SET = {1,2,3,4,5,6,7,8,9}

def loadPuzzle():
    root = tk.Tk().withdraw()
    file_path = filedialog.askopenfilename(initialdir=".\\", title="select a csv file containing sudoku puzzle")
    my_data = genfromtxt(file_path, delimiter=',', filling_values=0)
    puzzle = my_data.astype(int)
    print(puzzle)
    return puzzle


def getMissingNumbers(myList):
    return VALID_SET.difference(set(myList))


def getSubmatrixRange(x):  
    begin = 0
    if 0 <= x <= 2:
        begin = 0    
    if 3 <= x <= 5:
        begin = 3
    if 6 <= x <= 8:
        begin = 6
   
    # return min and max indexes
    return begin, begin + 3


def getSubmatrix(puzzle, loc):
    x_begin, x_end = getSubmatrixRange(loc[0])
    y_begin, y_end = getSubmatrixRange(loc[1])
    sub_matrix = puzzle[x_begin:x_end, y_begin:y_end]
    return sub_matrix.ravel()
    

def getSolvedSet(puzzle):
    solvedSet = {}
    rows, cols = puzzle.shape
    for i in range(rows):
        for j in range(cols):
            if puzzle[i, j] > 0:
                solvedSet[(i,j)] = [puzzle[i,j]]

    return solvedSet


def printSolver(solver):
    for index in solver:
        print("({0}, {1}) = {2}".format(index[0], index[1], solver[index]))


def getAllIndexes():
    """ returns a set of all possible cell indexes in a puzzle"""
    allIndexes = []
    for x in range(9):
        for y in range(9):
            allIndexes.append((x,y))

    return allIndexes

def solveCell(puzzle, loc):
    """ main solver algorithm for sudoku puzzle returns the
    viable candidates for a given cell"""

    # evaluate rows and columns
    rowSet = getMissingNumbers(puzzle[loc[0], :])
    colSet = getMissingNumbers(puzzle[:, loc[1]])
    tempSet = rowSet.intersection(colSet)
    #evaluate submatrix
    submatrixSet = getMissingNumbers(getSubmatrix(puzzle, loc))
    candidateSet = tempSet.intersection(submatrixSet)
    return candidateSet


def main():
    puzzle = loadPuzzle()
    solvedState = getSolvedSet(puzzle)
    solvedCells = solvedState.keys()
    allCells = getAllIndexes()
    unsolvedCells = set(allCells).difference(solvedCells)

    while len(solvedCells) != puzzle.size :
        for loc in unsolvedCells:
            candidateSet = solveCell(puzzle, loc)     
            if len(candidateSet) == 1:
                value = candidateSet.pop()
                print("({0},{1}) = {2}".format(loc[0], loc[1], value))
                # move the current cell to solved and update the puzzle
                solvedState[loc] = [value]
                puzzle[loc[0], loc[1]] = value

    # if we get here the puzzle is solved
    print(puzzle)
    
if __name__ == "__main__":
    main()