import random

def addRowNumber(row):
    if row < 10:
        return '  ' + str(row) + ' '
    else:
        return ' ' + str(row) + ' '

def printView(rows, cols):
    columnNumbers = ' '*len(addRowNumber(0)) + ''.join([str(x) for x in range(10)]*6)
    print(columnNumbers)
    for  row in range(rows):
        val = addRowNumber(row)
        for i in range(cols):
            if random.choice([0, 1]) == 0:
                val += '`'
            else:
                val += '~'

        val += addRowNumber(row)
        print(val)
    
    print(columnNumbers)

def main():
    printView(15,60)


if __name__ == "__main__":
    main()