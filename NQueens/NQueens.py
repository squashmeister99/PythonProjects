
def getDiagonals(N,i,j):
    ''' find diagonals for a given square i,j in a grid of size N'''
    result = []
    # find long diagonals
    x = i - 1
    y = j - 1
    while x >= 0 and y >= 0:
        result.append((x, y))
        x-=1
        y-=1

    x = i + 1
    y = j + 1
    while x < N and y < N :
        result.append((x, y))
        x+=1
        y+=1

    x = i - 1
    y = j + 1
    while x >= 0 and y < N :
        result.append((x, y))
        x-=1
        y+=1

    x = i + 1
    y = j - 1
    while x < N and y >= 0 :
        result.append((x, y))
        x+=1
        y-=1

    print("({0},{1}) = {2}".format(i, j, result))

    return result

def getMajorDiagonals(N, i, j):
    diag = []
    while i < N and j < N:
        diag.append((i,j))
        i += 1
        j += 1
    return diag

def findMinorDiagonals(N):
    result = []
    for sum in range(2*N - 1):
        diag = []
        for x in range(N):
            for y in range(N):
                if x + y == sum:
                    diag.append((x, y))
                    break;


        result.append(diag)

    print("Minor diagonals")
    for x in result:
        print(x)

    return result
        
def findDiagonals(N):
    return findMajorDiagonals(N).append(findMinorDiagonals(N))


def findMajorDiagonals(N):
    result = []
    x = 0
    for y in range(N):
       result.append(getMajorDiagonals(N, x, y))
    y = 0
    for x in range(1, N):
        result.append(getMajorDiagonals(N, x, y))

    print("Major diagonals")
    for x in result:
        print(x)

    return result
    

def main():
    findDiagonals(8)




if __name__ =="__main__":
    main()
