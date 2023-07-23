#################################################################
# FILE : asteroid.py
# WRITERS : Ilay Chen, ilaychen, Arad shapira, aradshapira,
# EXERCISE : intro2cs2 ex10 2021
# DESCRIPTION: An Asteroid class
# WEB PAGES I USED: None
# NOTES: ...
#################################################################

import random
import math


class Asteroid:
    # this class creates an asteroid with features that
    # can be seen in the constructor
    def __init__(self):
        self.__speed_x = random.randint(1, 5)
        self.__speed_y = random.randint(1, 5)
        self.__location_x = 0
        self.__location_y = 0
        self.__size = 0
        self.__radius = 0

    def set_location(self, location):
        """
        :param location: tuple representing location
        :return: set the new torpedo location
        """
        self.__location_x = location[0]
        self.__location_y = location[1]

    def get_location(self):
        """
        :return: tuple of the current location
        """
        return self.__location_x, self.__location_y

    def move(self, screen_min_x, screen_max_x, screen_min_y, screen_max_y):
        """
        input: borders of the screen
        return: updating the location in x,y axis of the torpedo on
                the screen, according to the formula
        """
        self.__location_x = screen_min_x +\
                            (self.__location_x
                             + self.__speed_x - screen_min_x)\
                            % (screen_max_x - screen_min_x)
        self.__location_y = screen_min_y +\
                            (self.__location_y + self.__speed_y
                             - screen_min_y) %\
                            (screen_max_y - screen_min_y)

    def has_intersection(self, obj):
        """
        :param obj: can be ship or torpedo in our game for example
        :return: True if there is intersection , False otherwise
        """
        distance = math.sqrt(math.pow((obj.get_location()[0]
                                       - self.__location_x), 2) +
                             math.pow((obj.get_location()[1]
                                       - self.__location_y), 2))
        if distance <= self.__radius + obj.get_radius():
            return True
        return False

    def set_radius(self, size):
        """
        :param size: current size of the asteroid
        :return: sets the updated radius
        """
        self.__radius = (size * 10) - 5

    def get_radius(self):
        """
        :return: radius of the asteroid
        """
        return self.__radius

    def get_size(self):
        """
        :return: size of the asteroid
        """
        return self.__size

    def set_size(self, size):
        """
        :param size: size of the asteroid
        :return: set the size and call
                 set_radius to set the radius accordingly
        """
        self.__size = size
        self.set_radius(self.__size)

    def set_speed(self, speed):
        """
        :param speed: tuple representing the speed
        :return: setting updated speed
        """
        self.__speed_x = speed[0]
        self.__speed_y = speed[1]

    def get_speed(self):
        """
        :return: tuple representing the speed of the asteroid
        """
        return self.__speed_x, self.__speed_y
