#################################################################
# FILE : ship.py
# WRITERS : Ilay Chen, ilaychen, Arad shapira, aradshapira,
# EXERCISE : intro2cs2 ex10 2021
# DESCRIPTION: An Ship class
# WEB PAGES I USED: None
# NOTES: ...
#################################################################

import math
from torpedo import Torpedo


class Ship:
    # this class creates a ship with features that
    # can be seen in the constructor
    # constants we have set according to orders of the exercise
    SHIP_RADIUS = 1
    INITIAL_LIVES = 3
    MAX_TORPEDOES = 10

    def __init__(self):
        """
        ship constructor, includes speed and locations in x,y axis
        the heading of the ship, torpedoes that belongs to the ship
        current number of lives, the radius of the ship
        (as it appears on the screen)
        """
        self.__speed_x = 0
        self.__speed_y = 0
        self.__location_x = 0
        self.__location_y = 0
        self.__heading = 0
        self.__torpedoes = []
        self.__lives = self.INITIAL_LIVES
        self.__radius = self.SHIP_RADIUS

    def move(self, screen_min_x, screen_max_x, screen_min_y, screen_max_y):
        """
        input: borders of the screen
        return: updating the location in x,y axis of the ship on
                the screen, according to the formula
        """
        self.__location_x = screen_min_x + (self.__location_x +
                                            self.__speed_x - screen_min_x) \
                            % (screen_max_x - screen_min_x)
        self.__location_y = screen_min_y + (self.__location_y +
                                            self.__speed_y - screen_min_y) \
                            % (screen_max_y - screen_min_y)

    def rotate_right(self, is_right):
        """
        :param is_right: True / False
        return: updating the heading of the ship 7 degrees right
        """
        if is_right:
            self.__heading -= 7

    def rotate_left(self, is_left):
        """
        :param is_left: True / False
        return: updating the heading of the ship 7 degrees left
        """
        if is_left:
            self.__heading += 7

    def shoot_torpedo(self, is_space_pressed):
        """
        :param is_space_pressed: True / False
        :return:
        """
        if is_space_pressed and len(self.__torpedoes) < \
                self.MAX_TORPEDOES:
            # means the shooting is legal, so we will append this torpedo
            # to the torpedo's list
            # and return this specific torpedo
            self.__torpedoes.append(Torpedo(self.get_location(),
                                            self.__heading, self.__speed_x,
                                            self.__speed_y))
            return self.__torpedoes[-1]

    def remove_torpedo(self, torpedo):
        """
        :param torpedo: from our list
        :return: removing this torpedo from the list
        """
        self.__torpedoes.remove(torpedo)
        return torpedo

    def get_torpedoes(self):
        """
        :return: the torpedo list
        """
        return self.__torpedoes

    def increase_speed(self, is_up):
        """
        :param is_up: True / False
        :return: increasing the ship's speed
        """
        # also we transfer from degrees to radians as required
        if is_up:
            self.__speed_x += math.cos(math.radians(self.__heading))
            self.__speed_y += math.sin(math.radians(self.__heading))

    def set_speed(self, speed):
        """
        :param speed: tuple, first is x speed. second is y speed
        :return: sets the new speed
        """
        self.__speed_x = speed[0]
        self.__speed_y = speed[1]

    def set_location(self, location):
        """
        :param location: tuple, first is x location. second is y location
        :return: sets the new speed
        """
        self.__location_x = location[0]
        self.__location_y = location[1]

    def remove_life(self):
        """
        :return: removes 1 from our current number of lives
        """

        self.__lives -= 1

    def get_life(self):
        """
        :return: number of live we have
        """
        return self.__lives

    def get_radius(self):
        """
        :return: the ship's radius
        """
        return self.__radius

    def get_location(self):
        """
        :return: tuple representing the ship's location
        """
        return self.__location_x, self.__location_y

    def get_speed(self):
        """
        :return: tuple of speed in x,y axis
        """
        return self.__speed_x, self.__speed_y

    def get_heading(self):
        """
        :return: the heading of the ship
        """
        return self.__heading
