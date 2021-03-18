from definitions import *

import random

class Bot:
  def __init__(self, name, side):
    self.name = name
    self.side = side

  def getMove(self, state, legal_moves):
    raise NotImplementedError

  def game_ended(self, winner, state):
    raise NotImplementedError

class RandomBot(Bot):
  def getMove(self, state, legal_moves):
    return getRandomMove(state, legal_moves)

  def game_ended(self, winner, state):
    pass


class MonteCarloBot(Bot):
  def getMove(self, state, legal_moves):
    return getRandomMove(state, legal_moves)

  def game_ended(self, winner, state):
    pass


def getRandomMove(state, legal_moves):
  return legal_moves[random.randrange(len(legal_moves))]
