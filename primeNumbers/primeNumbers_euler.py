import argparse
from time import perf_counter
from guppy import hpy


def getFirstNumber(myset):
    for x in myset:
        return x

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, default=15,
                        help="find all primes upto specified number")
    args = parser.parse_args()
    upperLimit = args.n

    '''Sieve of Eratosthenes prime search algoritm'''
    primes = []

    
    mylist = [x for x in range(2, upperLimit + 1)]
    h = hpy()
    print(h.heap())
    start = perf_counter()
    while len(mylist) :
        # add first number to the prime list
        currentPrime = getFirstNumber(mylist)
        primes.append(currentPrime)
        l2 = set([x*currentPrime for x in mylist if x*currentPrime <= upperLimit])
        mylist = [x for x in mylist if x not in l2]
        mylist.remove(currentPrime)

    end = perf_counter()

    print(h.heap())

    print("Sieve of Euler executed in {0} seconds".format(end - start))
    print("number of primes <= {0} = {1}".format(upperLimit, len(primes)))


if __name__ == "__main__":
    main()
