#################################################################
# FILE : torpedo.py
# WRITERS : Ilay Chen, ilaychen, Arad shapira, aradshapira,
# EXERCISE : intro2cs2 ex10 2021
# DESCRIPTION: An Torpedo class
# WEB PAGES I USED: None
# NOTES: ...
#################################################################

import math


class Torpedo:
    # this class creates a torpedo with features that
    # can be seen in the constructor
    # constant representing the torpedo
    # radius as it appears on the screen
    TORPEDO_RADIUS = 4

    def __init__(self, location, heading, speed_x, speed_y):
        """
        the torpedo constructor, all parameters are required
        in order to define a torpedo
        """
        self.__speed_x = speed_x + 2 * math.cos(math.radians(heading))
        self.__speed_y = speed_y + 2 * math.sin(math.radians(heading))
        self.__location_x = location[0]
        self.__location_y = location[1]
        self.__heading = heading
        self.__radius = self.TORPEDO_RADIUS
        self.__life_time = 0

    def get_location(self):
        """
        :return: torpedo's location as tuple
        """
        return self.__location_x, self.__location_y

    def get_heading(self):
        """
        :return: torpedo's heading
        """
        return self.__heading

    def move(self, screen_min_x, screen_max_x, screen_min_y, screen_max_y):
        """
        input: borders of the screen
        return: updating the location in x,y axis of the torpedo on
                the screen, according to the formula
        """
        self.__location_x = screen_min_x +\
                            (self.__location_x
                             + self.__speed_x - screen_min_x) % \
                            (screen_max_x - screen_min_x)
        self.__location_y = screen_min_y +\
                            (self.__location_y
                             + self.__speed_y - screen_min_y) % \
                            (screen_max_y - screen_min_y)

    def get_radius(self):
        """
        :return: torpedo's radius
        """
        return self.__radius

    def get_speed(self):
        """
        :return: torpedo's speed as tuple
        """
        return self.__speed_x, self.__speed_y

    def add_life_time(self):
        """
        helps to count the life time of the torpedo
        :return: adds 1 to the torpedo's life time
        """
        self.__life_time += 1

    def get_life_time(self):
        """
        :return: torpedo's life time
        """
        return self.__life_time
