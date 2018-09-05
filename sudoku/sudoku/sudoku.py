import numpy as np
import tkinter as tk
from tkinter import filedialog
from numpy import genfromtxt

validset = {1,2,3,4,5,6,7,8,9}

def loadPuzzle():
    root = tk.Tk().withdraw()
    #file_path = filedialog.askopenfilename(initialdir=".\\", title="select a csv file containing sudoku puzzle")
    my_data = genfromtxt("easy1.csv", delimiter=',', filling_values=0)
    puzzle = my_data.astype(int)
    print(puzzle)
    return puzzle

def getMissingNumbers(myList):
    return validset.difference(set(myList))

def getSubmatrixRange(x):  
    x_min = 0
    if 0 <= x <= 2:
        x_min = 0    
    if 3 <= x <= 5:
        x_min = 3
    if 6 <= x <= 8:
        x_min = 6
   
    # return min and max indexes
    return x_min, x_min + 2


def getSubmatrix(puzzle, loc):
    x_begin, x_end = getSubmatrixRange(loc[0])
    y_begin, y_end = getSubmatrixRange(loc[1])
    ixgrid = np.ix_([x_begin, x_end], [y_begin, y_end])
    sub_matrix = puzzle[ixgrid]
    print("-----submatrix-----")
    print(sub_matrix)
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
    allIndexes = []
    for x in range(9):
        for y in range(9):
            allIndexes.append((x,y))

    return allIndexes


def main():
    puzzle = loadPuzzle()
    solvedState = getSolvedSet(puzzle)
    solvedIndexes = solvedState.keys()
    allIndexes = getAllIndexes()
    unsolvedIndexes = set(allIndexes).difference(solvedIndexes)

    for index in unsolvedIndexes:
        row, col = index[0], index[1]
        rowSet = getMissingNumbers(puzzle[row, :])
        colSet = getMissingNumbers(puzzle[:, col])
        validPossibilities = rowSet.difference(colSet)

        if row == 2 and col == 0:
            temp = getSubmatrix(puzzle, index)
            print(temp)
    
    

    #a = np.arange(100).reshape(10,10)
    #print(a)
    #for i in range(10):
    #    print(a[i,:])

    #for j in range(10):
    #    print(a[:, j])

    #b = a[0:3, 0:3]
    #c = b.ravel()
    #print(np.unique(c))
    
    #if 11 in b:
    #    print("True")


if __name__ == "__main__":
    main()