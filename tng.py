from definitions import *
from printing import print_board
from engine import Engine
from bot import Bot, RandomBot, MonteCarloBot



tiger = RandomBot('tiger', T)
goat = RandomBot('goat', G)
e = Engine(tiger, goat)

games = []
n = 1000

for i in range(0,n):
  games.append(e.play(verbose=0))
  e.reset()


mean = 0.0
for game in games:
  mean =+ (game+1)/2

mean /= len(games)

print('{} games, goat win percentage: {}'.format(n, mean))


