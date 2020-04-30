import argparse
from time import perf_counter


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, default=15,
                        help="find all primes upto specified number")
    args = parser.parse_args()
    upperLimit = args.n
    mylist = [x for x in range(2, upperLimit + 1)]

    '''Sieve of Eratosthenes prime search algoritm'''
    primes = []

    start = perf_counter()

    while len(mylist) > 0:
        # add first number to the prime list
        currentPrime = mylist.pop(0)
        primes.append(currentPrime)
        multiple = currentPrime
        while multiple <= upperLimit:
            multiple += currentPrime
            try:
                mylist.remove(multiple)
            except ValueError:
                pass
    end = perf_counter()
    print("Sieve of Eratosthenes executed in {0} seconds".format(end - start))
    print("number of primes <= {0} = {1}".format(upperLimit, len(primes)))

    '''Euler's sieve algorithm'''
    primes.clear()

    mylist = [x for x in range(2, upperLimit + 1)]

    start = perf_counter()
    while len(mylist) > 0:
        # add first number to the prime list
        currentPrime = mylist[0]
        primes.append(currentPrime)
        l2 = [x*currentPrime for x in mylist if x*currentPrime <= upperLimit]
        mylist = [x for x in mylist if x not in l2]
        mylist.remove(currentPrime)

    end = perf_counter()
    print("Sieve of Euler executed in {0} seconds".format(end - start))
    print("number of primes <= {0} = {1}".format(upperLimit, len(primes)))


if __name__ == "__main__":
    main()
