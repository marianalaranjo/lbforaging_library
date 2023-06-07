import random
import numpy as np
import math
from scipy.spatial.distance import cityblock

from lbforaging.foraging.agent import Agent
#from lbforaging.foraging.environment import Action


class GreedyAgent(Agent):

    """
    A baseline agent for the SimplifiedPredatorPrey environment.
    The greedy agent finds the nearest prey and moves towards it.
    """

    def step(self, obs):

        for i in range(len(obs.players)):
            if(obs.players[i].is_self):
                current_agent = i
        preys = []
        for row in range(len(obs.field)):
            for column in range(len(obs.field[row])):
                if obs.field[row][column] != 0:
                    preys += [row, column,]

        closest_prey = self.closest_prey(obs.players[current_agent].position, preys)
        prey_found = closest_prey is not None

        return self.direction_to_go(obs.players[current_agent].position, closest_prey) if prey_found else 5

    # ################# #
    # Auxiliary Methods #
    # ################# #

    def direction_to_go(self, agent_position, prey_position):
        """
        Given the position of the agent and the position of a prey,
        returns the action to take in order to close the distance
        """
        distances = np.array(prey_position) - np.array(agent_position)
        abs_distances = np.absolute(distances)
        if abs_distances[0] > abs_distances[1]:
            return self._close_horizontally(distances)
        elif abs_distances[0] < abs_distances[1]:
            return self._close_vertically(distances)
        else:
            roll = random.uniform(0, 1)
            return self._close_horizontally(distances) if roll > 0.5 else self._close_vertically(distances)

    def closest_prey(self, agent_position, prey_positions):
        """
        Given the positions of an agent and a sequence of positions of all prey,
        returns the positions of the closest prey
        """
        min = math.inf
        closest_prey_position = None
        n_preys = int(len(prey_positions) / 2)
        for p in range(n_preys):
            prey_position = prey_positions[p * 2], prey_positions[(p * 2) + 1]
            distance = cityblock(agent_position, prey_position)
            if distance < min:
                min = distance
                closest_prey_position = prey_position
        return closest_prey_position
    # ############### #
    # Private Methods #
    # ############### #

    def _close_horizontally(self, distances):
        if distances[0] > 0:
            return 4
        elif distances[0] < 0:
            return 3
        else:
            return 0

    def _close_vertically(self, distances):
        if distances[1] > 0:
            return 2
        elif distances[1] < 0:
            return 1
        else:
            return 0
        
    def next(self, observation, action, next_observation, reward, terminal, info):
        # Not a learning agent
        pass