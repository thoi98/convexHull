from ast import List
import sys
from tokenize import Double
from typing import Tuple
import pygame
from pygame.locals import*
from math import sqrt, sin, acos, cos
import random

width = 1500
height = 700
screen_color = (200, 200, 200)
line_color = (255, 0, 0)


def generateRandomColorExceptWhite():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(
        0, 255) if r <= 150 and g <= 150 else random.randint(0, 100)
    return (r, g, b)


def transFormCoords(coord):
    return (width/2 + coord[0], height/2 - coord[1])


def drawAxes(screen, color=(100, 100, 100)):
    pygame.draw.line(screen, color, transFormCoords(
        (0, -height/2)), transFormCoords((0, height/2)))
    pygame.draw.line(screen, color, transFormCoords(
        (-width/2, 0)), transFormCoords((width/2, 0)))


def drawNewXAxis(screen, A, B):
    a = B[1] - A[1]
    b = A[0] - B[0]
    # c = a*(A[0]) + b1(A[1])

    p1: Tuple
    p2: Tuple
    p3: Tuple
    p4: Tuple
    if a > b:
        p1 = (-1*(b*height)/(2*a), height/2)
        p2 = ((b*height)/(2*a), -height/2)

        p3 = ((a*height)/(2*b), height/2)
        p4 = (-1*(a*height)/(2*b), -height/2)
    else:
        p1 = (width/2, -1*(a*width)/(2*b))
        p2 = (-width/2, (a*width)/(2*b))

        p3 = (width/2, (b*width)/(2*a))
        p4 = (-width/2, -1*(b*width)/(2*a))
    pygame.draw.line(screen, (250, 0, 0), transFormCoords(p1),
                     transFormCoords(p2))
    pygame.draw.line(screen, (0, 250, 0), transFormCoords(p3),
                     transFormCoords(p4))


def drawInfLine(screen, color, A, B, origin=False):
    a = B[1] - A[1]
    b = A[0] - B[0]
    c = a*(A[0]) + b*(A[1])

    if origin:
        c = 0

    p1: Tuple
    p2: Tuple
    if a > b:
        p1 = (c - ((b*height)/(2*a)), height/2) if a != 0 else (c, height/2)
        p2 = (c + ((b*height)/(2*a)), -height/2) if a != 0 else (c, -height/2)
    else:
        p1 = (width/2, c - ((a*width)/(2*b))) if b != 0 else (width/2, c)
        p2 = (-width/2, c + ((a*width)/(2*b))) if b != 0 else (-width/2, c)
    pygame.draw.line(screen, color, transFormCoords(p1),
                     transFormCoords(p2))


def drawPolygon(screen, points, color, isClosed=False):

    size = len(points)
    for i in range(1, size):
        pygame.draw.line(screen, color, transFormCoords(
            points[i-1]), transFormCoords(points[i]))
    if isClosed == True:
        pygame.draw.line(screen, color, transFormCoords(
            points[0]), transFormCoords(points[size-1]))


def getPerpendicularLine(A, B):
    a = B[1] - A[1]
    b = A[0] - B[0]
    a_ = -b
    b_ = a

    c = a_*(A[0]) + b_*(A[1])

    A_ = (0, c/b_) if b_ != 0 else (c/a_, 0)
    B_ = (1, (c-a_)/(b_)) if b_ != 0 else (c/a_, 1)
    return (A_, B_)


def plotPoints(screen, points, color, radius=1):
    for point in points:
        pygame.draw.circle(screen, color, transFormCoords(point), radius)


def getTilt(A, B):
    a = B[1] - A[1]
    b = A[0] - B[0]

    if(a > 0 and b > 0) or (a < 0 and b < 0):
        return -1
    elif (a > 0 and b < 0) or (a < 0 and b > 0):
        return 1
    else:
        return 0


def convertCoords(point, A, B):
    x1 = A[0]
    y1 = A[1]
    x2 = B[0]
    y2 = B[1]

    dx21 = x2-x1
    dy21 = y2-y1

    dx34 = 1
    dy34 = 0
    m12 = sqrt(dx21*dx21 + dy21*dy21)
    m13 = sqrt(dx34*dx34 + dy34*dy34)
    theta = acos((dx21*dx34 + dy21*dy34) / (m12 * m13))
    # print("theta :"+str(theta*57.2958))
    tilt = getTilt(A, B)
    x_: Double
    y_: Double
    if tilt == -1:
        x_ = point[0]*cos(theta)-point[1]*sin(theta)
        y_ = point[1]*cos(theta)+point[0]*sin(theta)
    else:  # elif tilt == 1:
        x_ = point[0]*cos(theta)+point[1]*sin(theta)
        y_ = -point[1]*cos(theta)+point[0]*sin(theta)
    return (x_, y_)


