import turtle
import argparse
import time

# constants
BG_COLOR = "white"
PEN_COLOR = "blue"
BOX_SIZE = 32


class Cell:

    # constants
    FILL_COLOR = "black"
    BG_COLOR = "white"
    RADIUS = BOX_SIZE/4

    def __init__(self, t, xmin, ymin, xmax, ymax, state=False):
        self.t = t
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.state = state
        self.size = self.xmax - self.xmin

    # check if the specified coordinates are inside the cell
    def isWithinBounds(self, x, y):
        a = (self.xmin <= x and x < self.xmax)
        b = (self.ymin <= y and y < self.ymax)
        result = a and b
        return result

    # stub method
    def flip(self):
        self.state = not(self.state)  # flip the state
        if self.state:
            color = Cell.FILL_COLOR
        else:
            color = Cell.BG_COLOR

        self.t.penup()
        self.t.goto(self.xmin + self.size/2, self.ymin + self.size/4)
        self.t.pendown()
        self.t.pen(pensize=2, pencolor=color, fillcolor=color, speed=0)
        self.t.begin_fill()
        self.t.circle(self.size/4)
        self.t.getscreen().update()
        self.t.end_fill()
        return

    def draw(self):
        self.t.penup()
        self.t.goto(self.xmin, self.ymin)
        self.t.pendown()

        for i in range(0, 4):
            self.t.forward(self.size)
            self.t.left(90)
        return


class Grid:

    def __init__(self):
        self.cells = []
        self.t = None
        self.x = 0
        self.y = 0
        self.neighbors = {}  # dictionary to store neighbours

    def setupTurtle(self):
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.pen(pencolor=PEN_COLOR, speed=0)
        screen = self.t.getscreen()
        screen.bgcolor(BG_COLOR)
        screen.title('Game of Life')
        screen.tracer(0, 0)
        screen.onclick(onClickFunction)

    def draw(self, x, y):
        self.setupTurtle()
        self.x = x
        self.y = y

        start_x = 0
        start_y = 0
        for i in range(0, x):
            nestedList = []
            for j in range(0, y):
                xmin = start_x + j*BOX_SIZE
                xmax = start_x + (j + 1)*BOX_SIZE
                ymin = start_y + i*BOX_SIZE
                ymax = start_y + (i + 1)*BOX_SIZE
                cell = Cell(self.t, xmin, ymin, xmax, ymax, False)
                cell.draw()
                nestedList.append(cell)

            self.cells.append(nestedList)
        self.t.getscreen().update()   # update the screen

    def getNeighbours(self, x, y):
        xi = []
        xi.append(x)
        xi.append(x-1) if x > 0 else None
        xi.append(x+1) if x < self.x - 1 else None

        yi = []
        yi.append(y)
        yi.append(y-1) if y > 0 else None
        yi.append(y+1) if y < self.y - 1 else None

        masterList = []
        for a in xi:
            for b in yi:
                if [a, b] != [x, y]:
                    masterList.append([a, b])

        return masterList

    # get count of neighbors that are alive
    def getLiveNeighbourCount(self, neighbours):
        count = 0
        for item in neighbours:
            cell = self.cells[item[0]][item[1]]
            if cell.state:
                count += 1
        return count

    def cacheNeighborInfo(self):
        for i in range(0, self.x):
            for j in range(0, self.y):
                self.neighbors[(i, j)] = self.getNeighbours(i, j)

    def shouldFlipState(self, x, y):
        # get the current cell
        cell = self.cells[x][y]
        liveCount = self.getLiveNeighbourCount(self.neighbors[(x, y)])
        flipState = False
        if cell.state:
            # cell is currently alive. keep it alive if it has 2 or 3 neighbors
            if not(liveCount == 2 or liveCount == 3):
                flipState = True
            else:
                flipState = False
        else:
            # cell is currently dead. make it alive it has 3 neighbors
            if liveCount == 3:
                flipState = True
            else:
                flipState = False

        return flipState

    def play(self, iterations):
        # cache neighbour info
        self.cacheNeighborInfo()

        cells_to_flip = []
        for x in range(0, iterations):
            # loop over all the cells
            for i in range(0, self.x):
                for j in range(0, self.y):
                    if self.shouldFlipState(i, j):
                        cells_to_flip.append([i, j])

            # update the states of the cells
            for item in cells_to_flip:
                cell = self.cells[item[0]][item[1]]
                cell.flip()

            # add a delay to activate animation
            time.sleep(5)


# globals
grid = Grid()


# get the index of the cell which on which the user clicked
def onClickFunction(x, y):

    for row in grid.cells:
        for cell in row:
            result = cell.isWithinBounds(x, y)
            if result:
                cell.flip()
                return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('x', type=int, default=15, help="x dimension")
    parser.add_argument('y', type=int, default=10, help="y dimension")
    parser.add_argument('i', type=int, default=5, help="generations")
    args = parser.parse_args()

    grid.draw(args.x, args.y)

    result = input(
        "press any key to start game after updating a few cells ! or q to quit \n")

    while result != "q":
        # play for N iterations
        grid.play(args.i)

        result = input(
            "press any key to start game after updating a few cells ! or q to quit \n")


if __name__ == "__main__":
    main()
