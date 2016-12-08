#!/usr/bin/python3
"""\
Usage: simple.py

To run an example of a simple simulation using pytraffic
"""

import pygame
from math import pi
from docopt import docopt

from pytraffic.entities import World
from pytraffic.entities import Trajectory
from pytraffic.entities import Line
from pytraffic.entities import Arc
from pytraffic.entities import Point
from pytraffic.entities import Ball

from pytraffic.colors import RED, GREEN, WHITE



SCREEN_SIZE = (640, 480) # In pixels
TICK_PERIOD = 100  # In miliseconds


def simulation():

    # World width and height in meters
    world = World(1000, 1000)  

    # Now let us define a trajectory
    trajectory = Trajectory(Line(Point(0, 50), Point(600, 50)), 
                            Arc(Point(600, 100), 50, (pi/2, 0)),
                            Line(Point(650, 100), Point(650, 600)),
                            Arc(Point(700, 600), 50, (pi, 3*pi/2)),
                            Line(Point(700, 650), Point(800, 650)))

    # Add some vehicles (balls)
    ball1 = Ball(3, trajectory, RED)
    ball2 = Ball(3, trajectory, GREEN)
    speed1=15
    speed2=0

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Simulador de tráfico")

    done = False
    clock = pygame.time.Clock()
    _time = 0

    while not done:
        
        clock.tick(1000/TICK_PERIOD)
        _time += (TICK_PERIOD/1000)

        speed1 = speed1 + 1
        speed2 = speed2 + 2
        ball1.set_speed(speed1)
        ball2.set_speed(speed2)

        screen.fill(WHITE)
        ball1.move(TICK_PERIOD/1000)
        ball2.move(TICK_PERIOD/1000)

        trajectory.render(world, screen)
        ball1.render(world, screen)
        ball2.render(world, screen)

        print('elapsed time: %.4f seconds\r' % _time, end='')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True

        pygame.display.flip()


if __name__ == '__main__':
    args = docopt(__doc__)

    simulation()