def convertCoordsList(points, A, B):
    # a = B[1] - A[1]
    # b = A[0] - B[0]
    x1 = A[0]
    y1 = A[1]
    x2 = B[0]
    y2 = B[1]

    dx21 = x2-x1
    dy21 = y2-y1

    dx34 = 1
    dy34 = 0
    m12 = sqrt(dx21*dx21 + dy21*dy21)
    m13 = sqrt(dx34*dx34 + dy34*dy34)
    theta = acos((dx21*dx34 + dy21*dy34) / (m12 * m13))
    print("theta :"+str(theta*57.2958))
    result = []
    tilt = getTilt(A, B)
    for point in points:
        x_: Double
        y_: Double
        if tilt == -1:
            x_ = point[0]*cos(theta)-point[1]*sin(theta)
            y_ = point[1]*cos(theta)+point[0]*sin(theta)
        else:  # elif tilt == 1:
            x_ = point[0]*cos(theta)+point[1]*sin(theta)
            y_ = -point[1]*cos(theta)+point[0]*sin(theta)
        result.append((x_, y_))
    return result


def getRandomPoints(x, factor=0.5):
    points = []
    for i in range(x):
        x = random.randrange(-width/2, width/2)*factor
        y = random.randrange(-height/2, height/2)*factor
        points.append((x, y))
    return points


def getLeftRightBounds(points, A, B):
    (A_, B_) = getPerpendicularLine(A, B)

    def convert(point):
        return convertCoords(point, A_, B_)

    xleft = (points[0], points[0])
    xright = (points[0], points[0])

    for i in range(1, len(points)):
        if convert(xleft[0])[0] > convert(points[i])[0]:
            xleft = (points[i], points[i])
        elif convert(xleft[0])[0] == convert(points[i])[0]:
            if convert(xleft[1])[1] < convert(points[i])[1]:
                xleft = (xleft[0], points[i])
            elif convert(xleft[0])[1] > convert(points[i])[1]:
                xleft = (points[i], xleft[1])

        if convert(xright[0])[0] < convert(points[i])[0]:
            xright = (points[i], points[i])
        elif convert(xright[0])[0] == convert(points[i])[0]:
            if convert(xright[1])[1] < convert(points[i])[1]:
                xright = (xright[0], points[i])
            elif convert(xright[0])[1] > convert(points[i])[1]:
                xright = (points[i], xright[1])
    # if A == xleft or B == xright or A == xright or B == xleft:
    #     return (A, B)
    return (xleft, xright)


def insertIntoList(lst, pointBefore, pointsToInsert):
    pointsToInsert = list(set(pointsToInsert))
    i = lst.index(pointBefore)+1
    for p in pointsToInsert:
        lst.insert(i, p)
        i += 1


def rubberBand(points, A, B, direction, logs=[]):

    if A[1] == B[1]:    # doing this because sometimes rotation gives slightly different values
        direction = 1
    if A == B:
        return []
    next: Tuple
    if direction == -1:  # meaning _|_ of this line is tilting left
        (next, _) = getLeftRightBounds(points, A, B)
    else:
        (_, next) = getLeftRightBounds(points, A, B)

    if next[0] == A or next[0] == B or next[1] == A or next[1] == B:
        return []

    if len(logs) != 0:  # notEmpty
        nextLogDraw = logs[-1]["draw"][:]
        nextLogErase = logs[-1]["draw"][:]

        insertIntoList(nextLogDraw, A, list(next))
        logs.append({"draw": nextLogDraw, "erase": nextLogErase})

    left = []
    right = []
    if direction == -1:
        left = rubberBand(points, A, next[0], direction, logs)
        right = rubberBand(points, next[1], B, direction, logs)
    else:
        left = rubberBand(points, A, next[1], direction, logs)
        right = rubberBand(points, next[0], B, direction, logs)
    result = []
    result.extend(left)
    if next[0] == next[1]:
        result.extend([next[0]])
    else:
        if direction == -1:
            result.extend([next[0], next[1]])
        else:
            result.extend([next[1], next[0]])
    result.extend(right)
    return result


