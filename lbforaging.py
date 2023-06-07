import argparse
import logging
import random
import time
import gym
import numpy as np
import lbforaging
from lbforaging.foraging.environment import Action
gym.logger.set_level(40)
from gym.envs.registration import register


logger = logging.getLogger(__name__)


def _game_loop(env, render):
    """
    """
    obs = env.reset()
    done = False

    if render:
        env.render()
        time.sleep(0.5)

    while not done:

        actions = env.action_space
        #print(env.Observation)

        nobs, nreward, ndone, _ = env.step(actions)
        if sum(nreward) > 0:
            print(nreward)

        if render:
            env.render()
            time.sleep(0.5)

        done = np.all(ndone)
    #print(env.players[0].score, env.players[1].score)


def main(game_count=1, render=False):
    s=8
    p=3
    f=2
    c=0
    register(
        id="Foraging-{0}x{0}-{1}p-{2}f{3}-v2".format(s, p, f, "-coop" if c else ""),
        entry_point="lbforaging.foraging:ForagingEnv",
        kwargs={
            "players": p,
            "max_food_level": 10,
            "field_size": (s, s),
            "max_food": f,
            "sight": s,
            "max_episode_steps": 50,
            "force_coop": c,
        },
    )
    env = gym.make("Foraging-8x8-3p-2f-v2")
    obs = env.reset()

    for episode in range(game_count):
        _game_loop(env, render)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play the level foraging game.")

    parser.add_argument("--render", action="store_true")
    parser.add_argument(
        "--times", type=int, default=1, help="How many times to run the game"
    )

    args = parser.parse_args()
    main(args.times, args.render)
