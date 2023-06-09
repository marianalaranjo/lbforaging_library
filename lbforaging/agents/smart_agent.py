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
        coop = False
        for i in range(len(obs.players)):
            if(obs.players[i].is_self):
                current_agent = i
        preys = []
        victims = []
        for row in range(len(obs.field)):
            for column in range(len(obs.field[row])):
                if obs.field[row][column] != 0:
                    preys += [row, column]
                    victims += [obs.field[row][column]]
        max_number = 0
        max_victims = -1
        if len(victims) == 1:
            max_victims = 0
        else:
            for victim in range(len(victims)):
                if victims[victim] > max_number:
                    max_number = victims[victim]
                    max_victims = victim

        if max_victims != -1:
            prey = (preys[max_victims*2], preys[max_victims*2+1])
            if coop:
                number_of_agents = 0
                for player in obs.players:
                    if prey == obs.players[current_agent].current_prey:
                        action = self.direction_to_go(obs, obs.players[current_agent].position, prey)
                        return action, prey
                    if prey == player.current_prey:
                        number_of_agents+=1
                
                if number_of_agents == 0:

                    action = self.direction_to_go(obs, obs.players[current_agent].position, prey)
                    return action, prey
                
                elif obs.field[prey[0]][prey[1]] > number_of_agents*5:
                    action = self.direction_to_go(obs, obs.players[current_agent].position, prey)
                    return action, prey

                preys[max_victims*2]= 999
                preys[max_victims*2+1] = 999
            else:
                for number in victims:
                    if number != max_number:
                        action = self.direction_to_go(obs, obs.players[current_agent].position, prey)
                        return action, prey
        
        closest_prey = self.closest_prey(obs.players[current_agent].position, preys)
        prey_found = closest_prey is not None

        if prey_found:
            action = self.direction_to_go(obs, obs.players[current_agent].position, closest_prey)
        else:
            action = random.choice(obs.actions)
        return action, closest_prey
            
    def direction_to_go(self, obs, agent_position, prey_position):
        actions = ()
        for el in range(len(obs.actions)):
            actions += (obs.actions[el].value, )
        distances = np.array(prey_position) - np.array(agent_position)
        abs_distances = np.absolute(distances)

        if abs_distances[0]==0 and abs_distances[1]==1 and Action.LOAD.value in actions:
            return Action.LOAD.value
        elif abs_distances[0]==1 and abs_distances[1]==0 and Action.LOAD.value in actions:
            return Action.LOAD.value
        elif abs_distances[0] < abs_distances[1]:
            return self._close_horizontally(obs, distances,actions)
        elif abs_distances[0] > abs_distances[1]:
            return self._close_vertically(obs, distances, actions)
        else:
            roll = random.uniform(0, 1)
            return self._close_horizontally(obs, distances, actions) if roll > 0.5 else self._close_vertically(obs, distances, actions)

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

    def _close_horizontally(self, obs, distances, actions):
    
        if distances[1] > 0 and Action.EAST.value in actions:
            return Action.EAST.value
        elif distances[1] < 0 and Action.WEST.value in actions:
            return Action.WEST.value
        else:
            return random.choice(obs.actions)

    def _close_vertically(self, obs, distances, actions):
        if distances[0] > 0 and Action.SOUTH.value in actions:
            return Action.SOUTH.value
        elif distances[0] < 0 and Action.NORTH.value in actions:
            return Action.NORTH.value
        else:
            return random.choice(obs.actions)
        