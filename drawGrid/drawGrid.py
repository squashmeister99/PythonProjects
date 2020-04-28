import turtle
import random
import argparse
from time import perf_counter, sleep

#constants
PEN_COLOR = "blue"
BG_COLOR = "white"
FILL_COLOR = "black"

' draws a box using turtle graphics'
def draw_box(t,x,y,size,fill_color = BG_COLOR):
    t.penup() # no drawing!
    t.goto(x,y) # move the pen to a different position
    t.pendown() # resume drawing
    
    t.fillcolor(fill_color)
    t.begin_fill()  # Shape drawn after this will be filled with this color!
 
    for i in range(0,4):
        t.forward(size) # move forward
        t.right(90) # turn pen right 90 degrees
 
    t.end_fill() 
 
 
def draw_board(args):
    x_dim = args.x
    y_dim = args.y
    iterations = args.i

    turtle.bgcolor(BG_COLOR)
    screen = turtle.Screen()
    board = turtle.Turtle()
    board.pencolor(PEN_COLOR)
    board.speed(0)
    screen.tracer(0, 0)
      
    for x in range(iterations):   
        
        
        t1_start = perf_counter()
        start_x = 0 # starting x position of the board
        start_y = 0 # starting y position of the board
        box_size = 15 # pixel size of each square in the board
        num_squares = x_dim*y_dim
        for i in range(0, x_dim ): 
            for j in range(0, y_dim ):
                square_color = FILL_COLOR if random.randrange(1, num_squares) > int(0.75*(num_squares)) else BG_COLOR         
                draw_box(board, start_x+j*box_size,start_y+i*box_size,box_size,square_color)

        screen.update()   # update the screen 
        t1_stop = perf_counter() 
        print("Elapsed time for loop: {0} sec", t1_stop - t1_start) 

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