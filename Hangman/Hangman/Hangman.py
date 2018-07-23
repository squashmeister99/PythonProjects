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

def main():
    for item in HANGMAN_PICS:
        print(item)

    for item in WORD_LIST:
        print(getRandomWord())

    print(playAgain())

if __name__ == "__main__":
    main()