import turtle
import random
import argparse
from time import perf_counter, sleep

# constants
PEN_COLOR = "blue"
BG_COLOR = "white"
FILL_COLOR = "black"
BOX_SIZE = 16
RADIUS = BOX_SIZE/4

#globals
master_list = []

class Box:

    def __init__(self, xmin, ymin, xmax, ymax, state = False):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.state = state
        self.size = self.xmax - self.xmin
        print("min = [{0}, {1}], max = [{2}, {3}]".format(xmin, ymin, xmax, ymax))

    # check if the specified coordinates are inside the box
    def isWithinBounds(self, x, y):
        a = (self.xmin <= x and x < self.xmax) 
        b = (self.ymin <= y and y < self.ymax)
        return a and b

    # stub method
    def drawCircle(self, t):
        return

    def drawBox(self, t):
        t.penup()
        t.goto(self.xmin, self.ymin)
        t.pendown()

        for i in range(0, 4):
            t.forward(self.size)
            t.left(90)
        return


# draws a circle of the specified radius
def draw_circle(t, x, y, fill_color=BG_COLOR):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.pen(pencolor="purple", fillcolor="orange", pensize=10, speed=0)
    t.begin_fill()
    t.circle(RADIUS)
    t.end_fill()
    return


def playGame(iterations, x_dim, y_dim):
    for x in range(iterations):

        t1_start = perf_counter()
        num_squares = x_dim*y_dim
        t1_stop = perf_counter()
        print("Elapsed time for loop: {0} sec", t1_stop - t1_start)


def onClickFunction(x, y):
    print("user clicked at coordinates ({0},{1})".format(x, y))

    rowIndex = 0
    for row in master_list:
        colIndex = 0
        for box in row:
            if box.isWithinBounds(x, y):
                print("box index is [{0}, {1}]".format(rowIndex, colIndex))
            colIndex += 1

        rowIndex += 1


    return


def setupScreen():
    screen = turtle.Screen()
    screen.bgcolor(BG_COLOR)
    screen.title('Game of Life')
    screen.tracer(0, 0)
    screen.onclick(onClickFunction)
    return screen


def setupGridTurtle():
    t = turtle.Turtle()
    t.hideturtle()
    t.pen(pencolor=PEN_COLOR, speed=0)
    return t


def draw_board(args):
    screen = setupScreen()
    t = setupGridTurtle()
    start_x = 0
    start_y = 0
    x_dim = args.x
    y_dim = args.y
    iterations = args.i
    for i in range(0, x_dim):
        nestedList = []
        for j in range(0, y_dim):
            xmin = start_x + j*BOX_SIZE;
            xmax = start_x + (j + 1)*BOX_SIZE;
            ymin = start_y + i*BOX_SIZE;
            ymax = start_y + (i + 1)*BOX_SIZE;

            box = Box(xmin, xmax, ymin, ymax, False)
            box.drawBox(t)
            nestedList.append(box)

        master_list.append(nestedList)

    screen.update()   # update the screen

    # playGame(iterations, x_dim, y_dim)
    # screen.exitonclick()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('x', type=int, default=15, help="x dimension")
    parser.add_argument('y', type=int, default=10, help="y dimension")
    parser.add_argument('i', type=int, default=5, help="iterations")
    args = parser.parse_args()

    draw_board(args)

    input("press any key to quit !")


if __name__ == "__main__":
    main()
