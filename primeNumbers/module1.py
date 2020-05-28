primes=[2,3,5,7]
primes2 = primes.copy()

def is_prime(n):
    if n <= 0:
        return False
        
    if n < primes2[-1]:
        return n in primes2
    else:
        listOfNumbers = set([x for x in range(2, n + 1)])
        while len(listOfNumbers) > 0:
            currentPrime = listOfNumbers.pop()
            primes2.append(currentPrime)
            multiple = currentPrime
            while multiple <= n + 1:
                multiple += currentPrime
                try:
                    listOfNumbers.remove(multiple)
                except KeyError:
                    pass
        
        return n in primes2

print(is_prime(25))
