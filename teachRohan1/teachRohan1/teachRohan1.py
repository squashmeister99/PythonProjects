# Author: Rajesh Vaidya
# creeation date:  May 21, 2019
import turtle
t = turtle.Pen()
turtle.bgcolor("brown")
colors = ["red", "blue", "green", "yellow", "purple", "coral"]
for x in range(50):
    t.pencolor(colors[x%len(colors)])
    t.forward(x)
    t.left(74)
