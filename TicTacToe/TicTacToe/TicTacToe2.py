import random

###### class GameEngine
class GameEngine:
    # constants required for game
    VALID_MOVES = list((range(1,10)))
    INIT_VALUE = " "
    # possible winning combinations
    WINNING_SET = [(1,2,3), (4,5,6), (7,8,9),   #horizontal
                    (1,4,7), (2,5,8), (3,6,9),  #vertical
                    (1,5,9), (7,5,3)]           #diagonals
    board = []                                  #initial board

    CENTER = 5
    CORNERS = [1,3,7,9]
    SIDES = [2,4,6,8]

    def __init__(self):
        board = ["D"] + list(INIT_VALUE for x in range(1, 10))             #initialize the board

    def drawRow(self, row):
        # this function prints the current row
        print("{0} | {1} | {2}".format(row[0], row[1], row[2]))

    def drawBoard(self):
        #this function prints out the current board
        print(" ")
        drawRow(board[7:])
        drawRow(board[4:7])
        drawRow(board[1:4])

    def chooseLetter(self):
        #lets the player choose whether he wants to be X or O
        letter = ''
        while not(letter == 'X' or letter == 'O'):
            print("Do you want to be X or O?")
            letter = input().upper()

        if letter == "X":
            return ("X", "O")
        else:
            return ("O", "X")

    def whoGoesFirst(self):
        return "computer" if random.randint(0,1) == 0 else "player"

    def isSpaceFree(self, move):
        if move == 0:   # special case for index = 0, which is ignored
            return False;
        else:
            return board[move] == INIT_VALUE

    def isBoardFull(self):
        result =  True if INIT_VALUE not in board else False
        return result

    #check if we have a winner
    def isWinner(self, letter):
        for item in WINNING_SET:
            x = [board[item[0]], board[item[1]], board[item[2]]] # construct a potential winning set
            if x.count(x[0]) == len(x) and x[0] == letter:
                return True;

        return False;

    #check if we can win on next move. if true, return winning move
    def hasWinningMove(self, letter):
        for item in WINNING_SET:
            x = [board[item[0]], board[item[1]], board[item[2]]] # construct a potential winning set
            if x.count(letter) == 2:
                #find winning move
                for idx, val in enumerate(x):
                    if val == INIT_VALUE:
                        return (True, item[idx])

        return (False, None)

    def makeMove(self, move, letter):
        board[move] = letter

####### class HumanPlayer #########################
class HumanPlayer:
    letter = ''

    def __init__(self, letter):
        self.letter = letter
        
    def nextMove(self, board):
        move = 0
        while move not in VALID_MOVES or not isSpaceFree(board, move):
            print('what is your next move ?(1-9)')
            move = int(input())
            if not isSpaceFree(board, move):
                print('the board position is not free. Pick another move (1-9)')

        board.makeMove(move, self.letter)

####### class ComputerPlayer #############################
class ComputerPlayer:
    letter = ''

    def __init__(self, letter):
        self.letter = letter

    def nextMove(self, board):
        nextMove = _getMove(board);
        board.makeMove(nextMove, self.letter)

    def _chooseRandomMove(self, board, moveList):
        # choose a valid random move
        possibleMoves = [x for x in moveList if board.isSpaceFree(x)]
        if possibleMoves:
            return random.choice(possibleMoves)
        else:
            return None

    def _getPlayerLetter(self):
        if self.letter == "X":
            return "O"
        else:
            return "X"

    def _getMove(self, board):
        #check if computer has a winning move
        willWinOnNextMove, winningMove = board.hasWinningMove(self.letter)
        if willWinOnNextMove:
            return winningMove

        #check if player has a winning move. if yes, then block it
        willPlayerWinOnNextMove, blockingMove = board.hasWinningMove(board, _getPlayerLetter())
        if willPlayerWinOnNextMove:
            return blockingMove

        #take corners if available
        nextMove = _chooseRandomMove(board,board.CORNERS)
        if nextMove:
            return nextMove

        #take center if available
        if board.isSpaceFree(board.CENTER):
            return board.CENTER;

        #if we reach here, then pick a random move on the side
        return _chooseRandomMove(board,board.SIDES)


################### main ####################

def main():
    print('Welcome to Tic-Tac-Toe')
    while True:
        game = GameEngine()
        playerLetter, computerLetter = game.chooseLetter()                      # get letter choices
        human = HumanPlayer(playerLetter)
        computer = ComputerPlayer(computerLetter)

        turn = game.whoGoesFirst()
        print("'{0}' will go first".format(turn))
        gameIsPlaying = True

        while gameIsPlaying:
            if turn == "player":
                game.drawBoard()
                human.nextMove(game.board)
               
                if game.isWinner(human.letter):
                    game.drawBoard()
                    print("Congratulations. You have won !")
                    gameIsPlaying = False

                else:
                    if game.isBoardFull():
                        game.drawBoard()
                        print("The game is a tie!")
                        break;
                    else:
                        turn = "computer"
            else:
                computer.nextMove(game.board)
                
                if game.isWinner(computer.letter):
                    drawBoard(board)
                    print("Computer has won ! Better luck next time")
                    gameIsPlaying = False

                else:
                    if game.isBoardFull():
                        game.drawBoard()
                        print("The game is a tie!")
                        break;
                    else:
                        turn = "player"

        print("do you want to play again ? (yes or no)")
        if not input().lower().startswith("y"):
            break;

if __name__ == "__main__":
    main()
