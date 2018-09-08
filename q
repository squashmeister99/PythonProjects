[1mdiff --git a/sudoku/sudoku/sudoku.py b/sudoku/sudoku/sudoku.py[m
[1mindex c154410..2df1a80 100644[m
[1m--- a/sudoku/sudoku/sudoku.py[m
[1m+++ b/sudoku/sudoku/sudoku.py[m
[36m@@ -130,7 +130,7 @@[m [mdef runSolver(puzzle, solvedSet):[m
     unsolvedCells = VALID_INDEXES.difference(solvedSet.keys())[m
     puzzleStatus = PuzzleState.UNSOLVED[m
 [m
[31m-    while len(solvedSet) != puzzle.size  :[m
[32m+[m[32m    while len(solvedSet) != puzzle.size and puzzleStatus != PuzzleState.INVALID  :[m
         oldSize = len(unsolvedCells)[m
         for loc in unsolvedCells:[m
             candidateSet = solveCell(puzzle, loc)[m
[36m@@ -140,26 +140,33 @@[m [mdef runSolver(puzzle, solvedSet):[m
                 break;[m
 [m
             if len(candidateSet) == 1:[m
[31m-                value = candidateSet.pop()[m
[31m-                [m
[32m+[m[32m                value = candidateSet.pop()[m[41m             [m
                 # move the current cell to solved and update the puzzle[m
                 solvedSet[loc] = [value][m
                 setCellValue(puzzle, loc, value)[m
[32m+[m[32m                if loc in unsolvedSet:[m
[32m+[m[32m                    unsolvedSet.pop(loc)[m
[32m+[m
             else:[m
                 unsolvedSet[loc] = candidateSet[m
 [m
         unsolvedCells = VALID_INDEXES.difference(solvedSet.keys())[m
 [m
         if(len(unsolvedCells) == oldSize):[m
[31m-            puzzleState = PuzzleState.UNSOLVED[m
[32m+[m[32m            puzzleStatus = PuzzleState.UNSOLVED[m
             print("solved state size = {0}".format(len(solvedSet)))[m
             break;[m
 [m
     if isPuzzleSolved(puzzle):[m
[31m-       puzzleState = PuzzleState.SOLVED[m
[32m+[m[32m       puzzleStatus = PuzzleState.SOLVED[m
[32m+[m
[32m+[m[32m    if not isPuzzleValid(puzzle):[m
[32m+[m[32m       puzzleStatus = PuzzleState.INVALID[m
 [m
     print(puzzle)[m
[31m-    return puzzleState, unsolvedSet[m
[32m+[m[32m    print("solved size = {0}, unsolved cells = {1}, unsolved set = {2}".format(len(solvedSet), len(unsolvedCells), len(unsolvedSet)))[m
[32m+[m[32m    #assert(len(unsolvedCells) == len(unsolvedSet))[m
[32m+[m[32m    return puzzleStatus, unsolvedSet[m
 [m
 def getGuessList(unsolvedSet):[m
     """ returns a list of guesses"""[m
[36m@@ -176,7 +183,8 @@[m [mdef getGuessList(unsolvedSet):[m
     for loc in unsolvedSet:[m
         if len(unsolvedSet[loc]) > 3:[m
             guessList.append((loc, list(unsolvedSet[loc])))[m
[31m-    [m
[32m+[m
[32m+[m[32m    print("guess list size = {0}".format(len(guessList)))[m
     return guessList[m
 [m
 def setCellValue(puzzle, cell, value):[m
[36m@@ -238,7 +246,6 @@[m [mdef main():[m
             # update the puzzle from the snapshot state[m
             # apply the guess[m
             print("puzzle is in unsolved state")[m
[31m-[m
             guessList = getGuessList(unsolvedSet)[m
             saveOrRestoreSnapshot(solvedSet, solver_snapshot)[m
             updatePuzzle(puzzle, solvedSet)[m
[36m@@ -260,8 +267,7 @@[m [mdef main():[m
                 print(cell, value)[m
                  [m
             updatePuzzle(puzzle, solvedSet)[m
[31m-            updateSnapshot(solvedSet, solvedSet_snapshot)[m
[31m-            break;[m
[32m+[m[32m            updateSnapshot(solvedSet, solver_snapshot)[m
             [m
     print(puzzle)[m
     [m
