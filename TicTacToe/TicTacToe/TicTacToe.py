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
    if move == 0:
        return False;
    else:
        return board[move] == ''

def getPlayerMove(board):
    move = 0
    while move not in VALID_MOVES or not isSpaceFree(board, move):
        print('what is your next move ?(1-9)')
        move = int(input)
    return move

def chooseRandomComputerMove(board, moveList):
    # choose a valid random move
    possibleMoves = []
    for i in moveList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if possibleMoves:
        return random.choice(possibleMoves)
    else:
        return None

def isBoardFull(board):
    result =  True if '' not in board else False
    return result

def getComputerMove(board, letterChoice):
    return None

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



def main():
    board = list(1 for x in range(10))
    drawBoard(board)
    letterChoice = chooseLetter()
    playerLetter = letterChoice[0]
    computerLetter = letterChoice[1]
    print("player letter = '{0}'".format(letterChoice[0]))
    print("computer letter = '{0}'".format(letterChoice[1]))
    print("{0} goes first".format(whoGoesFirst()))
    print(isWinner(board, 1))
    board = [-99, 0, 1, 2, 3, 1, 5, 6, 7, 8]
    almostWon, index = hasWinningMove(board, 1)
    if almostWon:
        print("winning move for '0' is = {0:d}".format(index))
    else:
        print("no winning move yet")
    


if __name__ == "__main__":
    main()
