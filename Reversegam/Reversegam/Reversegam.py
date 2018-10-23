import _random
import sys

# define board dimensions
WIDTH = HEIGHT = 8

def drawBoard(board):
    print("  12345678")
    print(" +--------")
    for y in range(HEIGHT):
        print("{0}|".format(y + 1), end="")
        for x in range(WIDTH):
            print(board[x][y], end="")
        print("|{0}".format(y + 1))
    print(" +--------")
    print("  12345678")

def isOnBoard(loc):
    return 0 <= loc[0] < WIDTH and 0 <= loc[1] < HEIGHT

def isValidMove(board, tile, loc):
    if board[loc[0]][loc[1]] != " " or not isOnBoard(loc):
           return False
    otherTile = "O" if tile == "X" else "X"
    tileToFlip = []





def getBoard():
    board = []
    for i in range(HEIGHT):
        board.append([" " for _ in range(WIDTH)])
    return board


        
    



    
def main():
    board = getBoard()
    drawBoard(board)

if __name__ == "__main__":
    main()