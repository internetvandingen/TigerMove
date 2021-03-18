from definitions import *

import random

class Bot:
  def __init__(self, name):
    self.name = name

  def getMove(self, board, canGoatsMove, legal_moves):
    raise NotImplementedError

  def game_ended(self, winner, board):
    raise NotImplementedError

class RandomBot(Bot):
  def getMove(self, board, canGoatsMove, legal_moves):
    return legal_moves[random.randrange(len(legal_moves))]

  def game_ended(self, winner, board):
    pass


class MonteCarloBot(Bot):
  def getMove(self, board, canGoatsMove, legal_moves):
    return legal_moves[random.randrange(len(legal_moves))]

  def game_ended(self, winner, board):
    pass
