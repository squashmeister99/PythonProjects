import random

VALID_MOVES = list((range(1,10)))

# possible winning combinations
WINNING_SET = [(1,2,3), (4,5,6), (7,8,9),   #horizontal
                (1,4,7), (2,5,8), (3,6,9),  #vertical
                (1,5,9), (7,5,3)]           #diagonals

def drawRow(row):
    # this function prints the current row
    print("{0} | {1} | {2}".format(row[0], row[1], row[2]))

def drawBoard(board):
    #this function prints out the current board
    drawRow(board[7:])
    drawRow(board[4:7])
    drawRow(board[1:4])

def chooseLetter():
    #lets the player choose whether he wants to be X or O
    letter = ''
    while not(letter == 'X' or letter == 'O'):
        print("Do you want to be X or O?")
        letter = input().upper()

    if letter == "X":
        return ("X", "O")
    else:
        return ("O", "X")

def whoGoesFirst():
    return "computer" if random.randint(0,1) == 0 else "player"


def isSpaceFree(board, move):
    if move == 0:   # special case for index = 0, which is ignored
        return False;
    else:
        return board[move] == ' '

def getPlayerMove(board):
    move = 0
    while move not in VALID_MOVES or not isSpaceFree(board, move):
        print('what is your next move ?(1-9)')
        move = int(input())
        if not isSpaceFree(board, move):
            print('the board position is not free. Pick another move (1-9)')

    return move

def chooseRandomComputerMove(board, moveList):
    # choose a valid random move
    possibleMoves = [x for x in moveList if isSpaceFree(board, x)]
    if possibleMoves:
        return random.choice(possibleMoves)
    else:
        return None

def isBoardFull(board):
    result =  True if ' ' not in board else False
    return result

def getComputerMove(board, letterChoice):
    playerLetter = letterChoice[0]
    computerLetter = letterChoice[1]

    #check if computer has a winning move
    willWinOnNextMove, winningMove = hasWinningMove(board, computerLetter)
    if willWinOnNextMove:
        return winningMove

    #check if player has a winning move. if yes, then block it
    willWinOnNextMove, blockingMove = hasWinningMove(board, playerLetter)
    if willWinOnNextMove:
        return blockingMove

    #take corners if available
    nextMove = chooseRandomComputerMove(board,[1,3,7,9])
    if nextMove:
        return nextMove

    #take center if available
    if isSpaceFree(board, 5):
        return 5;

    #if we reach here, then pick a random move on the side
    return chooseRandomComputerMove(board,[2, 4, 6, 8])

#check if we have a winner
def isWinner(board, letter):
    for item in WINNING_SET:
        x = [board[item[0]], board[item[1]], board[item[2]]] # construct a potential winning set
        if x.count(x[0]) == len(x) and x[0] == letter:
            return True;

    return False;

#check if we can win on next move. if true, return winning move
def hasWinningMove(board, letter):
    for item in WINNING_SET:
        x = [board[item[0]], board[item[1]], board[item[2]]] # construct a potential winning set
        if x.count(letter) == 2:
            #find winning move
            for idx, val in enumerate(x):
                if val != letter:
                    return (True, item[idx])

    return (False, None)

def makeMove(board, move, letter):
    board[move] = letter

def main():
    print('Welcome to Tic-Tac-Toe')
    while True:
        board = list(' ' for x in range(10))             #initialize the board
        playerLetter, computerLetter = chooseLetter()   # get letter choices
        turn = whoGoesFirst()
        print("'{0}' will go first".format(turn))
        gameIsPlaying = True

        while gameIsPlaying:
            if turn == "player":
                print(" ")
                drawBoard(board)
                move = getPlayerMove(board)
                print("player move = {0}".format(move))
                makeMove(board, move, playerLetter)
                print(" ")
                drawBoard(board)

            if isWinner(board, playerLetter):
                drawBoard(board)
                print("Congratulations. You have won !")
                gameIsPlaying = False

            else:
                if isBoardFull(board):
                    drawBoard(board)
                    print("The game is a tie!")
                    gameIsPlaying = False
                else:
                    turn = "computer"

            if turn == "computer":
                move = getComputerMove(board, (playerLetter, computerLetter))
                makeMove(board, move, computerLetter)

            if isWinner(board, computerLetter):
                drawBoard(board)
                print("Computer has won ! Better luck next time")
                gameIsPlaying = False

            else:
                if isBoardFull(board):
                    drawBoard(board)
                    print("The game is a tie!")
                    gameIsPlaying = False
                else:
                    turn = "player"

        print("do you want to play again ? (yes or no)")
        if not input().lower().startswith("y"):
            break;



if __name__ == "__main__":
    main()
