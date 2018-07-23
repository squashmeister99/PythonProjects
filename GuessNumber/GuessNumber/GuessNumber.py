import random

numberOfAttempts = 0

def main():
    print("Hello, what is your name")
    name = input()
    number = random.randint(1,20)
    print('Well, ' + name + ', I am thinking of a number from 1 to 20')

    for numberOfAttempts in range(6):
        print("Take a guess")
        guess = int(input())

        if guess < number:
            print('Your guess is too low')

        if guess > number:
            print('Your guess is too high')

        if guess == number:
            print("Good job, {0:s}, you guessed the number in {1:d} tries".format(name, numberOfAttempts + 1))
            break;

if __name__ == "__main__":
    main()