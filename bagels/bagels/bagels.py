import random

#define global variables
NUM_DIGITS = 3
MAX_GUESS = 10
NUMBERS = list(range(10))
STR_NUMBERS = "0 1 2 3 4 5 6 7 8 9".split()

# returns a number that is NUM_DIGITS long
def getSecretNumber():
    random.shuffle(NUMBERS)
    secretnumber = ''
    for i in range(NUM_DIGITS):
        secretnumber += str(NUMBERS[i])

    return secretnumber

def getClues(secretNumber, guess):
    if secretNumber == guess:
        return "You got it !"

    clues = []
    for i in range(len(guess)):
        if guess[i] == secretNumber[i]:
            clues.append("Fermi")
        elif guess[i] in secretNumber:
            clues.append("Pico")

    if len(clues) == 0:
        clues.append("Bagels")

    clues.sort() 
    return " ".join(clues)

def isOnlyDigits(guess):
    if guess == "":
        return False
    
    for i in guess:
        if i not in STR_NUMBERS:
            return False

    return True


def printIntro():
    print("I am thinking of a {0} digit number. Try and guess what it is. You have {1} guesses".format(NUM_DIGITS, MAX_GUESS))
    print("the clues I give are ...")
    print("When I say :  that means:")
    print("Bagels: None of the digits is correct")
    print("Pico: Digit is correct but in wrong place")
    print("Fermi: Digit is correct and in the right place")


def main():
    printIntro()
    while True:
        secretNumber = getSecretNumber()
        print("I have thought of a number. You have {0} guesses to get it".format(MAX_GUESS))
        
        numGuesses = 1 
        while numGuesses < MAX_GUESS:
            guess = ''
            while len(guess) != NUM_DIGITS or not isOnlyDigits(guess):
                print("Guess number {0}".format(numGuesses))
                guess = input()

            print(getClues(secretNumber, guess))
            numGuesses += 1

            if guess == secretNumber:
                break;

            if numGuesses > MAX_GUESS:
                print("you ran out of guesses. the secret number was {0}".format(secretNumber))

        print("do you want to play again ? (yes or no)")
        if not input().lower().startswith('y'):
            break;


if __name__ == "__main__":
    main()
