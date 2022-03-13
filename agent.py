"""
Represents an agent that can learn to navigate an environment.
"""

import random
from environment import Environment

__author__ = "Shawn Carter"
__version__ = "Spring 2022"
__pylint__ = "Version 2.12.2"

class Agent():
    """
    Represents an agent that can learn to navigate an environment.
    """

    _alpha: float = .1
    _gamma: float = .9
    _epsilon: float = .1
    _policy: list = None
    _q_table: dict = {}
    _environment: Environment = None
    _tile_visit_counts: list = None

    def __init__(self):
        self._alpha = .1
        self._gamma = .9
        self._epsilon = .1
        self._policy = None
        self._q_table = {}
        self._environment = None
        self._tile_visit_counts = None

    def load_environment(self, file_path):
        """
        Loads a new environment and resets the q-table and policy.
        """
        random.seed(31)
        self._q_table.clear()
        self._policy = None

        self._environment = Environment(file_path)
        self._tile_visit_counts = [0] * len(self.environment.rewards)

        for i in range(len(self.environment.rewards)):
            for action in self.environment.get_actions_for_position(i):
                self._q_table[action] = 0

    def _get_best_action_for_position(self, position, visited = None):
        """
        Gets the action with the highest q-score for a specified position, ignoring visited tiles.

        If all neighboring tiles have been visited, None will be returned instead.

        Args: position - The specified position.
            visited  - All previously visited tiles
        Return: The action that leads to an unvisited tile with the highest value in q_table;
                None if all adjacent tiles have been visited.
        """
        actions = self.environment.get_actions_for_position(position)

        if visited is not None:
            actions = list(filter(lambda action: action not in visited, actions))

        #If all actions have been done before
        if len(actions) == 0:
            return None

        actions.sort(key = self._q_table.get, reverse = True)
        best_actions = list(
            filter(lambda action: self._q_table[action] == self._q_table[actions[0]], actions)
        )
        return random.choice(best_actions)

    def _get_random_action_for_position(self, position):
        """
        Gets a random action for a specified position.

        All possible actions have an equal chance of being selected.

        Args: position - The specified position.
        Return: A list containing a randomly selected action for the position.
        """
        actions = self.environment.get_actions_for_position(position)
        selected_action = random.choice(actions)
        return selected_action

    def _get_next_action_for_position(self, position, episilon, visited):
        action: tuple

        if random.random() > episilon:
            action = self._get_best_action_for_position(position, visited)
            if action is None:
                action = self._get_random_action_for_position(position)
        else:
            action = self._get_random_action_for_position(position)

        return action

    def _calculate_new_q_value(self, action):
        """
        Calculates an updated q-value for a specified action without updating the q-table.

        Args: Action - The specified action.
        Return: The new q-score.
        """
        cur_score = self._q_table[action]
        next_position = action[1]

        next_reward = self.environment.get_reward_at(next_position)
        next_actions = self.environment.get_actions_for_position(next_position)
        next_best_q_value = max(map(self._q_table.get, next_actions))

        new_score = (1 - self.alpha) * cur_score + self.alpha * \
            (next_reward + self.gamma * next_best_q_value)

        return new_score

    def _end_movement_step(self, path):
        cur_position = path[-1]
        if self.environment.is_goal_tile(cur_position):
            if not self._found_end or len(path) < len(self._policy):
                self._policy = path
            return True
        if self.environment.is_restart_tile(cur_position):
            if self._policy is None or (not self._found_end and len(path) < len(self.policy)):
                self._policy = path
            return True
        return False

    def train(self, episodes):
        """
        Trains the agent over a specified number of episodes.

        Args: episodes - The number of episodes to run.
        Return: None
        """
        cur_percent = 0
        cur_epsilon = self._epsilon

        for i in range(episodes):
            position = self.environment.start_position
            path = [position]
            self._tile_visit_counts[position] += 1
            visited = set()

            while True:
                action = self._get_next_action_for_position(position, cur_epsilon, visited)

                self._q_table[action] = self._calculate_new_q_value(action)
                position = action[1]

                path.append(position)
                visited.add(action)

                if i * 100 // episodes  > cur_percent:
                    cur_percent = i * 100 // episodes
                    print(f"{cur_percent}% done...")

                self._tile_visit_counts[position] += 1
                if self._end_movement_step(path):
                    break

            cur_epsilon = i / episodes * self._epsilon

    @property
    def alpha(self):
        """
        Gets the agent's alpha value.

        Params - None
        Return - The agent's alpha value.
        """
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        """
        Sets the agent's alpha value; must be between 0 and 1, inclusive.

        Params - value: The new alpha value.
        Return - None
        """
        if value < 0 or value > 1:
            raise Exception("alpha must be between 0 and 1, inclusive.")
        self._alpha = value

    @property
    def gamma(self):
        """
        Sets the agent's alpha value; must be between 0 and 1, inclusive.

        Params - None
        Return - The agent's alpha value.
        """
        return self._gamma

    @gamma.setter
    def gamma(self, value):
        """
        Sets the agent's gamma value; must be between 0 and 1, inclusive.

        Params - value: The new gamma value.
        Return - None
        """
        if value < 0 or value > 1:
            raise Exception("gamma must be between 0 and 1, inclusive.")
        self._gamma = value

    @property
    def epsilon(self):
        """
        Gets the agent's epsilon value.

        Params - None
        Return - The agent's epsilon value.
        """
        return self._epsilon

    @epsilon.setter
    def epsilon(self, value):
        """
        Sets the agent's epsilon value; must be between 0 and 1, inclusive.

        Params - value: The new epsilon value
        Return - None
        """
        if value < 0 or value > 1:
            raise Exception("epsilon must be between 0 and 1, inclusive.")
        self._epsilon = value

    @property
    def policy(self):
        """
        Gets the agent's policy.

        Params - None
        Return - The agent's policy.
        """
        return self._policy

    @property
    def tile_visit_counts(self):
        """
        Gets a list representing how many times the agent has visited a location.

        Params - None
        Return - The list of how many times the agent has visited a location.
        """
        return self._tile_visit_counts

    @property
    def environment(self):
        """
        Gets the agent's environment.

        Params - None
        Return - The agent's environment.
        """
        return self._environment

    @property
    def _found_end(self):
        return self.policy is not None and self.environment.is_goal_tile(self.policy[-1])