def solve(screen, points):
    (xleft, xright) = getLeftRightBounds(points, (0, 0), (0, 1))
    (ydown, yup) = getLeftRightBounds(points, (0, 0), (1, 0))

    up_left = [xleft[1]]
    logs_upLeft = [{"draw": [xleft[1], yup[0]], "erase":[]}]
    up_left.extend(rubberBand(points, xleft[1], yup[0], -1, logs_upLeft))
    up_left.extend([yup[0]])

    down_left = [xleft[0]]
    logs_downLeft = [{"draw": [xleft[0], ydown[0]], "erase":[]}]
    down_left.extend(rubberBand(points, xleft[0], ydown[0], -1, logs_downLeft))
    down_left.extend([ydown[0]])

    up_right = [yup[1]]
    logs_upRight = [{"draw": [yup[1], xright[1]], "erase":[]}]
    up_right.extend(rubberBand(points, yup[1], xright[1], 1, logs_upRight))
    up_right.extend([xright[1]])

    down_right = [ydown[1]]
    logs_downRight = [{"draw": [ydown[1], xright[0]], "erase":[]}]
    down_right.extend(rubberBand(
        points, ydown[1], xright[0], 1, logs_downRight))
    down_right.extend([xright[0]])

    hull = []
    hull.extend(up_left)
    hull.extend(up_right)
    hull.extend(list(reversed(down_right)))
    hull.extend(list(reversed(down_left)))

    logs = []
    if xleft[0] != xleft[1]:
        logs.append({"draw": list(xleft), "erase": []})
    if xright[0] != xright[1]:
        logs.append({"draw": list(xright), "erase": []})
    if yup[0] != yup[1]:
        logs.append({"draw": list(yup), "erase": []})
    if ydown[0] != ydown[1]:
        logs.append({"draw": list(ydown), "erase": []})
    logs.extend(logs_upLeft[:1])
    logs.extend(logs_downLeft[:1])
    logs.extend(logs_upRight[:1])
    logs.extend(logs_downRight[:1])
    logs.extend(logs_upLeft[1:])
    logs.extend(logs_downLeft[1:])
    logs.extend(logs_upRight[1:])
    logs.extend(logs_downRight[1:])

    return (hull, logs)


def write(screen, dataToWrite, pos=(2, 0), color=(0, 0, 0), fontSize=11, lineSpace=1):
    myfont = pygame.font.SysFont("monospace", fontSize)
    lines = dataToWrite.split("\n")
    for i in range(len(lines)):
        label = myfont.render(lines[i], 1, color)
        screen.blit(label, (pos[0], pos[1]+(i*lineSpace)+(fontSize*(i+1))))
    pygame.display.update()


def main():
    pygame.display.set_caption('Convex Hull')
    pygame.font.init()

    screen = pygame.display.set_mode((width, height))
    screen.fill(screen_color)
    drawAxes(screen)

    write(screen, "SPACE - next iteration\nRETURN - auto iterate\nESC - exit\nR - Restart\nRight arrow -> Generate new set of points",
          color=(0, 150, 50))

    # region test

    points = getRandomPoints(100, 1/2)
    points = list(set(points))
    print(points)
    print("\n\n")
    plotPoints(screen, points, (0, 0, 0), 1)
    (hull, logs) = solve(screen, points)

    # endregion
    pygame.display.flip()

    logs_iter = iter(logs)
    axesVisible = True
    autoIterate = False
    pygame.time.Clock()
    draw = False

    while True:
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)
            elif events.type == KEYDOWN and events.key == K_ESCAPE:
                return
            elif events.type == KEYUP and events.key == K_SPACE:
                draw = True
            elif events.type == KEYUP and events.key == K_x:
                if axesVisible == True:
                    drawAxes(screen, screen_color)
                else:
                    drawAxes(screen)
                axesVisible = not axesVisible
                pygame.display.update()

            elif events.type == KEYUP and events.key == K_RETURN:
                autoIterate = not autoIterate
            elif events.type == KEYUP and events.key == K_r:  # restart
                logs_iter = iter(logs)
                # erase big red points on hull
                plotPoints(screen, hull, screen_color, 3)
                # erase edges of hull
                drawPolygon(screen, hull, screen_color)
                # draw points
                plotPoints(screen, points, (0, 0, 0), 1)
                pygame.display.update()

            elif events.type == KEYUP and events.key == K_RIGHT:
                # erase points
                plotPoints(screen, points, screen_color, 3)
                # erase edges of hull
                drawPolygon(screen, hull, screen_color)

                points = getRandomPoints(100, 1/2)
                points = list(set(points))
                print(points)
                print("\n\n")
                plotPoints(screen, points, (0, 0, 0), 1)
                (hull, logs) = solve(screen, points)

                # draw points
                plotPoints(screen, points, (0, 0, 0), 1)
                if axesVisible == True:
                    drawAxes(screen)
                logs_iter = iter(logs)
                pygame.display.update()

        if autoIterate == True:
            if pygame.time.get_ticks() % 1000 == 0:
                draw = True
        if draw == True:
            log = next(logs_iter, None)
            if log != None:
                drawPolygon(screen, log["erase"], screen_color)
                drawPolygon(screen, log["draw"], (0, 0, 250))
                print(log)
                pygame.display.flip()
            else:
                plotPoints(screen, hull, (255, 0, 0), 3)
                drawPolygon(screen, hull, generateRandomColorExceptWhite())
                pygame.display.flip()
            draw = False


main()
