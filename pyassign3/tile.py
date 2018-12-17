'''tile.py: tile the wall

__author__ = 'Li Hongyu'
__pkuid__ = '1700017785'
__email__ = 'hongyuli@pku.edu.cn'
'''

import turtle


def tile(m, n, a, b):
    '''tile the wall'''

    def start(wall):
        '''find the starting point: return column j, row i;
        return None if the wall has been totally tiled'''
        for j in range(n):
            for i in range(m):
                if wall[j][i] == 0:
                    return j, i

    def check(direction, a, b):
        '''check if the pile can be piled horizontally/vertically
        direction: 'h'(means horizontally) / 'v'(means vertically)'''
        if direction != 'h':
            a, b = b, a
        try:
            for j in range(j0, j0 + b):
                for i in range(i0, i0 + a):
                    if wall[j][i] == 1:
                        return False
            return True
        except IndexError:
            return False

    def work(mode, direction, a, b):
        '''do/undo the work of tiling
        (change the state of recording points)
        mode: 'd'(means do the work of tiling) -> from 0 to 1
           or 'u'(means undo) -> from 1 to 0
        direction: 'h'(means horizontally) / 'v'(means vertically)'''
        if direction != 'h':
            a, b = b, a
        if mode == 'd':
            for j in range(j0, j0 + b):
                for i in range(i0, i0 + a):
                    wall[j][i] = 1
            answer.append(tuple(
                sorted([(m * j + i) for i in range(i0, i0 + a)
                        for j in range(j0, j0 + b)])))
        else:
            for j in range(j0, j0 + b):
                for i in range(i0, i0 + a):
                    wall[j][i] = 0
            answer.pop()

    if not start(wall):  # the wall has been completely tiled
        results.append(answer[:])
        return

    j0, i0 = start(wall)

    if check('h', a, b):
        work('d', 'h', a, b)
        tile(m, n, a, b)
        work('u', 'h', a, b)

    if a != b and check('v', a, b):
        # avoid repetitive answers when the tile is square
        work('d', 'v', a, b)
        tile(m, n, a, b)
        work('u', 'v', a, b)


def main(m, n, a, b):
    '''call the function tile and print the answers'''
    tile(m, n, a, b)
    for i in range(len(results)):
        print(i, results[i])


def draw_wall(m, n):
    '''draw the wall with grid lines'''

    def number():
        t.up()
        for j in range(n):
            for i in range(m):
                t.goto((i + 0.5) * side, (j + 0.5) * side)
                t.write(m * j + i)

    t.pencolor('blue')
    # draw the horizontal lines
    for i in range(n):
        angle = 90 * (-1)**i
        t.forward(m * side)
        t.left(angle)
        t.forward(side)
        t.left(angle)
    t.forward(m * side)
    t.left(angle)
    # draw the vertical lines
    for j in range(m):
        angle = 90 * (-1)**(j + n)
        t.forward(n * side)
        t.right(angle)
        t.forward(side)
        t.right(angle)
    t.forward(n * side)

    number()

    # go back to the origin
    t.up()
    t.home()
    t.down()


def draw_tiles(results):
    '''draw the boundaries of all the tiles'''

    def rectangle(pile):
        '''draw the boundary of one tile'''

        # go to the lower left cornor of the rectangle
        t.up()
        t.goto(pile[0] % m * side, pile[0]//m * side)
        t.down()
        # draw the rectangle
        # (find if the tile is placed horizontally / vertically by calculating)
        small, large = min(a, b), max(a, b)
        if pile[0] + large - 1 in pile and large <= m:  # length >= width
            length, weigth = large, small
        else:
            length, weigth = small, large

        for i in range(2):
            t.forward(length * side)
            t.left(90)
            t.forward(weigth * side)
            t.left(90)
        # go back to the origin
        t.up()
        t.home()
        t.down()

    t.pencolor('black')
    t.pensize(5)
    # choose which kind of piling method to be visulized
    if results:
        no = int(w.numinput('Visualization',
                            'Input number of 0 - {}'.format(len(results) - 1),
                            None, 0, len(results) - 1)
                 )
        result = results[no]
        for pile in result:  # draw the boundary of each tile
            rectangle(sorted(pile))
    else:
        print('No proper method of piling found!')


def main_draw():
    turtle.hideturtle()
    # use the larger coordinate to prevent the graph from:
    # 1) beyong the screen; 2) be distorted into rectangle from square
    border = max(m * side + 50, n * side + 50)
    w.setworldcoordinates(-50, -50, border, border)
    # w.screensize(2 * m * side + 100, 2 * n * side + 100)
    t.speed(0)
    draw_wall(m, n)
    draw_tiles(results)
    turtle.done()


if __name__ == '__main__':
    m, n, a, b = int(input('m: ')), int(
        input('n: ')), int(input('a: ')), int(input('b: '))
    wall = [[0] * m for i in range(n)]
    # be cautious that list repetition means reference but not copy!!!!!
    results, answer = [], []
    main(m, n, a, b)

    side = 50
    w = turtle.Screen()
    t = turtle.Turtle()
    main_draw()
