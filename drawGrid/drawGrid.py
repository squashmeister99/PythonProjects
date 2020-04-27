import turtle
import random
import argparse


def draw_box(t,x,y,size,fill_color = 'white'):
    t.penup() # no drawing!
    t.goto(x,y) # move the pen to a different position
    t.pendown() # resume drawing
    
    t.fillcolor(fill_color)
    t.begin_fill()  # Shape drawn after this will be filled with this color!
 
    for i in range(0,4):
        t.forward(size) # move forward
        t.right(90) # turn pen right 90 degrees
 
    t.end_fill() # Go ahead and fill the rectangle!
 
 
def draw_board(board, screen, x_dim, y_dim, iterations = 10):
    for x in range(iterations):
        start_x = 0 # starting x position of the chess board
        start_y = 0 # starting y position of the chess board
        box_size = 15 # pixel size of each square in the chess board

        for i in range(0, x_dim): # 8x8 chess board
            for j in range(0, y_dim):
                square_color = 'black' if random.randrange(1, x_dim*y_dim) > int(0.9*(x_dim*y_dim)) else 'white' 
                
                draw_box(board,start_x+j*box_size,start_y+i*box_size,box_size,square_color)
        screen.update()   # update the screen     

def main():
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('x', type=int, default=15, help="x dimension")
    parser.add_argument('y', type=int, default=10, help="y dimension")
    parser.add_argument('i', type=int, default=5, help="iterations")
    args = parser.parse_args()

    screen = turtle.Screen()
    screen.tracer(0, 0)
    board = turtle.Turtle()
    board.speed(0)
    draw_board(board, screen, args.x, args.y, args.i)
    screen.exitonclick() 
    

if __name__ == "__main__":
    main()