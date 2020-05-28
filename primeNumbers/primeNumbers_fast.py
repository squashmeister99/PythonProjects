import argparse
from time import perf_counter

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, default=15,
                        help="find all primes upto specified number")
    args = parser.parse_args()
    upperLimit = args.n
    myset = set([x for x in range(2, upperLimit + 1)])

    '''Sieve of Eratosthenes prime search algoritm'''
    primes = []

    start = perf_counter()

    while len(myset):
        currentPrime = myset.pop()
        primes.append(currentPrime)
        multiple = currentPrime
        while multiple <= upperLimit:
            multiple += currentPrime
            try:
                myset.remove(multiple)
            except KeyError:
                pass
    end = perf_counter()
    print("Sieve of Eratosthenes executed in {0} seconds".format(end - start))
    print("number of primes <= {0} = {1}".format(upperLimit, len(primes)))

if __name__ == "__main__":
    main()
