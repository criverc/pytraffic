#!/usr/bin/python3
"""\
Usage: multiple.py [--with-bike-lane] [--save=dir]

To run an example of a simple simulation using pytraffic.
In this example there are multiple balls, they keep coming
out at a regular pace with a constant speed.

Options:
--with-bike-lane   Do simulation with bike lane
--save=dir         Directory into which save a movie of the simulation
"""

from math import pi
from docopt import docopt
from collections import defaultdict
import pygame
from numpy.random import normal

from pytraffic.entities import World
from pytraffic.entities import Trajectory
from pytraffic.entities import Line
from pytraffic.entities import Arc
from pytraffic.entities import Point
from pytraffic.entities import Ball

from pytraffic.colors import RED, GREEN, WHITE, BLUE, BLACK


pygame.init()

SCREEN_SIZE = (799, 535) # In pixels
SPEED_UP = 1
MAX_DECELERATION = -0.9 * 9.81

FONT = pygame.font.SysFont("monospace", 19)


def tick_period(speed_up):

    return ({ 1: 20, 2: 40, 3: 80, 4: 100, 5: 120, 6: 160 }[speed_up])/(1000*speed_up)


def acceleration(distance, rel_speed, speed_up):

    acc = 0.8*(9.81/distance)*(rel_speed/speed_up)
    if acc < 0:
        return max(MAX_DECELERATION, acc) * speed_up * speed_up
    else:
        return min(-MAX_DECELERATION, acc) * speed_up * speed_up


def adjust_speeds(balls, speed_up):
    """To adjust speed of all balls"""

    for ball in balls:

        unimpeded = True

        for other_ball in balls:

            if ball is other_ball:
                continue

            if ball.can_see(other_ball):
                unimpeded = False
                speed_to_other = ball.relative_speed_to(other_ball, tick_period(speed_up))
                if speed_to_other is not None:
                    if speed_to_other < 0:
                        # we are closing! slow down
                        distance_to_other = ball.distance_to(other_ball)
                        acc = acceleration(distance_to_other, speed_to_other, speed_up)
                        new_speed = acc * tick_period(speed_up) + ball.speed
                        ball.set_speed(max(0, new_speed))

        if unimpeded:
            ball.set_speed(min(ball.base_speed,
                               0.2 * 9.81 * speed_up * speed_up * tick_period(speed_up)
                               + ball.speed))


def get_colliding_ball(ball, balls):

    for other_ball in balls:
        if ball is other_ball:
            continue

        if ball.intersects(other_ball):
            return other_ball


def get_visible_ball(ball, balls):

    for other_ball in balls:
        if ball is other_ball:
            continue

        if ball.intersects(other_ball) or ball.can_see(other_ball):
            return other_ball


collision_statistics = defaultdict(int)

def remove_balls_that_collide(balls):

    _ = []

    for ball in balls:

        colliding_ball = get_colliding_ball(ball, balls)

        if colliding_ball is not None:
            tags = sorted([ball.tag, colliding_ball.tag])
            collision_statistics['{}_{}'.format(*tags)] += 0.5

        else:
            _.append(ball)

    return _


def print_statistics(screen):

    label_position = [SCREEN_SIZE[0]*.10, SCREEN_SIZE[1]*0.7]
    for key, value in collision_statistics.items():
        label = FONT.render('{} collisions: {}'.format(key.upper(), int(value)), 1, WHITE, BLACK)
        screen.blit(label, label_position)
        label_position[1] += 20  # TODO: Use line height, do not hardcode


class BallShooter(object):


    def __init__(self, speed_up, trajectory, period, mean, spread, color):
        self.__time = 0
        self.__speed_up = speed_up
        self.__PERIOD = period/speed_up
        self.__trajectory = trajectory
        self.__mean = mean
        self.__spread = spread
        self.__color = color


    def __really_spawn(self):
        ball = Ball(1, self.__trajectory, color=self.__color, draw_cone=True)
        ball.set_speed(normal(self.__mean, self.__spread)*self.__speed_up)

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


def simulation(with_bike_lane, save_dir, speed_up):

    fps = speed_up/tick_period(speed_up)

    print('desired FPS: {}'.format(fps))

    # World width and height in meters
    world = World(188, 125.88)

    # Now let us define a trajectory
    trajectories = [ Trajectory(Line(Point(0, 69.18), Point(98.76, 69.18)),
                                Arc(Point(98.76, 65.88), 3.5, (3*pi/2, 2*pi)),
                                Line(Point(101.76, 65.88), Point(101.76, 0))),
                     Trajectory(Line(Point(0, 69.18), Point(101.76, 69.18)),
                                Arc(Point(101.76, 65.88), 3.5, (3*pi/2, 2*pi)),
                                Line(Point(104.76, 65.88), Point(104.76, 0)))]

    if with_bike_lane:
        bike_lane = Trajectory(Line(Point(0, 74.19), Point(94.76, 74.19)),
                               Arc(Point(94.76, 70.88), 3.5, (3*pi/2, 2*pi)),
                               Line(Point(97.76, 70.88), Point(97.76, 0)))

        trajectories.append(bike_lane)

    # mean=14m/s (50Km/h), std deviation=25%
    car_shooter = BallShooter(speed_up, trajectories[0], 5, 14, 14*.25, RED)

    # mean=6.1m/s (21Km/h), std deviation=25%
    bike_shooter = BallShooter(speed_up, trajectories[1], 13, 6.1, 6.1*.25, GREEN)

    if with_bike_lane:
        bike_lane_shooter = BallShooter(speed_up, bike_lane, 20, 6.1, 6.1*.25, BLUE)

    # Add some vehicles (balls)
    balls = []

    background = pygame.image.load ("cruce.png")
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Simulador de tráfico")

    done = False
    clock = pygame.time.Clock()
    _time = 0
    frame_no = 0


    while not done:
        clock.tick(fps)
        _time += tick_period(speed_up)

        screen.blit(background, background.get_rect())

        for trajectory in trajectories:
            trajectory.render(world, screen)


        car = car_shooter.spawn(tick_period(speed_up))
        if car is not None and get_visible_ball(car, balls) is None:
            car.tag = 'car'
            balls.append(car)


        bike = bike_shooter.spawn(tick_period(speed_up))
        if bike is not None and get_visible_ball(bike, balls) is None:
            bike.tag = 'vehicular_cyclist'
            balls.append(bike)

        if with_bike_lane:
            bike = bike_lane_shooter.spawn(tick_period(speed_up))
            if bike is not None and get_visible_ball(bike, balls) is None:
                bike.tag = 'cyclestrian'
                balls.append(bike)

        for ball in balls:
            ball.move(tick_period(speed_up))
            ball.render(world, screen)

        adjust_speeds(balls, speed_up)
        balls = remove_balls_that_exited(balls)
        balls = remove_balls_that_collide(balls)

        print('fps: %d, number of balls: %d, elapsed time: %.4f seconds\r' % (clock.get_fps(), len(balls), _time * speed_up), end='')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        print_statistics(screen)
        pygame.display.flip()

        if save_dir:
            frame_no += 1
            pygame.image.save(screen, '{}/image{}.jpeg'.format(save_dir, frame_no))


if __name__ == '__main__':
    ARGS = docopt(__doc__)

    simulation(ARGS['--with-bike-lane'], ARGS['--save'], SPEED_UP)
