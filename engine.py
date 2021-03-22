from definitions import *
from state import State
from printing import print_board

class Engine:
  def __init__(self, tigerBot, goatBot):
    self.bots = [goatBot, tigerBot]
    self.reset()

  def reset(self):
    self.state = State()
    self.hasWinner = E

  def reset_state(self, state):
    self.state = State(state)
    self.hasWinner = state.getWinner()

  def play(self, verbose=0):
    while(self.state.movenr < MAX_MOVES and self.hasWinner == E):
      self.move_sequence(verbose)

    if self.hasWinner == T:
      self.bots[0].game_ended(False, self.state)
      self.bots[1].game_ended(True, self.state)
    elif self.hasWinner == G:
      self.bots[0].game_ended(True, self.state)
      self.bots[1].game_ended(False, self.state)

    return self.hasWinner

  def move_sequence(self, verbose):
    legalMoves = self.state.getLegalMoves()
    if len(legalMoves) == 0:
      raise Exception("{}: no legal moves in state:\n".format(self.state.movenr, self.state.board))
      # self.hasWinner = -1*self.state.whosTurn
      # if verbose:
      #   print("no legal moves for goat")
      # return
    botInTurnIndex = 0 if self.state.whosTurn == G else 1
    move = self.bots[botInTurnIndex].getMove(self.state, legalMoves)
    if move not in legalMoves:
      raise Exception("{}: illegal move: {} in state:\n{}".format(self.state.movenr, move, self.state.board))
      # self.hasWinner = -1*self.state.whosTurn
      # if verbose:
      #   print("move {} is illegal, {} wins".format(move, self.hasWinner))
      # return
    self.state.parseMove(move)

    if verbose > 0:
      print("{}: move: {}, has been eaten: {}".format(self.state.movenr, move, self.state.goatsEaten))
      # print(legalMoves)
      print_board(self.state.board)

    self.hasWinner = self.state.getWinner()


