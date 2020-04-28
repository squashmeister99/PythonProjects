import turtle
import random
import argparse
from time import perf_counter, sleep

#constants
PEN_COLOR = "blue"
BG_COLOR = "white"
FILL_COLOR = "black"
BOX_SIZE = 16
RADIUS = BOX_SIZE/4

# draws a circle of the specified radius
def draw_circle(t, x, y, fill_color = BG_COLOR):
    t.penup() # no drawing!
    t.goto(x,y) # move the pen to a different position
    t.pendown() # resume drawing
    t.pen(pencolor="purple" , fillcolor = "orange", pensize = 10, speed = 0 )
    t.begin_fill()
    t.circle(RADIUS)
    t.end_fill()
    return


' draws a box using turtle graphics'
def draw_box(t,x,y,size,fill_color = BG_COLOR):
    t.penup() # no drawing!
    t.goto(x,y) # move the pen to a different position
    t.pendown() # resume drawing
    
    for i in range(0,4):
        t.forward(size) # move forward
        t.right(90) # turn pen right 90 degrees
 
    return
 
def playGame(iterations, x_dim, y_dim):
    for x in range(iterations):   
           
        t1_start = perf_counter()       
        num_squares = x_dim*y_dim    
        t1_stop = perf_counter() 
        print("Elapsed time for loop: {0} sec", t1_stop - t1_start)

def setupScreen():
    screen = turtle.Screen()
    screen.bgcolor(BG_COLOR)
    screen.title('Game of Life')
    screen.tracer(0, 0)
    return screen

def setupGridTurtle():
    t = turtle.Turtle()
    t.hideturtle()
    t.pen(pencolor = PEN_COLOR, speed = 0)
    return t

def draw_board(args):

    screen = setupScreen()
    t = setupGridTurtle()
    
    start_x = 0 # starting x position of the board
    start_y = 0 # starting y position of the board

    x_dim = args.x
    y_dim = args.y
    iterations = args.i

    for i in range(0, x_dim ): 
            for j in range(0, y_dim ):    
                draw_box(t, start_x+j*BOX_SIZE, start_y+i*BOX_SIZE, BOX_SIZE)

    
    screen.update()   # update the screen 
      
    #playGame(iterations, x_dim, y_dim) 

    screen.exitonclick()

def main():

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('x', type=int, default=15, help="x dimension")
    parser.add_argument('y', type=int, default=10, help="y dimension")
    parser.add_argument('i', type=int, default=5, help="iterations")
    args = parser.parse_args()
    
    draw_board(args)

    

if __name__ == "__main__":
    main()