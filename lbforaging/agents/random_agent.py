import random

from lbforaging.foraging.agent import Agent
#from lbforaging.foraging.environment import Action


class RandomAgent(Agent):
    name = "Random Agent"

    def step(self, obs):
        return random.choice(obs.actions)
