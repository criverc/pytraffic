"""Entities to be used to create traffic simulations"""

import math
import pygame
from .colors import BLACK, RED


def point2pixel(point, world, screen):
    """To Convert a real point in real units to pixel units"""

    pixel_x = screen.get_width() * (point.x / world.width)
    pixel_y = screen.get_height() * (point.y / world.height)

    return pixel_x, pixel_y


class World(object):
    """To contain global simulation data"""

    def __init__(self, width, height):
        self.width = width
        self.height = height


class Point(object):
    """A point is defined in real units, meters"""

    def __init__(self, x, y):
        self.x = x
        self.y = y


    def render(self, world, screen):
        pixel_x, pixel_y = point2pixel(self, world, screen)
        pygame.draw.line(screen, BLACK, [pixel_x, pixel_y], [pixel_x, pixel_y], 1)


class Line(object):


    def __init__(self, point_a, point_b, color=BLACK):
        self.point_a = point_a
        self.point_b = point_b
        self.color = color


    def render(self, world, screen):
        pixel_a_x, pixel_a_y = point2pixel(self.point_a, world, screen)
        pixel_b_x, pixel_b_y = point2pixel(self.point_b, world, screen)

        pygame.draw.line(screen, self.color, [pixel_a_x, pixel_a_y], [pixel_b_x, pixel_b_y], 1)


    def distance(self):
        x_b = self.point_b.x
        x_a = self.point_a.x
        y_b = self.point_b.y
        y_a = self.point_a.y

        return math.sqrt((x_b-x_a)*(x_b-x_a) + (y_b-y_a)*(y_b-y_a))


    def point(self, length):
        """To get the point at length along the curve"""

        cos = (self.point_b.x - self.point_a.x)/self.distance()
        sin = (self.point_b.y - self.point_a.y)/self.distance()

        dx = cos * length
        dy = sin * length

        x = dx + self.point_a.x
        y = dy + self.point_a.y

        return Point(x, y)


    def get_tangent_cone(self, length, aperture, visibility_distance):
        """Given a point length in the Line return a tangent cone"""
        # TODO: Implement
        pass


class Arc(object):


    def __init__(self, center, radius, arc, color=BLACK):
        """In real units, meters, and range of radians"""

        self.center = center
        self.radius = radius
        self.arc = arc
        self.color = color


    def render(self, world, screen):
        p_a = Point(self.center.x - self.radius, self.center.y - self.radius)

        x, y = point2pixel(p_a, world, screen)
        dx, dy = point2pixel(Point(2 * self.radius, 2 * self.radius), world, screen)

        if self.arc[1] < self.arc[0]:
            arc = self.arc[1], self.arc[0]
        else:
            arc = self.arc

        pygame.draw.arc(screen, self.color, [x, y, dx, dy], *arc, 1)


    def distance(self):
        return math.sqrt(((self.arc[1] - self.arc[0]) * self.radius)**2)


    def point(self, length):
        """To get the point at length along the curve"""

        if self.arc[1] < self.arc[0]:
            sense = -1
        else:
            sense = 1

        theta = self.arc[0] + sense * (length / self.radius)

        x = self.center.x + self.radius * math.cos(theta)
        y = self.center.y - self.radius * math.sin(theta)

        return Point(x, y)


class Trajectory(object):
    """A trajectory is made up of segments, straight lines, curves, etc."""


    def __init__(self, *segments):
        self.segments = segments


    def render(self, world, screen):
        for obj in self.segments:
            obj.render(world, screen)


    def distance(self):
        distance = 0
        for _ in self.segments:
            distance += _.distance()

        return distance


    def point(self, length):
        """To get a point in trajectory given length along trajectory"""

        distance_a = 0
        distance_b = 0

        segment = None

        for _ in self.segments:
            distance_b += _.distance()
            if length < distance_b:
                segment = _
                break
            distance_a = distance_b

        if segment is None:
            return None

        return segment.point(length-distance_a)


class Ball(object):


    def __init__(self, radius, trajectory, color=RED):
        self.position = 0
        self.trajectory = trajectory
        self.center = trajectory.point(self.position)
        self.radius = radius
        self.color = color
        self.speed = 0


    def set_speed(self, speed):
        self.speed = speed


    def move(self, tick):
        self.position += self.speed * tick
        self.center = self.trajectory.point(self.position)


    def render(self, world, screen):
        if self.center is not None:
            point_a = Point(self.center.x-self.radius, self.center.y-self.radius)

            width = 2*self.radius
            height = 2*self.radius
            size = Point(width, height)

            pygame.draw.ellipse(screen, self.color, [*point2pixel(point_a, world, screen),
                                                     *point2pixel(size, world, screen)])

