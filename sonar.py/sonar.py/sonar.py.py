import random

def printView(rows, cols):
   
    for  row in range(rows):
        val = ''
        for i in range(cols):
            if random.choice([0, 1]) == 0:
                val += '`'
            else:
                val += '~'
        
        print(val)


def main():
    printView(20,40)


if __name__ == "__main__":
    main()