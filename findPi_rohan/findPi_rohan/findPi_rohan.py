q=1
sign = 1
for x in range(3,500000, 2):
    sign = -1*sign
    currentTerm = sign/x
    q = q + currentTerm
    if (x%9999 == 0):
        print(4*q)
