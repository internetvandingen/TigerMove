from definitions import *
from printing import print_board
from engine import Engine
from bot import Bot, RandomBot, MonteCarloBot



tiger = MonteCarloBot('tiger', T)
goat = MonteCarloBot('goat', G)
e = Engine(tiger, goat)

games = []
n = 1

for i in range(0,n):
  games.append(e.play(verbose=1))
  e.reset()


mean = 0
for game in games:
  mean =+ game

mean /= len(games)

print('{} games, goat win percentage: {}'.format(n, mean))


