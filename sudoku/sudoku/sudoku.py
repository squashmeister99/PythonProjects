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

def getSolvedSet(puzzle):
    solvedSet = {}
    rows, cols = puzzle.shape
    print("rows = {0}, columns = {1}".format(rows, cols))
    for i in range(rows):
        for j in range(cols):
            if puzzle[i, j] > 0:
                solvedSet[(i,j)] = [puzzle[i,j]]

    return solvedSet

def printSolverState(solver):
    for index in solver:
        print("({0}, {1}) = {2}".format(index[0], index[1], solver[index]))




def main():
    puzzle = loadPuzzle()

    solvedState = getSolvedSet(puzzle)
    printSolverState(solvedState)
    
    

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