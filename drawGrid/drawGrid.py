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


# draws a box using turtle graphics'
def draw_box(t, x, y, size, fill_color=BG_COLOR):
    t.penup()
    t.goto(x, y)
    t.pendown()

    for i in range(0, 4):
        t.forward(size)
        t.right(90)
    return


def playGame(iterations, x_dim, y_dim):
    for x in range(iterations):

        t1_start = perf_counter()
        num_squares = x_dim*y_dim
        t1_stop = perf_counter()
        print("Elapsed time for loop: {0} sec", t1_stop - t1_start)


def onClickFunction(x, y):
    print("user clicked at coordinates ({0},{1})".format(x, y))
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
        for j in range(0, y_dim):
            draw_box(t, start_x+j*BOX_SIZE, start_y+i*BOX_SIZE, BOX_SIZE)

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


if __name__ == "__main__":
    main()
