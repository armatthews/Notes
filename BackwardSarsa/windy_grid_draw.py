import math
import numpy as np
import matplotlib.pyplot as plt

def hinton(matrix, ax=None):
    ax = ax if ax is not None else plt.gca()

    ax.patch.set_facecolor('gray')
    ax.set_aspect('equal', 'box')
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())

    for (x, y), w in np.ndenumerate(matrix):
        color = 'white' if w > 0 else 'black'
        size = 1.
        rect = plt.Rectangle([x, y], size, size, facecolor=color, edgecolor=color)

        c = plt.Circle([x + size / 2, y + size / 2], 0.1, color='g')
        if w > 0.25:
          ax.arrow(x + size/2, y + size/2, 0.0, 0.35, head_width=0.05, head_length=0.1, fc='r', ec='r')
        elif w < -0.25:
          ax.arrow(x + size/2, y + size/2, -0.35, -0.0, head_width=0.05, head_length=0.1, fc='r', ec='r')
        ax.add_patch(rect)
        ax.add_patch(c)

    circle = plt.Circle((0, 0), 1.0, color='g')
    ax.add_patch(circle)

    ax.autoscale_view()
    ax.invert_yaxis()

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
    ax.arrow(x + 0.5, y + 0.5, 0.35 * dx, 0.35 * dy, head_width=0.05, head_length=0.1, fc=color, ec=color)

  """for (x, y), w in np.ndenumerate(matrix):
      color = 'white' if w > 0 else 'black'
      size = 1.
      rect = plt.Rectangle([x, y], size, size, facecolor=color, edgecolor=color)

      c = plt.Circle([x + size / 2, y + size / 2], 0.1, color='g')
      if w > 0.25:
        ax.arrow(x + size/2, y + size/2, 0.0, 0.35, head_width=0.05, head_length=0.1, fc='r', ec='r')
      elif w < -0.25:
        ax.arrow(x + size/2, y + size/2, -0.35, -0.0, head_width=0.05, head_length=0.1, fc='r', ec='r')
      ax.add_patch(rect)
      ax.add_patch(c)"""

  ax.text(0.5, 3.5, 'S')
  ax.text(7.5, 3.5, 'G')

  ax.autoscale_view()
  #ax.invert_yaxis()
  plt.show()

if __name__ == '__main__':
    hinton(np.random.rand(10, 7) - 0.5)
    plt.show()
