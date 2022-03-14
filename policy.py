"""
Holds the path and reward for a policy.
"""

__author__ = "Shawn Carter"
__version__ = "Spring 2022"
__pylint__ = "Version 2.12.2"


class Policy:
    """
    Holds the path and reward for a policy.
    """
    _reward: int
    _path: list[int]

    def __init__(self, reward, path):
        self._reward = reward
        self._path = path

    @property
    def reward(self):
        """
        Gets the policy's reward.

        Params - None
        Return - The policy's reward.
        """
        return self._reward

    @property
    def path(self):
        """
        Gets the policy's path.

        Params - None
        Return - The policy's path.
        """
        return self._path
