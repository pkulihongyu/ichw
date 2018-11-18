'''planets_sub.py: draw 6 planets in the solar system
only normal functions used

__author__ = 'Li Hongyu'
__pkuid__ = '1700017785'
__email__ = 'hongyuli@pku.edu.cn'
'''

import turtle
import math


w = turtle.Screen()
t0, t1, t2, t3, t4, t5, t6 = (
	turtle.Turtle(), turtle.Turtle(), turtle.Turtle(), 
	turtle.Turtle(), turtle.Turtle(), turtle.Turtle(), 
	turtle.Turtle()
)


def init(t, a, e, focus_location, size, color):
	t.shape('circle')
	t.turtlesize(size, size)
	t.color(color)
	t.speed(0)

	c = a * e
	b = math.sqrt(a**2 - c**2)
	sign = 1 if focus_location == 'left' else -1
	orbit = (t, a, b, c, sign)

	t.up()
	t.goto(sign * c + a, 0)
	t.down()

	return orbit


def ellipse(t, a, b, c, sign, theta):
	t.goto(sign * c + a * math.cos(math.radians(theta)),
		   b * math.sin(math.radians(theta)))


def planets():
	init(t0, 0, 1, 'left', 1.2, 'yellow')

	datas = [
	(t1, 40, 0.5, 'right', 0.9, 'blue'), 
	(t2, 80, 0.4, 'right', 1, 'green'), 
	(t3, 120, 0, 'left', 1.1, 'red'), 
	(t4, 160, 0.1, 'left', 0.9, 'black'), 
	(t5, 200, 0.2, 'right', 0.8, 'orange'), 
	(t6, 250, 0.2, 'right', 0.8, 'lightblue')
	]
	orbits = []
	for data in datas:
		orbit = init(data[0], data[1], data[2], data[3], data[4], data[5])
		orbits.append(orbit)

	theta = 0
	while True:
		theta += 1
		for orbit in orbits:
			ellipse(orbit[0], orbit[1], orbit[2], orbit[3], orbit[4], 
				(theta / orbit[1]**2/3) * 10**5)


if __name__ == '__main__':
	planets()
	turtle.done()
