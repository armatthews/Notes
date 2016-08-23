import sys
import math
import random
import signal
from collections import defaultdict
from windy_grid_draw import draw

import signal
import sys

# Board is a 10 by 7 grid
# The agent starts at the center of the 1st column
# Goal is at the center of the 3rd column frmo the right
# At each time step wind pushes the agent up a number of tiles
# depending on which column it is in:
# 0 0 0 1 1 1 2 2 1 0
# Agent receives a reward of -1 per timestep until it gets to the goal,
# at which point the episode terminates.

possible_actions = ['left', 'right', 'up', 'down']
alpha = 0.15 # step size
epsilon = 0.1 # epsilon greedy
gamma = 0.9 # future discounting
lamda = 0.9 # TD(lambda)

def ctrlc_handler(signal, frame):
  possible_actions = ['left', 'right', 'up', 'down']
  for y in range(6, -1, -1):
    for x in range(10):
      greedy_action = max(possible_actions, key=lambda action: agent.qvalues[(x, y), action])
      print greedy_action[0],
    print
  draw(agent.qvalues)
  sys.exit(0)
signal.signal(signal.SIGINT, ctrlc_handler)

class Agent:
  def __init__(self):
    self.qvalues = defaultdict(float) # ((x, y), A) --> real
    self.reset()

  def reset(self):
    self.x = 0
    self.y = 3

  def choose_action(self):
    if random.random() < epsilon:
      return random.choice(possible_actions)
    random.shuffle(possible_actions)
    return max(possible_actions, key=lambda action: self.qvalues[self.state(), action])

  def apply_action(self, action):
    wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
    self.y += wind[self.x]

    if action == 'left':
      self.x -= 1
    elif action == 'right':
      self.x += 1
    elif action == 'up':
      self.y += 1
    elif action == 'down':
      self.y -= 1

    if self.x < 0:
      self.x = 0
    elif self.x > 9:
      self.x = 9

    if self.y > 6:
      self.y = 6
    elif self.y < 0:
      self.y = 0

  def at_goal(self):
    return self.state() == (7, 3)

  def state(self):
    return (self.x, self.y)

agent = Agent()
episode = 0
while True:
  agent.reset()
  episode += 1
  history = []
  step_count = 0
  while not agent.at_goal():
    action = agent.choose_action()
    history.append((agent.state(), action))
    step_count += 1
    print episode, step_count, action
    agent.apply_action(action)

    greedy_action = max(possible_actions, key=lambda action: agent.qvalues[agent.state(), action])
    for i, (prev_state, prev_action) in enumerate(history):
      step_diff = step_count - i
      agent.qvalues[prev_state, prev_action] += alpha * math.pow(lamda * gamma, step_diff) * (-1 + gamma * agent.qvalues[agent.state(), greedy_action] - agent.qvalues[history[-1]])
