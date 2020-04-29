import turtle
import argparse

# constants
BG_COLOR = "white"
PEN_COLOR = "blue"
BOX_SIZE = 32

class Cell:

    # constants 
    FILL_COLOR = "black"
    BG_COLOR = "white"
    RADIUS = BOX_SIZE/4

    def __init__(self, t, xmin, ymin, xmax, ymax, state = False):
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
        self.state = not(self.state) # flip the state
        if self.state:
            color = Cell.FILL_COLOR
        else:
            color = Cell.BG_COLOR

        self.t.penup()
        self.t.goto(self.xmin + self.size/2, self.ymin + self.size/4)
        self.t.pendown()
        self.t.pen(pensize=2, pencolor= color, fillcolor=color, speed=0)
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
        start_x = 0
        start_y = 0
        for i in range(0, x):
            nestedList = []
            for j in range(0, y):
                xmin = start_x + j*BOX_SIZE;
                xmax = start_x + (j + 1)*BOX_SIZE;
                ymin = start_y + i*BOX_SIZE;
                ymax = start_y + (i + 1)*BOX_SIZE;
                cell = Cell(self.t, xmin, ymin, xmax, ymax, False)
                cell.draw()
                nestedList.append(cell)

            self.cells.append(nestedList)
        self.t.getscreen().update()   # update the screen


# globals
grid = Grid()

# get the index of the cell which on which the user clicked
def onClickFunction(x, y):

    for row in grid.cells:
        for cell in row:
            result =  cell.isWithinBounds(x, y)
            if result:
                cell.flip()
                return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('x', type=int, default=15, help="x dimension")
    parser.add_argument('y', type=int, default=10, help="y dimension")
    parser.add_argument('i', type=int, default=5, help="iterations")
    args = parser.parse_args()

    grid.draw(args.x, args.y)
    input("press any key to quit !")





if __name__ == "__main__":
    main()
