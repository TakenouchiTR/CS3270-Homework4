"""
Homework 4 for Intelligent Systems.

Has an agent navigate an environment to find the goal.
"""

import time
from agent import Agent

__author__ = "Shawn Carter"
__version__ = "Spring 2022"
__pylint__ = "Version 2.12.2"

EPISODES = 1_000_000
ENVIRONMENT_FILE = "sample_environment.json"

def display_visit_counts(visit_counts, environment_width):
    """
    Displays a list of tile visit counts as a table with a specified environment width.

    Params - visit_counts: A list containing how many times a tile was visited.
             environment_width: How wide the environment is, in tiles.
    Return - None
    """
    for i in range(len(visit_counts) // environment_width):
        formatted_counts = map(str, visit_counts[i * environment_width:(i + 1) * environment_width])
        print("\t".join(formatted_counts))

def display_success_rate(agent: Agent):
    """
    Calculates and displays how often the agent is able to make it to the goal.

    Params - agent: The trained agent.
    Return - None
    """
    successful_episodes = 0
    for position, visit_count in enumerate(agent.tile_visit_counts):
        if agent.environment.is_goal_tile(position):
            successful_episodes += visit_count

    success_rate = successful_episodes / EPISODES * 100
    print(f"Agent reached the goal(s) {success_rate:.2f}% of the time.")

def display_agent_information(agent: Agent):
    """
    Displays information about the agent after completing its training.

    Params - agent: The trained agent
    Return - None
    """
    print(f"Found policy: {agent.policy}")
    display_success_rate(agent)
    print("Tile visit counts:")
    display_visit_counts(agent.tile_visit_counts, agent.environment.width)

def main():
    """
    The main entry point for the script.
    """
    agent = Agent()
    agent.load_environment(ENVIRONMENT_FILE)

    start = time.time()
    print(f"Running {EPISODES:,} training episodes...")
    agent.train(EPISODES)

    duration = time.time() - start
    print(f"{EPISODES:,} episodes run in {duration:.2f} seconds")

    display_agent_information(agent)

if __name__ == "__main__":
    main()
