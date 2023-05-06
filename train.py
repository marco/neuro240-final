import copy
import random
from tetris import *
import pickle
import sys

q = {}
a = 0.75
g = float(sys.argv[1])
explore = float(sys.argv[2])
actions = [-1, 0, 1]
it = 10000

def run_games(iterations):
  hi_score = 0
  hi_reward = 0

  print('iteration,score,hiscore,hireward')

  for i in range(iterations):
    game = Game()
    last_score = 0
    while not game.game_over:
      st = game.numerical_representation()
      random.shuffle(actions)
      at = actions[0] if random.random() < explore else max(actions, key=lambda a: q.get((st, a), 0))
      game.step(at)
      st1 = game.numerical_representation()
      reward = game.score - last_score
      last_score = game.score

      # Q-Leaning:
      q[(st, at)] = q.get((st, at), 0) + \
        a * (
          reward + \
            g * max([q.get((st1, a), 0) for a in actions]) - \
            q.get((st, at), 0)
        )

      # Sarsa:
      # random.shuffle(actions)
      # a1 = actions[0] if random.random() < explore else max(actions, key=lambda a: q.get((st1, a), 0))
      # q[(st, at)] = q.get((st, at), 0) + \
      #   a * (
      #     reward + \
      #       g * q.get((st1, a1), 0) - \
      #       q.get((st, at), 0)
      #   )

      if q[(st, at)] > hi_reward:
        hi_reward = q[(st, at)]

    configure_turtle()
    game.draw()

    if hi_score < game.score:
      hi_score = game.score

    print(str(i) + ',' + str(game.score) + ',' + str(hi_score) + ',' + str(hi_reward))

run_games(it)
with open('sarsa-{}-{}.pickle'.format(g, explore), 'wb') as file:
  pickle.dump(q, file)
