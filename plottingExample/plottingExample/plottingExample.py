import matplotlib.pyplot as plt
import random

x = [a for a in range(10)]
y = [a for a in range(10)]
random.shuffle(y)

#basic plot
plt.plot(x,y)
plt.show()

#plot with x and y labels
plt.ylabel('random numbers')
plt.xlabel('index')
plt.plot(x,y)
plt.show()

# add multiple plots
plt.figure(1)

#subplot1
plt.subplot(211)
plt.plot(x,y)

#subplot2
plt.subplot(212)
plt.plot(x, y)

plt.show()

plt.clf()                       # clear current figure
plt.figure(1)                # the first figure
plt.subplot(211)             # the first subplot in the first figure
plt.plot([1, 2, 3])
plt.subplot(212)             # the second subplot in the first figure
plt.plot([4, 5, 6])


plt.figure(2)                # a second figure
plt.plot([4, 5, 6])          # creates a subplot(111) by default

plt.figure(1)                # figure 1 current; subplot(212) still current
plt.subplot(211)             # make subplot(211) in figure1 current
plt.title('Easy as 1, 2, 3') # subplot 211 title
plt.show()