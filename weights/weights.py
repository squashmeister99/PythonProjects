import numpy as np
def calculateWeights(myArray):
    weights = []
    sum = 2.0*np.sum(myArray)
    for item in myArray:
        val = 0.5 - float(item/sum)
        weights.append(val)

    return weights/np.sum(weights)

a = [700, 800, 900]
print(calculateWeights(a))

