from definitions import *

from state import State
from engine import Engine


import random

class Bot:
  def __init__(self, name, side):
    self.name = name
    self.side = side
    # random.seed(0)

  def getMove(self, state, legal_moves):
    raise NotImplementedError

  def game_ended(self, winner, state):
    raise NotImplementedError

class RandomBot(Bot):
  def getMove(self, state, legal_moves):
    return getRandomMove(state, legal_moves)

  def game_ended(self, winner, state):
    pass

values = (99, 10, 50, 10, 99,
          10,  1,  2,  1, 10,
          50,  2,  1,  2, 50,
          10,  1,  2,  1, 10,
          99, 10, 50, 10, 99)
def getGoatPlaceValues(legal_moves):
  probs = []
  for move in legal_moves:
    probs.append(values[move])
  return probs

class MonteCarloBot(Bot):
  def getMove(self, state, legal_moves):
    # if len(legal_moves) == 0:
    #   raise Exception("no legal moves left! Cannot make a move on state:\n{}".format(state.board))
    if state.movenr < 15:
      probabilities = getGoatPlaceValues(legal_moves)
    else:
      tiger = RandomBot('tiger', T)
      goat = RandomBot('goat', G)
      cm = Engine(tiger, goat)
      n = 50
      probabilities = []
      for move in legal_moves:
        moved_state = State(state)
        moved_state.parseMove(move)
        evaluation = 0.0
        for i in range(0,n):
          cm.reset_state(moved_state)
          result = cm.play(verbose=0)
          # evaluation += (0.001 + (1.0 + result) / 2.0) * (cm.state.movenr/5)
          # evaluation += (0.001 + (1.0 + result) / 2.0)
          evaluation += (1.0 + result) / 2.0
          # print("{}: sim {}: {} -> {}".format(move, i, result, evaluation))
        probabilities.append(evaluation / n)
    print("moves: {}".format(legal_moves))
    print("probs: {}".format(probabilities))
    print("board: {}".format(state.board))
    index = max(enumerate(probabilities),key=lambda x: x[1])[0]
    return legal_moves[index]
    # return random.choices(legal_moves, probabilities)[0]

  def game_ended(self, winner, state):
    pass


def getRandomMove(state, legal_moves):
  return legal_moves[random.randrange(len(legal_moves))]
