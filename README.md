Group 27
Daniela Machado - 92445
Mariana Laranjo - 92517
Ricardo Martins - 95662


In order to run the code, you need to open the terminal in the same directory as the lbforaging.py file, and use the following command line:

  python lbforaging.py --render --times #

In order to visualize the graphical form of the program you will need to have the --render argument.

To choose how many episodes the program will run, you need to add the argument --times # (where # is an integer greater than 0)



To pick what agent you want to run the program, you have to change it on line 99 in the following file:

  lbforaging/foraging/environment.py -> line 99

You choose from:
  - RandomAgent
  - GreedyAgent
  - SmartAgent



To enable/disable multi-agent cooperation, the user needs to switch the variable coop on line 20 of the following file:
  
  lbforaging/agents/smart_agent.py -> line 20 -> coop = True/False (True = Cooperation Enabled, False = Cooperation Disabled)


To change the settings of the environment, you will need to change the main() function in the lbforaging.py file:
  Variables:
    - s (line 105) -> Dimension of the grid (Ex.: s=5 creates a 5x5 grid)
    - p (line 106) -> Number of agents (Ex.: p=3 adds 3 agents per episode)
    - f (line 107) -> Number of emergencies/preys (Ex.: f=8 adds 8 emergencies per episode)
  
  You will also need to change line 122:

    env = gym.make("Foraging-{s}x{s}-{p}p-{f}f-v2")

  Where s, p and f values are the ones defined on the previous lines