from lbforaging.foraging.agent import Agent
from enum import Enum
import random
import numpy as np
import math
from scipy.spatial.distance import cityblock

class Action(Enum):
    NONE = 0
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    LOAD = 5

class SmartAgent(Agent):
    name = "Smart Agent"

    def step(self, obs):
        #print(obs.field)
        for i in range(len(obs.players)):
            if(obs.players[i].is_self):
                current_agent = i
        preys = ()
        victims = []
        for row in range(len(obs.field)):
            for column in range(len(obs.field[row])):
                if obs.field[row][column] != 0:
                    preys += (row, column)
                    victims += [obs.field[row][column]]
        #print(preys)
        #print(victims)

        max_victims = -1
        if len(victims) == 1:
            max_victims = 0
        else:
            for victim in range(len(victims)-1):
                if victims[victim] > victims[victim+1] and victims[victim] > max_victims:
                    max_victims = victim
                elif victims[victim+1] > victims[victim] and victims[victim+1] > max_victims:
                    max_victims = victim + 1
        
        #print(max_victims)

        if max_victims != -1:
            prey = (preys[max_victims], preys[max_victims+1])
            #print(prey)
            return self.direction_to_go(obs, obs.players[current_agent].position, prey)
        
        closest_prey = self.closest_prey(obs.players[current_agent].position, preys)
        prey_found = closest_prey is not None

        if prey_found:
            action = self.direction_to_go(obs, obs.players[current_agent].position, closest_prey)
        else:
            action = random.choice(obs.actions)
        return action
            


    
    def direction_to_go(self, obs, agent_position, prey_position):
        distances = np.array(prey_position) - np.array(agent_position)
        abs_distances = np.absolute(distances)
        if abs_distances[0]==0 and abs_distances[1]==1 and Action.LOAD in obs.actions:
            return Action.LOAD
        elif abs_distances[0]==1 and abs_distances[1]==0 and Action.LOAD in obs.actions:
            return Action.LOAD
        elif abs_distances[0] > abs_distances[1]:
            return self._close_horizontally(obs, distances)
        elif abs_distances[0] < abs_distances[1]:
            return self._close_vertically(obs, distances)
        else:
            roll = random.uniform(0, 1)
            return self._close_horizontally(obs, distances) if roll > 0.5 else self._close_vertically(obs, distances)

    def closest_prey(self, agent_position, prey_positions):
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

    def _close_horizontally(self, obs, distances):
        if distances[0] > 1 and Action.EAST in obs.actions:
            return Action.EAST
        elif distances[0] < -1 and Action.WEST in obs.actions:
            return Action.WEST
        else:
            return random.choice(obs.actions)

    def _close_vertically(self, obs, distances):
        if distances[1] > 1 and Action.SOUTH in obs.actions:
            return Action.SOUTH
        elif distances[1] < -1 and Action.NORTH in obs.actions:
            return Action.NORTH
        else:
            return random.choice(obs.actions)