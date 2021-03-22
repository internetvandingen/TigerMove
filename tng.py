from definitions import *
from printing import print_board
from engine import Engine
from bot import Bot, RandomBot, MonteCarloBot

from state import State

tiger = RandomBot('tiger', T)
# goat = RandomBot('goat', G)
goat = MonteCarloBot('goat', G)
e = Engine(tiger, goat)


games = []
n = 1

for i in range(0,n):
  games.append(e.play(verbose=1))
  e.reset()


mean = 0.0
for game in games:
  mean =+ (game+1)/2

mean /= len(games)

print('{} games, goat win percentage: {}'.format(n, mean))


