import turtle

pen = turtle.Turtle()

def curve():
    for i in range(200):
        pen.right(1)
        pen.forward(1)

def heart():
    pen.fillcolor('red')
    pen.begin_fill()
    pen.left(140)
    pen.forward(113)
    curve()
    pen.left(120)
    pen.forward(112)
    curve()
    pen.end_fill()

def text1():
    pen.up()
    pen.setpos(-68, 95)
    pen.down()
    pen.color('yellow')
    pen.write("I LOVE YOU", font=("Arial", 16, "bold"))

# Llamadas a las funciones
heart()
text1()
pen.ht()

turtle.done()