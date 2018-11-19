'''planet.py: draw 6 planets in the solar system
not only normal function but also class used

__author__ = 'Li Hongyu'
__pkuid__ = '1700017785'
__email__ = 'hongyuli@pku.edu.cn'
'''

import turtle
import math


class planet():

    def __init__(self, a, e, focus_location, size, color):
        t = turtle.Turtle(shape='circle')
        t.turtlesize(size, size)
        t.color(color)
        t.speed(0)

        c = a * e
        b = math.sqrt(a**2 - c**2)
        sign = 1 if focus_location == 'left' else -1
        # assign 1 to sign if focus_location == 'left', else assign -1

        t.up()
        t.goto(sign * c + a, 0)
        t.down()

        self.t = t
        self.a = a
        self.b = b
        self.c = c
        self.sign = sign

    def orbit(self, theta):
        adjuster = 10**4 * 2
        angle = (theta / self.a**2/3) * adjuster
        # to adjust the angular velocity of each planet
        self.t.goto(
            self.sign * self.c + self.a * math.cos(math.radians(angle)),
            self.b * math.sin(math.radians(angle))
            )


def planets():
    Sun = planet(0, 1, 'left', 1.2, 'yellow')

    datas = [
        (40, 0.5, 'right', 0.7, 'blue'),
        (80, 0.4, 'right', 1, 'green'),
        (120, 0, 'left', 1.1, 'red'),
        (160, 0.1, 'left', 0.9, 'black'),
        (200, 0.2, 'right', 0.8, 'orange'),
        (250, 0.2, 'right', 0.8, 'lightblue')
    ]
    # to store the datas of each planet:
    # a(major semi-axis), e(eccentricity), focus_location, size, color

    Mercury, Venus, Earth, Mars, Jupiter, Saturn = [planet(
        data[0], data[1], data[2], data[3], data[4]) for data in datas]
    # List Comprehensions: create a planet object for each data in datas,
    # then assign them to the planets

    theta = 0
    while True:
        for p in [Mercury, Venus, Earth, Mars, Jupiter, Saturn]:
            theta += 1
            p.orbit(theta)


if __name__ == '__main__':
    w = turtle.Screen()
    planets()
    turtle.done()
