import random

def bubbleSort(items):
    loopIndex = 0
    for i in range(len(items)):
        for j in range(len(items) -i - 1):
            loopIndex += 1
            if items[j] > items[j+1]:
                items[j], items[j+1] = items[j+1], items[j]

    return loopIndex


def main():
    random_items = [random.randint(-50, 100) for c in range(100)]
    print(random_items)
    iterations = bubbleSort(random_items)
    print(random_items)
    print("bubblesort took {0} iterations to sort {1} numbers".format(iterations, len(random_items)))

if __name__ == "__main__":
    main()


