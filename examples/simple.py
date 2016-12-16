#!/usr/bin/python3
"""\
Usage: simple.py

To run an example of a simple simulation using pytraffic
"""

from math import pi
from docopt import docopt
import pygame

from pytraffic.entities import World
from pytraffic.entities import Trajectory
from pytraffic.entities import Line
from pytraffic.entities import Arc
from pytraffic.entities import Point
from pytraffic.entities import Ball

from pytraffic.colors import RED, GREEN, WHITE



SCREEN_SIZE = (799, 535) # In pixels
TICK_PERIOD = 100  # In miliseconds


def simulation():

    # World width and height in meters
    world = World(188, 125.88)

    # Now let us define a trajectory
    trajectories = [ Trajectory(Line(Point(0, 69.18), Point(99.76, 69.18)),
                                Arc(Point(99.76, 65.88), 3.5, (3*pi/2, 2*pi)),
                                Line(Point(102.76, 65.88), Point(102.76, 0))),
                     Trajectory(Line(Point(188, 67.18), Point(103.53, 67.18)),
                                Arc(Point(104.29, 65.95), 1.53, (3*pi/2, pi)),
                                Line(Point(102.76, 65.65), Point(102.76, 0)))]


    # Add some vehicles (balls)
    ball1 = Ball(1, trajectories[0], RED)
    ball2 = Ball(1, trajectories[0], GREEN)
    speed1 = 15
    speed2 = 3

    background = pygame.image.load ("cruce.png")
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Simulador de tráfico")

    done = False
    clock = pygame.time.Clock()
    _time = 0

    while not done:

        clock.tick(1000/TICK_PERIOD)
        _time += (TICK_PERIOD/1000)

        speed2 = speed2 + 0.3
        ball1.set_speed(speed1)
        ball2.set_speed(speed2)

        screen.blit(background, background.get_rect())
        ball1.move(TICK_PERIOD/1000)
        ball2.move(TICK_PERIOD/1000)

        for trajectory in trajectories:
            trajectory.render(world, screen)

        ball1.render(world, screen)
        ball2.render(world, screen)

        print('elapsed time: %.4f seconds\r' % _time, end='')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.flip()


if __name__ == '__main__':
    ARGS = docopt(__doc__)

    simulation()
