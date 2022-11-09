import random
import pygame
from pygame.locals import*
import sys
from tokenize import Double
from typing import Tuple

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


def drawPolygon(screen, points, color, isClosed=False):

    size = len(points)
    for i in range(1, size):
        pygame.draw.line(screen, color, transFormCoords(
            points[i-1]), transFormCoords(points[i]))
    if isClosed == True:
        pygame.draw.line(screen, color, transFormCoords(
            points[0]), transFormCoords(points[size-1]))


def plotPoints(screen, points, color, radius=1):
    for point in points:
        pygame.draw.circle(screen, color, transFormCoords(point), radius)


def getRandomPoints(x, factor=0.5):
    points = []
    for i in range(x):
        x = random.randrange(-width/2, width/2)*factor
        y = random.randrange(-height/2, height/2)*factor
        points.append((x, y))
    return points


def crossProduct(v1, v2):  # v1 -> v2 : -1 means clockwise
    return v1[0]*v2[1]-v1[1]*v2[0]


def solve(points):
    points.sort()

    upHull = points[:2]
    logs = []
    logs.append({"draw": upHull[:], "erase": []})
    for i in range(2, len(points)):

        while len(upHull) > 1 and crossProduct((points[i][0]-upHull[len(upHull)-1][0], points[i][1]-upHull[len(upHull)-1][1]), (upHull[len(upHull)-1][0]-upHull[len(upHull)-2][0], upHull[len(upHull)-1][1]-upHull[len(upHull)-2][1])) < 0:
            upHull.pop()
        upHull.append(points[i])
        logs.append({"draw": upHull[:], "erase": logs[len(logs)-1]["draw"]})

    points.reverse()
    lowHull = points[:2]

    logs.append({"draw": lowHull[:], "erase": []})
    for i in range(2, len(points)):

        while len(lowHull) > 1 and crossProduct((points[i][0]-lowHull[len(lowHull)-1][0], points[i][1]-lowHull[len(lowHull)-1][1]), (lowHull[len(lowHull)-1][0]-lowHull[len(lowHull)-2][0], lowHull[len(lowHull)-1][1]-lowHull[len(lowHull)-2][1])) < 0:
            lowHull.pop()
        lowHull.append(points[i])
        logs.append({"draw": lowHull[:], "erase": logs[len(logs)-1]["draw"]})

    hull = upHull[:]
    if upHull[len(upHull)-1] != lowHull[0]:
        hull.extend(lowHull[:])
    else:
        hull.extend(lowHull[1:])

    if hull[0] == hull[len(hull)-1]:
        hull.pop()

    return (hull, logs)


def main():
    noOfPoints = 100
    factor = 1/1.5
    points = getRandomPoints(noOfPoints, factor)

    (hull, logs) = solve(points)

    screen = pygame.display.set_mode((width, height))
    screen.fill(screen_color)
    drawAxes(screen)
    plotPoints(screen, points, (0, 0, 0), 2)
    pygame.display.flip()

    logs_iter = iter(logs)
    axesVisible = True
    autoIterate = False
    pygame.time.Clock()
    draw = False

    # print(logs)

    speed = 0
    tickAt = 500
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

            elif events.type == KEYUP and events.key == K_RIGHT:
                screen.fill(screen_color)
                # pygame.display.update()
                points = getRandomPoints(noOfPoints, factor)
                points = list(set(points))
                # print(points)
                # print("\n\n")
                plotPoints(screen, points, (0, 0, 0), 2)
                (hull, logs) = solve(points)

                # draw points
                plotPoints(screen, points, (0, 0, 0), 2)
                if axesVisible == True:
                    drawAxes(screen)
                logs_iter = iter(logs)
                pygame.display.update()

            elif events.type == KEYUP and events.key == K_r:  # restart
                screen.fill(screen_color)
                logs_iter = iter(logs)
                # draw points
                plotPoints(screen, points, (0, 0, 0), 2)
                if axesVisible == True:
                    drawAxes(screen)
                pygame.display.update()
            elif events.type == KEYDOWN and events.key == K_UP:
                speed += 1
            elif events.type == KEYDOWN and events.key == K_DOWN:
                speed -= 1
            elif events.type == KEYUP and (events.key == K_UP or events.key == K_DOWN):
                speed = 0

        if speed > 0 and pygame.time.get_ticks() % 200 == 0:
            speed += 1
            print("tickAt : "+str(tickAt))
        if speed < 0 and pygame.time.get_ticks() % 200 == 0:
            speed -= 1
            print("tickAt : "+str(tickAt))

        if speed != 0 and tickAt+speed > 0 and pygame.time.get_ticks() % 1000 == 0:
            tickAt += speed

        if autoIterate == True:
            if pygame.time.get_ticks() % tickAt == 0:
                draw = True
        if draw == True:
            log = next(logs_iter, None)
            # print(log)
            plotPoints(screen, points, (0, 0, 0), 2)
            if axesVisible == True:
                drawAxes(screen)
            if log != None:
                drawPolygon(screen, log["erase"], screen_color)
                drawPolygon(screen, log["draw"], (0, 0, 250))
                # print(log)
                pygame.display.flip()
            else:
                plotPoints(screen, hull, (255, 0, 0), 3)
                drawPolygon(
                    screen, hull, generateRandomColorExceptWhite(), True)
                pygame.display.flip()
            draw = False


main()
