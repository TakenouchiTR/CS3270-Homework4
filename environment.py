import json
from os import environ

__author__ = "Shawn Carter"
__version__ = "Spring 2022"
__pylint__ = "Version 2.12.2"

class Environment():
    def __init__(self, file_path):
        self.load_file(file_path)
        self.create_action_cache()

    def load_file(self, file_path):
        with open(file_path) as file:
            data = json.load(file)
            self.rewards = data["environment"]
            self.goals = data["win_tiles"]
            self.restart_tiles = data["restart_tiles"]
            self.width = data["width"]
            self.start_position = data["start_position"]

    def create_action_cache(self):
        self.cache = []
        for i in range(len(self.rewards)):
            actions = []
            
            #Not on top edge
            if i // 10 != 0:
                actions.append((i, i - 10))
            #Not on right edge
            if i % self.width != self.width - 1:
                actions.append((i, i + 1))
            #Not on bottom edge
            if i // 10 != len(self.rewards) // self.width - 1:
                actions.append((i, i + 10))
            #Not on left edge
            if i % self.width != 0:
                actions.append((i, i - 1))
            
            self.cache.append(actions)

    def get_actions_for_position(self, position):
        """
        Creates a list containing all possible actions for a given position.

        Args: position - The specified position.
        Return: A list containing all posible actions for the position.
        """
        return self.cache[position]