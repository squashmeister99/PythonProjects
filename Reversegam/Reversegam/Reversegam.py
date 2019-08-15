import random
import sys
import copy


# define board dimensions
WIDTH = HEIGHT = 8
NEIGHBOURS = [ [x, y] for x in range(-1, 2) for y in range(-1, 2) if x | y != 0]
CORNERS = [(0,0), (0, WIDTH - 1), (HEIGHT -1, 0), (HEIGHT - 1, WIDTH - 1)]
DIGITS1TO8 = [str(x) for x in range(1,9)]

def getBoardCopy(board):
    return copy.deepcopy(board)

def getBoardWithValidMoves(board, tile):
    boardCopy = getBoardCopy(board)
    for x, y in getValidMoves(board, tile):
        boardCopy[x][y] = "."
    return boardCopy

def getValidMoves(board, tile):
    validMoves = [[x,y] for x in range(WIDTH) for y in range(HEIGHT) if isValidMove(board, tile, (x,y)) != False]
    return validMoves


def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(WIDTH):
        for y in range(WIDTH):
            if board[x][y] == "X":
                xscore += 1
            if board[x][y] == "O":
                oscore += 1
    return {"X":xscore, "O": oscore}


def enterPlayerTile():
    tile = ""
    while tile not in ["X", "O"]:
        print("do you want to be X or O ?")
        tile = input().upper()
    
    if tile == "X":
        return ["X", "O"]
    else:
        return ["O", "X"]

def whoGoesFirst():
    return random.choice(['computer', 'player'])

def makeMove(board, tile, loc):
    tilesToFlip = isValidMove(board, tile, loc)
    if not tilesToFlip:
        return False

    board[loc[0]][loc[1]] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile

    return True

def isOnCorner(loc):
    return loc in CORNERS

def getPlayerMove(board, playerTile):
    while True:
        print('enter your move, "quit" to end game, or "hints" to toggle hints.')
        move = input().lower()
        if move in ["quit", "hints"]:
            return move

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, (x,y)):
                break
            else:
                continue

        else:
            print('That is not a valid move. Enter column (1-8) and then row (1-8)')
            print('For example, 81 will move to top right hand corner')

    return (x,y)


def getComputerMove(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)

    for x, y in possibleMoves:
        if isOnCorner((x,y)):
            return (x,y)

    bestScore = -1
    bestMove = [-1, -1]
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, (x,y))
        score = getScoreOfBoard(board)[computerTile]
        if score > bestScore:
            bestMove = (x, y)
            bestScore = score

    return bestMove

def printScore(board, playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print("You: {0} points. Computer: {1} points".format(scores[playerTile], scores[computerTile]))

def playGame(playerTile, computerTile):
    showHints = False
    turn = whoGoesFirst()
    print("The {0} will go first".format(turn))

    board = getNewBoard()
    board[3][3] = "X"
    board[4][4] = "X"
    board[3][4] = "Y"
    board[4][3] = "Y"

    while True:
        playerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)

        if len(playerValidMoves) == 0 and len(computerValidMoves) == 0:
            return board

        elif turn == "player":
            if len(playerValidMoves) > 0:
                if showHints:
                    validBoardMoves = getBoardWithValidMoves(board, playerTile)
                    drawBoard(validBoardMoves)
                else:
                    drawBoard(board)
                printScore(board, playerTile, computerTile)

                move = getPlayerMove(board, playerTile)
                if move == "quit":
                    print('Thanks for playing')
                elif move == "hints":
                    showHints = not showHints
                    continue
                else:
                    makeMove(board, playerTile, move)

            turn = "computer"

        elif turn == "computer":
            if len(computerValidMoves) > 0:
                drawBoard(board)
                printScore(board, playerTile, computerTile)

                input("press Enter to see computer move")
                move = getComputerMove(board, computerTile)
                makeMove(board, computerTile, move)

            turn = "player"


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

    otherTile = "O" if tile == "X" else "O"

    tilesToFlip = []
    for xdir, ydir in NEIGHBOURS:
        x, y = loc[0], loc[1]
        x+= xdir
        y+= ydir
        while isOnBoard((x,y)) and board[x][y] == otherTile:
            x+= xdir
            y+= ydir
            if isOnBoard((x,y)) and board[x][y] == tile:
                while True:
                    x -= xdir
                    y -= ydir
                    if (x,y) == loc:
                        break;
                    tilesToFlip.append([x, y])

    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip


def getNewBoard():
    board = []
    for i in range(HEIGHT):
        board.append([" " for _ in range(WIDTH)])
    return board


def main():
    print("Welcome to reversegam!")
    playerTile, computerTile = enterPlayerTile()

    while True:
        finalBoard = playGame(playerTile, computerTile)
        drawBoard(finalBoard)
        scores = getScoreOfBoard(finalBoard)
        printScore(finalBoard, playerTile, computerTile)

        print("do you want to play again ? (yes or no)")
        if not input().lower().startswith("y"):
            break


if __name__ == "__main__":
    main()