"""
Homework 4 for Intelligent Systems.

Has an agent navigate an environment to find the goal.
"""

from random import seed
import time
from agent import Agent

__author__ = "Shawn Carter"
__version__ = "Spring 2022"
__pylint__ = "Version 2.12.2"

EPISODES = 1_000_000
ENVIRONMENT_FILE = "sample_environment.json"
seed(31)

def main():
    """
    The main entry point for the script.
    """
    agent = Agent()
    agent.load_environment(ENVIRONMENT_FILE)
    start = time.time()
    agent.train(EPISODES)
    print(time.time() - start)

    for i in range(len(agent.hit_counts) // agent.environment.width):
            print("\t".join(list(map(str, agent.hit_counts[i * agent.environment.width:(i + 1) * agent.environment.width]))))
    print(agent.policy)
    
if __name__ == "__main__":
    main()
