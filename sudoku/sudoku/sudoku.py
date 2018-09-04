import numpy as np
import csv
import sys



def main():
    a = np.arange(100).reshape(10,10)
    print(a)
    for i in range(10):
        print(a[i,:])

    for j in range(10):
        print(a[:, j])

    b = a[0:3, 0:3]
    c = b.ravel()
    print(np.unique(c))
    
    if 11 in b:
        print("True")


if __name__ == "__main__":
    main()