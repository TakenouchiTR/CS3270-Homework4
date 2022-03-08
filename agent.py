from random import randint, random, seed
from environment import Environment

__author__ = "Shawn Carter"
__version__ = "Spring 2022"
__pylint__ = "Version 2.12.2"

class Agent():
    def __init__(self):
        self.alpha = .1
        self.gamma = .9
        self.epsilon = .1
        self.found_end = False
        self.policy = None
        self.q_table = {}
        self.environment = None
        self.hit_counts = None

    def load_environment(self, file_path):
        seed(31)
        self.q_table.clear()
        self.policy = None
        self.found_end = False

        self.environment = Environment(file_path)
        self.hit_counts = [0] * len(self.environment.rewards)

        for i in range(len(self.environment.rewards)):
            for action in self.environment.get_actions_for_position(i):
                self.q_table[action] = 0

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

        best_actions = list(filter(lambda action: self.q_table[action] == self.q_table[actions[0]], actions))
        selected_action = best_actions[randint(0, len(best_actions) - 1)]
        return selected_action

    def _get_random_action_for_position(self, position):
        """
        Gets a random action for a specified position.

        All possible actions have an equal chance of being selected.

        Args: position - The specified position.
        Return: A list containing a randomly selected action for the position.
        """
        actions = self.environment.get_actions_for_position(position)
        selected_action = actions[randint(0, len(actions) - 1)]
        return selected_action

    def _calculate_new_q_value(self, action):
        """
        Calculates an updated q-value for a specified action without updating the q-table.

        Args: Action - The specified action.
        Return: The new q-score.
        """
        cur_score = self.q_table[action]
        next_position = action[1]
        next_best_action = self._get_best_action_for_position(next_position)
        new_score = (1 - self.alpha) * cur_score + self.alpha * \
            (self.environment.rewards[next_position] + self.gamma * self.q_table[next_best_action])
        return new_score

    def train(self, episodes):
        """
        Trains the agent over a specified number of episodes.

        Args: episodes - The number of episodes to run.
        Return: None
        """

        cur_epsilon = self.epsilon

        for i in range(episodes):
            position = self.environment.start_position
            path = [position]
            self.hit_counts[position] += 1
            visited = set()

            while True:
                action: tuple
                if random() > cur_epsilon:
                    action = self._get_best_action_for_position(position, visited)
                    if action is None:
                        action = self._get_random_action_for_position(position)
                else:
                    action = self._get_random_action_for_position(position)

                self.q_table[action] = self._calculate_new_q_value(action)
                position = action[1]
                path.append(position)
                visited.add(action)
                self.hit_counts[position] += 1

                if position in self.environment.goals:
                    if not self.found_end or len(path) < len(self.policy):
                        if len(path) == 13:
                            print(f"shortest {i}")
                            print(path)
                        self.policy = path
                        self.found_end = True
                    break
                if position in self.environment.restart_tiles:
                    if not self.found_end and (self.policy is None or len(self.policy) < len(path)):
                        self.policy = path
                    break
            cur_epsilon = i / episodes * self.epsilon