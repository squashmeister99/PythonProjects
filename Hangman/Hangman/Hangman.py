import random

HANGMAN_PICS = ['''
    +---+
        |
        |
        |
       ===''', '''
    +---+
    0   |
        |
        |
       ===''', '''
    +---+
    0   |
    |   |
        |
       ===''', '''
    +---+
    0   |
   /|   |
        |
       ===''', '''
    +---+
    0   |
   /|\  |
        |
       ===''', '''
    +---+
    0   |
   /|\  |
   /    |
       ===''', '''
    +---+
    0   |
   /|\  |
   / \  |
       ===''']


WORDS_AND_CATEGORIES = {"Colors":"red blue green yellow magenta purple indigo white black".split(),
                        "Shapes":"triangle square diamond rhombus pentagon rectangle ellipse octagon".split,
                        "Fruits":"apple orange banana kiwi mango jackfruit guava strawberry".split()}

def initVariables():
    return '', '', getRandomWord(), False

#fetch a random word from the word list
def getRandomWord():
    category = random.choice(list(WORDS_AND_CATEGORIES.keys()))
    wordList = WORDS_AND_CATEGORIES[category]
    return (category, wordList[random.randint(0, len(wordList) - 1)])

def playAgain():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

def displayBoard(missedLetters, correctLetters, secretWordTuple):
    category = secretWordTuple[0]
    secretWord = secretWordTuple[1]
    print('word category = {0}'.format(category))
    print(HANGMAN_PICS[len(missedLetters)])
    print()

    print('Missed letters:', end= ' ')
    for letter in missedLetters:
        print(letter, end = ' ')
    print()

    blanks = '_'*len(secretWord)
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    # print current status
    for letter in blanks:
        print(letter, end = ' ')
    print()

def getGuess(alreadyGuessed):
    while True:
        print('Guess a letter.')
        guess = input().lower()
        if len(guess) != 1:
            print('Please enter a single letter')
        elif guess in alreadyGuessed:
            print('You have already guessed the letter. Plese choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER between a-z')
        else:
            return guess


def main():
    print('HANGMAN')
    missedLetters, correctLetters, secretWordTuple, gameIsDone = initVariables()
    category = secretWordTuple[0]
    secretWord = secretWordTuple[1]
    

    while True:
        displayBoard(missedLetters, correctLetters, secretWordTuple)

        guess = getGuess(missedLetters + correctLetters)
        if guess in secretWord:
            correctLetters += guess
            #check if player has won
            foundAllLetters = True
            for i in range(len(secretWord)):
                if secretWord[i] not in correctLetters:
                    foundAllLetters = False
                    break;

            if foundAllLetters:
                print('Yes! The secret word is \'{0:s}\'. You have won !'.format(secretWord))
                gameIsDone = True

        else:
            missedLetters += guess
            # check if player has lost
            if len(missedLetters) == len(HANGMAN_PICS) -1:
                displayBoard(missedLetters, correctLetters, secretWordTuple)
                print('You have run out of guesses !. The secret word was \'{0}\''.format(secretWord))
                gameIsDone = True

        if gameIsDone:
            if playAgain():
                    missedLetters, correctLetters, secretWordTuple, gameIsDone = initVariables()
                    secretWord = secretWordTuple[1]
                    category = secretWordTuple[0]
            else:
                break;



if __name__ == "__main__":
    main()