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

        max_victims = -1
        if len(victims) == 1:
            max_victims = 0
        else:
            for victim in range(len(victims)-1):
                if victims[victim] > victims[victim+1] and victims[victim] > max_victims:
                    max_victims = victim
                elif victims[victim+1] > victims[victim] and victims[victim+1] > max_victims:
                    max_victims = victim + 1
        print("VICTIMS")
        print(victims)
        print("MAX_VICTIMS")
        print(max_victims)

        if max_victims != -1:
            prey = (preys[max_victims*2], preys[max_victims*2+1])
            print(prey)
            action = self.direction_to_go(obs, obs.players[current_agent].position, prey)
            print(action)
            return action
        
        closest_prey = self.closest_prey(obs.players[current_agent].position, preys)
        prey_found = closest_prey is not None

        if prey_found:
            action = self.direction_to_go(obs, obs.players[current_agent].position, closest_prey)
        else:
            action = random.choice(obs.actions)
        return action
            
    def direction_to_go(self, obs, agent_position, prey_position):
        actions = ()
        for el in range(len(obs.actions)):
            actions += (obs.actions[el].value, )
        distances = np.array(prey_position) - np.array(agent_position)
        abs_distances = np.absolute(distances)
        print("DISTANCES: ")
        print(distances)
        print(distances[0])
        print(distances[1])
        print("ABSOLUTE DISTANCES:")
        print(abs_distances)
        print(abs_distances[0])
        print(abs_distances[1])
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
        print("CLOSE HORIZONTAL")
        if distances[1] > 0 and Action.EAST.value in actions:
            print("EAST")
            return Action.EAST.value
        elif distances[1] < 0 and Action.WEST.value in actions:
            print("WEST")
            return Action.WEST.value
        else:
            print("RANDOM")
            return random.choice(obs.actions)

    def _close_vertically(self, obs, distances, actions):
        print("CLOSE VERTICAL")
        if distances[0] > 0 and Action.SOUTH.value in actions:
            print("SOUTH")
            return Action.SOUTH.value
        elif distances[0] < 0 and Action.NORTH.value in actions:
            print("NORTH")
            return Action.NORTH.value
        else:
            print("RANDOM")
            return random.choice(obs.actions)
        
# class ConventionAgent(SmartAgent):



#     def action(self) -> int:
#         agent_order = self.conventions[0]
#         action_order = self.conventions[1]
#         prey_pos = self.observation[self.n_agents * 2:]
#         agent_pos = (self.observation[self.agent_id * 2], self.observation[self.agent_id * 2 + 1])
#         agent_priority = agent_order.index(self.agent_id)
#         return self.advance_to_pos(agent_pos, prey_pos, action_order[agent_priority])

#     def advance_to_pos(self, agent_pos: Tuple, prey_pos: Tuple, agent_dest: int) -> int:
#         """
#         Choose movement action to advance agent towards the destination around prey
        
#         :param agent_pos: current agent position
#         :param prey_pos: prey position
#         :param agent_dest: agent destination in relation to prey (0 for NORTH, 1 for SOUTH,
#                             2 for WEST, and 3 for EAST)

#         :return: movement index
#         """
    
#         def _get_prey_adj_locs(loc: Tuple) -> List[Tuple]:
#             prey_x = loc[0]
#             prey_y = loc[1]
#             return [(prey_x, prey_y - 1), (prey_x, prey_y + 1), (prey_x - 1, prey_y), (prey_x + 1, prey_y)]
        
#         def _move_vertically(distances) -> int:
#             if distances[1] > 0:
#                 return DOWN
#             elif distances[1] < 0:
#                 return UP
#             else:
#                 return STAY
            
#         def _move_horizontally(distances) -> int:
#             if distances[0] > 0:
#                 return RIGHT
#             elif distances[0] < 0:
#                 return LEFT
#             else:
#                 return STAY
            
#         prey_adj_locs = _get_prey_adj_locs(prey_pos)
#         distance_dest = np.array(prey_adj_locs[agent_dest]) - np.array(agent_pos)
#         abs_distances = np.absolute(distance_dest)
#         if abs_distances[0] > abs_distances[1]:
#             return _move_horizontally(distance_dest)
#         elif abs_distances[0] < abs_distances[1]:
#             return _move_vertically(distance_dest)
#         else:
#             roll = np.random.uniform(0, 1)
#             return _move_horizontally(distance_dest) if roll > 0.5 else _move_vertically(distance_dest)