import random

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
        return "X", "O"
    else:
        return "O", "X"

def whoGoesFirst():
    if random.randint(0,1) == 0:
        return "computer"
    else:
        return "player"

def main():
    board = list(1 for x in range(10))
    drawBoard(board)
    playerLetter, computerLetter = chooseLetter()
    print("you chose the letter {0}".format(playerLetter))
    print("{0} goes first".format(whoGoesFirst()))


if __name__ == "__main__":
    main()
