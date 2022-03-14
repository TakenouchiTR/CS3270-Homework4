"""
Stores information about an environment that an agent can navigate, including
the start position, the rewards for each tile, the goals, and the restart tiles.
"""

import json

__author__ = "Shawn Carter"
__version__ = "Spring 2022"
__pylint__ = "Version 2.12.2"

class Environment():
    """
    Stores information about an environment that an agent can navigate, including
    the start position, the rewards for each tile, the goals, and the restart tiles.
    """
    _rewards: list
    _goals: set
    _game_over_tile: set
    _width: int
    _start_position: int

    def __init__(self, file_path):
        self.load_file(file_path)
        self._create_action_cache()

    def load_file(self, file_path):
        """
        Loads an environment from a file.
        """
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
            self._rewards = data["environment"]
            self._goals = data["win_tiles"]
            self._game_over_tile = data["game_over_tiles"]
            self._width = data["width"]
            self._start_position = data["start_position"]

    def _create_action_cache(self):
        self.cache = []
        for i in range(len(self._rewards)):
            actions = []

            #Not on top edge
            if i // self._width != 0:
                actions.append((i, i - 10))
            #Not on right edge
            if i % self._width != self._width - 1:
                actions.append((i, i + 1))
            #Not on bottom edge
            if i // 10 != len(self._rewards) // self._width - 1:
                actions.append((i, i + 10))
            #Not on left edge
            if i % self._width != 0:
                actions.append((i, i - 1))

            self.cache.append(actions)

    def get_actions_for_position(self, position):
        """
        Creates a list containing all possible actions for a given position.

        Args: position - The specified position.
        Return: A list containing all posible actions for the position.
        """
        return self.cache[position][:]

    def is_goal_tile(self, position):
        """
        Checks whether or not a tile is a goal or not.

        Params - position: The specified position.
        Return - [True] iff the tile is a goal, otherwise [False].
        """
        return position in self._goals

    def is_game_over_tile(self, position):
        """
        Checks whether or not a tile is a restart tile or not.

        Params - position: The specified position.
        Return - [True] iff the tile is a restart tile, otherwise [False]
        """
        return position in self._game_over_tile

    def is_restart_tile(self, position):
        """
        Checks whether a tile is either a game over tile or a goal tile.

        Params - position: The specified position.
        Return - [True] iff the tile is a goal or a game over tile, otherwise [False].
        """
        return self.is_game_over_tile(position) or self.is_goal_tile(position)

    def get_reward_at(self, position):
        """
        Gets the reward at a specified position.

        Params - position: The specified position.
        Return - The reward at the specified position.
        """
        if position < 0 or position >= len(self._rewards):
            raise Exception("position must be at least 0, but less than the number of tiles.")
        return self._rewards[position]

    @property
    def width(self):
        """
        Gets the environment's width.

        Params - None
        Return - The environment's width.
        """
        return self._width

    @property
    def start_position(self):
        """
        Gets the environment's start position.

        Params - None
        Return - The environment's start position.
        """
        return self._start_position

    @property
    def rewards(self):
        """
        Gets the environment's rewards.

        Params - None
        Return - The environment's rewards.
        """
        return self._rewards
