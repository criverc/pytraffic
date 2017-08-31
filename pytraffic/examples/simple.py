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


def adjust_speeds(balls):
    """To adjust speed of all balls"""

    for ball in balls:

        for other_ball in balls:

            if ball is other_ball:
                continue

            if ball.can_see(other_ball):
                speed_to_other_ball = ball.relative_speed_to(other_ball, TICK_PERIOD/1000)
                if speed_to_other_ball is not None:
                    if speed_to_other_ball < 0:
                        # we are closing! slow down
                        ball.set_speed(ball.speed*0.8)

                    elif speed_to_other_ball > 0:
                        # otherwise increase speed (follow)
                        ball.set_speed(ball.speed*1.05)
            else:
                ball.set_speed(min(ball.base_speed, ball.speed*1.05))


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
    red_ball = Ball(1, trajectories[0], color=RED, draw_cone=True)
    green_ball = Ball(1, trajectories[0], color=GREEN, draw_cone=True)

    background = pygame.image.load ("cruce.png")
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Simulador de tráfico")

    done = False
    clock = pygame.time.Clock()
    _time = 0

    # move red ball for a few seconds
    red_ball.set_speed(10)

    while _time < 3:
        clock.tick(1000/TICK_PERIOD)
        _time += (TICK_PERIOD/1000)
        screen.blit(background, background.get_rect())
        red_ball.move(TICK_PERIOD/1000)
        for trajectory in trajectories:
            trajectory.render(world, screen)
        red_ball.render(world, screen)
        pygame.display.flip()


    # now add green ball
    green_ball.set_speed(30)

    while not done:

        clock.tick(1000/TICK_PERIOD)
        _time += (TICK_PERIOD/1000)

        screen.blit(background, background.get_rect())
        red_ball.move(TICK_PERIOD/1000)
        green_ball.move(TICK_PERIOD/1000)

        for trajectory in trajectories:
            trajectory.render(world, screen)

        red_ball.render(world, screen)
        green_ball.render(world, screen)

        adjust_speeds([green_ball, red_ball])

        print('elapsed time: %.4f seconds\r' % _time, end='')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.flip()


if __name__ == '__main__':
    ARGS = docopt(__doc__)

    simulation()
