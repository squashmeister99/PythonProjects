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

WORD_LIST = '''cat dog apple banana spider stork eagle ferret panda shark anaconda crocodile alligator pirhana
                orca '''.split()

#fetch a random word from the word list
def getRandomWord():
    return WORD_LIST[random.randint(0, len(WORD_LIST) - 1)]

def playAgain():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

def displayBoard(missedLetters, correctLetters, secretWord):
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

def main():
    print('HANGMAN')
    missedLetters = ''
    correctLetters = ''
    secretWord = getRandomWord()
    gameIsDone = False


    while not gameIsDone:
        displayBoard(missedLetters, correctLetters, secretWord)
        gameIsDone = not playAgain()

if __name__ == "__main__":
    main()