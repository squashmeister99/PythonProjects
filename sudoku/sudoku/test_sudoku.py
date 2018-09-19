import sudoku
import numpy as np
import os



def test_easy():
    p = sudoku.PuzzleSolver()
    p.loadPuzzle(os.path.join(os.getcwd(), "puzzles", "easy1.csv"))
    status = p.solve()
    assert(status == sudoku.PuzzleState.SOLVED)


def test_medium():
    p = sudoku.PuzzleSolver()
    p.loadPuzzle(os.path.join(os.getcwd(), "puzzles", "medium1.csv"))
    status = p.solve()
    assert(status == sudoku.PuzzleState.SOLVED)


def test_hard():
    p = sudoku.PuzzleSolver()
    p.loadPuzzle(os.path.join(os.getcwd(), "puzzles", "hard1.csv"))
    status = p.solve()
    assert(status == sudoku.PuzzleState.SOLVED)


def test_extreme():
    p = sudoku.PuzzleSolver()
    p.loadPuzzle(os.path.join(os.getcwd(), "puzzles", "extreme1.csv"))
    status = p.solve()
    assert(status == sudoku.PuzzleState.SOLVED)


def test_ohdear():
    p = sudoku.PuzzleSolver()
    p.loadPuzzle(os.path.join(os.getcwd(), "puzzles", "ohdear1.csv"))
    status = p.solve()
    assert(status == sudoku.PuzzleState.UNSOLVED)


def test_checkAnswer():
    p = sudoku.PuzzleSolver()
    p.loadPuzzle(os.path.join(os.getcwd(), "puzzles", "extreme5.csv"))
    status = p.solve()
    solution = sudoku.PuzzleSolver()
    solution.loadPuzzle(os.path.join(os.getcwd(), "puzzles", "extreme5_solution.csv"))
    assert(status == sudoku.PuzzleState.SOLVED)
    assert(np.array_equal(p.puzzle, solution.puzzle))

if __name__ == "__main__":
    test_easy()
    test_medium()
