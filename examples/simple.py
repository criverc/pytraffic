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



SCREEN_SIZE = (1266, 807) # In pixels
TICK_PERIOD = 100  # In miliseconds


def simulation():

    # World width and height in meters
    world = World(298, 190)

    # Now let us define a trajectory
    trajectory = Trajectory(Line(Point(0.23, 29.64), Point(13.88, 39.76)),
                            Line(Point(13.88, 39.76), Point(53.17, 62.35)),
                            Line(Point(53.17, 62.35), Point(156.94, 99.53)),
                            Arc(Point(157.312, 94.07), 6, (0.08 + 3*pi/2, 3*pi/2 + pi/4)),
                            Line(Point(160.84, 98.71), Point(196, 0.5)))

    # Add some vehicles (balls)
    ball1 = Ball(1, trajectory, RED)
    ball2 = Ball(1, trajectory, GREEN)
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
