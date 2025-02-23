import argparse
import logging
import random
import time
import math
import gym
import numpy as np
import lbforaging
from lbforaging.foraging.environment import Action
import matplotlib.pyplot as plt
gym.logger.set_level(40)
from gym.envs.registration import register


logger = logging.getLogger(__name__)

def z_table(confidence):
    return {
        0.99: 2.576,
        0.95: 1.96,
        0.90: 1.645
    }[confidence]

def standard_error(std_dev, n, confidence):
    return z_table(confidence) * (std_dev / math.sqrt(n))

def plot_confidence_bar(names, means, std_devs, N, title, x_label, y_label, confidence, show=False, filename=None, colors=None, yscale=None):
    errors = [standard_error(std_devs[i], N[i], confidence) for i in range(len(means))]
    fig, ax = plt.subplots()
    x_pos = np.arange(len(names))
    ax.bar(x_pos, means, yerr=errors, align='center', alpha=0.5, color=colors if colors is not None else "gray", ecolor='black', capsize=10)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(names)
    ax.set_title(title)
    ax.yaxis.grid(True)
    if yscale is not None:
        plt.yscale(yscale)
    plt.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    if show:
        plt.show()
    plt.close()

def compare_results(results, confidence=0.95, title="Agents Comparison", metric="Steps Per Episode", colors=None):
    names = list(results.keys())
    means = [result.mean() for result in results.values()]
    stds = [result.std() for result in results.values()]
    N = [result.size for result in results.values()]

    plot_confidence_bar(
        names=names,
        means=means,
        std_devs=stds,
        N=N,
        title=title,
        x_label="", y_label=f"Avg. {metric}",
        confidence=confidence, show=True, colors=colors
    )

def bar_plot(solved):
    fig = plt.figure(figsize = (10, 5))
    

    episodes = list(range(1,len(solved)+1,1))

    # creating the bar plot
    plt.bar(episodes, solved, color ='maroon',
            width = 0.4)
    plt.axhline(y=sum(solved) / len(solved),linewidth=1, color='blue')
    plt.yticks(np.arange(0, max(solved)+1, 1))
    plt.xticks(np.arange(1, max(episodes)+1, 1))
    plt.xlabel("Episode")
    plt.ylabel("No. of emergencies solved")
    plt.title("Number of emergencies solved per episode")
    plt.show()

def main(game_count=1, render=False):
    s=10
    p=3
    f=8
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
    env = gym.make("Foraging-10x10-3p-8f-v2")

    size_results = game_count*f
    results = np.zeros(size_results)
    last_position = 0
    emergencies_solved= []
    for episode in range(game_count):
        obs = env.reset()
        steps = 0
        done = False
        emergencies_solved+= [0,]

        if render:
            env.render()
            time.sleep(0.5)

        while not done:
            steps+=1
            actions = env.action_space

            nobs, nreward, ndone, _ = env.step(actions)

            if env.solved > emergencies_solved[episode]:
                emergencies_solved[episode]+=1

            if sum(nreward) > 0:
                print(nreward)

            if render:
                env.render()
                time.sleep(0.5)

            done = np.all(ndone)
        
        for i in range(len(env.solved_steps)):
            if env.solved_steps[i] == 0:
                results[last_position + i] = 50
            else:
                results[last_position+i] = env.solved_steps[i]
        last_position = last_position+i+1
    

    bar_plot(emergencies_solved)

    final = {
        env.players[0].name: results
    }
    compare_results(final, title=env.players[0].name, colors=["orange"])

        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play the level foraging game.")

    parser.add_argument("--render", action="store_true")
    parser.add_argument(
        "--times", type=int, default=1, help="How many times to run the game"
    )

    args = parser.parse_args()
    main(args.times, args.render)
