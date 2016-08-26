import math
import numpy as np
import matplotlib.pyplot as plt

def draw(qvalues):
  possible_actions = ['left', 'right', 'up', 'down']
  ax = plt.gca()

  ax.patch.set_facecolor('gray')
  ax.set_aspect('equal', 'box')
  ax.xaxis.set_major_locator(plt.NullLocator())
  ax.yaxis.set_major_locator(plt.NullLocator())

  for ((x, y), a), q in qvalues.iteritems():
    greedy_action = max(possible_actions, key=lambda action: qvalues[(x, y), action])
    if a != greedy_action:
      continue
    rect = plt.Rectangle([x, y], 1.0, 1.0, facecolor='white', edgecolor='black')
    ax.add_patch(rect)
    if a == 'left':
      dx = -1.0
      dy = 0.0
    elif a == 'right':
      dx = 1.0
      dy = 0.0
    elif a == 'up':
      dx = 0.0
      dy = 1.0
    elif a == 'down':
      dx = 0.0
      dy = -1.0
    color = 'g' if a == greedy_action else 'r'
    al = math.sqrt(dx * dx + dy * dy)
    aw = 0.35 * dx / al
    ah = 0.35 * dy / al
    ax.arrow(x + 0.5 - 0.5*aw, y + 0.5 - 0.5*ah, 0.35 * dx, 0.35 * dy, head_width=0.1, head_length=0.1, fc=color, ec=color)

  ax.text(0.5, 3.5, 'S')
  ax.text(7.5, 3.5, 'G')

  wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
  for i in range(10):
    ax.text(i + 0.5, -0.3, str(wind[i]))

  ax.autoscale_view()
  #ax.invert_yaxis()
  plt.show()
