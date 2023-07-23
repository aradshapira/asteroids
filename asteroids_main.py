#################################################################
# FILE : asteroid_main.py
# WRITERS : Ilay Chen, ilaychen, Arad shapira, aradshapira,
# EXERCISE : intro2cs2 ex10 2021
# DESCRIPTION: An asteroid game class implementation
# WEB PAGES I USED: None
# NOTES: ...
#################################################################

from screen import Screen
from ship import Ship
from asteroid import Asteroid
import sys
import random
import math

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    # Some default values for the game
    INITIAL_ASTEROID_SIZE = 3
    SCORE_LIST = [0, 100, 50, 20]
    TORPEDO_MAX_LIFE_TIME = 200
    LOOSE_TEXT = "You have lost! You are looser"
    WIN_TEXT = "You save the galaxy! you are my hero!"
    QUIT_GAME = "Shame on you! what will the galaxy do without you?!"
    MESSAGE_TITLE = "Dear saver,"

    def __init__(self, asteroids_amount):
        """
        init function, start the ship, and make the initial asteroids
        :param asteroids_amount: number of asteroids to make
        """
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        # Initiate the score and the asteroid list
        self.__sum_score = 0
        self.__asteroid_list = []

        # Make the ship
        self.__ship = Ship()
        self.__ship = self.set_location(self.__ship)

        # make the asteroids
        self.make_asteroids(asteroids_amount)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        Main function of te game. run all the game and handle all the objects.
        In every loop moves all objects, and check if there are intersection and implement it
        """
        # Check if user want to exit and show informative message.
        if self.__screen.should_end():
            self.exit_game(self.QUIT_GAME)

        # call the ship to shut torpedo if it can, get that torpedo and add it to the screen.
        new_torpedo = self.__ship.shoot_torpedo(self.__screen.is_space_pressed())
        if new_torpedo is not None:
            self.__screen.register_torpedo(new_torpedo)

        # Moves the ship
        self.move_ship()

        self.handle_torpedo()
        
        self.handle_asteroids()

        # If all lives over, loose the game
        if self.__ship.get_life() == 0:
            self.exit_game(self.LOOSE_TEXT)
        # If all asteroid over win the game
        elif len(self.__asteroid_list) == 0:
            self.exit_game(self.WIN_TEXT)
    
    def move_ship(self):
        """
        Function check user input to move the ship and moves it.
        then draw the move on the screen.
        """
        self.__ship.rotate_right(self.__screen.is_right_pressed())
        self.__ship.rotate_left(self.__screen.is_left_pressed())
        self.__ship.increase_speed(self.__screen.is_up_pressed())
        self.__ship.move(self.__screen_min_x, self.__screen_max_x, self.__screen_min_y, self.__screen_max_y)
        self.__screen.draw_ship(self.__ship.get_location()[0], self.__ship.get_location()[1], self.__ship.get_heading())
    
    def handle_torpedo(self):
        """
        Function check for each torpedo if he end his life_time, and delete him from ship and screen if needed.
        Otherwise, it moves him, draw, and the check if it has intersection with some asteroid.
        If so, its handle the impact, and add score.
        """
        for torpedo in self.__ship.get_torpedoes():
            torpedo.add_life_time()
            if torpedo.get_life_time() == self.TORPEDO_MAX_LIFE_TIME:
                remove = self.__ship.remove_torpedo(torpedo)
                self.__screen.unregister_torpedo(remove)
                break
            else:
                torpedo.move(self.__screen_min_x, self.__screen_max_x, self.__screen_min_y, self.__screen_max_y)
                self.__screen.draw_torpedo(torpedo, torpedo.get_location()[0], torpedo.get_location()[1],
                                           torpedo.get_heading())

            for asteroid in self.__asteroid_list:
                if asteroid.has_intersection(torpedo):
                    remove = self.__ship.remove_torpedo(torpedo)
                    self.__screen.unregister_torpedo(remove)
                    score = self.make_asteroids(2, asteroid.get_size() - 1, torpedo.get_speed(), asteroid.get_speed(),
                                                asteroid.get_location(), True)
                    self.__sum_score += score
                    self.__screen.set_score(self.__sum_score)
                    self.__screen.unregister_asteroid(asteroid)
                    self.__asteroid_list.remove(asteroid)
                    break
            
    def handle_asteroids(self):
        """
        Function moves all the asteroids and chek if one of the hit the ship. If it hits, it remove one live and the
        asteroid, and show informative message.
        """
        for asteroid in self.__asteroid_list:
            asteroid.move(self.__screen_min_x, self.__screen_max_x, self.__screen_min_y, self.__screen_max_y)
            self.__screen.draw_asteroid(asteroid, asteroid.get_location()[0], asteroid.get_location()[1])

            if asteroid.has_intersection(self.__ship):
                self.__screen.show_message("Oh No!", "Your ship is crashed")
                self.__screen.remove_life()
                self.__ship.remove_life()
                self.__screen.unregister_asteroid(asteroid)
                self.__asteroid_list.remove(asteroid)
                break

    def exit_game(self, text):
        """
        Get informative massage, show it and end the game.
        :param text: informative massage text
        """
        self.__screen.show_message(self.MESSAGE_TITLE, text)
        self.__screen.end_game()
        sys.exit()

    def set_location(self, obj, new_location=(0, 0)):
        """
        Function set the location of the given object. in a random location, or specific if given.
        Also, checks that if its asteroid, the random location is not on the ship.
        :param obj: object to set location
        :param new_location: specific location
        :return: the object with the new location
        """
        if new_location != (0, 0):
            obj.set_location(new_location)
            return obj
        location = (random.randint(1, self.__screen_max_x), random.randint(1, self.__screen_max_y))
        obj.set_location(location)
        if type(obj) == Asteroid:
            if obj.has_intersection(self.__ship):
                return self.set_location(obj)
        return obj

    def make_asteroids(self, num=DEFAULT_ASTEROIDS_NUM, size=3, torpedo_speed=(0, 0), old_asteroid_speed=(0, 0),
                       old_asteroid_location=(0, 0), is_split=False):
        """
        Function handle all the make of the asteroids, in the beginning and inside the game loop.
        Can make default asteroids in the start of the game, and new asteroid when there is an impact.
        :param num: number of asteroids to make
        :param size: size of new asteroid
        :param torpedo_speed: speed of hitting object
        :param old_asteroid_speed: old asteroid speed
        :param old_asteroid_location: old asteroid location
        :param is_split: is the asteroid needed to be split to two new asteroids
        :return: score to add accordingly the size of the asteroid
        """
        if size == 1:
            return self.SCORE_LIST[size]

        new_speed = []
        # If split, make new speeds in x and y
        if is_split:
            num = 2
            for i in range(2):
                new_speed.append((torpedo_speed[i] + old_asteroid_speed[i]) /
                                 math.sqrt(math.pow(old_asteroid_speed[0], 2) + math.pow(old_asteroid_speed[1], 2)))
        for i in range(num):
            new_asteroid = Asteroid()
            new_asteroid.set_size(size)
            new_asteroid = self.set_location(new_asteroid, old_asteroid_location)

            if is_split:
                # if this is the second when we split, make it opposite direction
                if num == 2:
                    new_speed[0] *= -1
                    new_speed[1] *= -1
                new_asteroid.set_speed(new_speed)

            self.__asteroid_list.append(new_asteroid)
            self.__screen.register_asteroid(self.__asteroid_list[-1], new_asteroid.get_size())

        return self.SCORE_LIST[size]


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
