import sudoku
import numpy as np


def test_easy():
    p = sudoku.PuzzleSolver()
    p.loadPuzzle("easy1.csv")
    status = p.solve()
    assert(status == sudoku.PuzzleState.SOLVED)


def test_medium():
    p = sudoku.PuzzleSolver()
    p.loadPuzzle("medium1.csv")
    status = p.solve()
    assert(status == sudoku.PuzzleState.SOLVED)


def test_hard():
    p = sudoku.PuzzleSolver()
    p.loadPuzzle("hard1.csv")
    status = p.solve()
    assert(status == sudoku.PuzzleState.SOLVED)


def test_extreme():
    p = sudoku.PuzzleSolver()
    p.loadPuzzle("extreme_1.csv")
    status = p.solve()
    assert(status == sudoku.PuzzleState.SOLVED)


def test_ohdear():
    p = sudoku.PuzzleSolver()
    p.loadPuzzle("ohdear_1.csv")
    status = p.solve()
    assert(status == sudoku.PuzzleState.UNSOLVED)


def test_checkAnswer():
    p = sudoku.PuzzleSolver()
    p.loadPuzzle("extreme5.csv")
    status = p.solve()
    solution = sudoku.PuzzleSolver()
    solution.loadPuzzle("extreme5_solution.csv")
    assert(status == sudoku.PuzzleState.SOLVED)
    assert(np.array_equal(p.puzzle, solution.puzzle))
