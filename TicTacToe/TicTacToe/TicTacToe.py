import random

def drawRow(row):
    print("{0} | {1} | {2}".format(row[0], row[1], row[2]))

def drawBoard(board):
    #this function prints out the current board
    drawRow(board[7:])
    drawRow(board[4:7])
    drawRow(board[1:4])



def main():
    board = list(1 for x in range(10))
    drawBoard(board)

if __name__ == "__main__":
    main()
