#!/usr/bin/python3
"""\
Usage: multiple.py

To run an example of a simple simulation using pytraffic.
In this example there are multiple balls, they keep coming
out at a regular pace with a constant speed.
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
                speed_to_other = ball.relative_speed_to(other_ball, TICK_PERIOD/1000)
                distance_to_other = ball.distance_to(other_ball)
                if speed_to_other is not None:
                    if speed_to_other < 0:
                        # we are closing! slow down
                        ball.set_speed(ball.speed*(1/distance_to_other))

                    elif speed_to_other > 0:
                        # otherwise increase speed (follow)
                        ball.set_speed(ball.speed*1.03)
            else:
                ball.set_speed(min(ball.base_speed, ball.speed*1.03))



class BallShooter(object):


    def __init__(self, trajectory):
        self.__time = 0
        self.__PERIOD = 5
        self.__SPEED = 15
        self.__trajectory = trajectory


    def __really_spawn(self):
        ball = Ball(1, self.__trajectory, color=RED, draw_cone=True)
        ball.set_speed(15)

        return ball


    def spawn(self, tick):
        ball=None

        if self.__time == 0:
            ball = self.__really_spawn()

        module_a = self.__time % self.__PERIOD
        self.__time += tick
        module_b = self.__time % self.__PERIOD

        if module_b < module_a:
            ball = self.__really_spawn()

        return ball


def remove_balls_that_exited(balls):
    _ = []
    for ball in balls:
        if ball.center is not None:
            _.append(ball)

    return _


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

    shooter = BallShooter(trajectories[0])

    # Add some vehicles (balls)
    balls = []

    background = pygame.image.load ("cruce.png")
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Simulador de tráfico")

    done = False
    clock = pygame.time.Clock()
    _time = 0


    while not done:

        clock.tick(1000/TICK_PERIOD)
        _time += (TICK_PERIOD/1000)

        screen.blit(background, background.get_rect())

        for trajectory in trajectories:
            trajectory.render(world, screen)

        ball = shooter.spawn(TICK_PERIOD/1000)
        if ball is not None:
            balls.append(ball)

        for ball in balls:
            ball.move(TICK_PERIOD/1000)
            ball.render(world, screen)

        adjust_speeds(balls)
        balls = remove_balls_that_exited(balls)

        print('number of balls: %d, elapsed time: %.4f seconds\r' % (len(balls), _time), end='')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.flip()


if __name__ == '__main__':
    ARGS = docopt(__doc__)

    simulation()
