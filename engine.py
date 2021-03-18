from definitions import *
from State import State
from printing import print_board

class Engine:
  def __init__(self, tigerBot, goatBot):
    self.tigerBot = tigerBot
    self.goatBot = goatBot
    self.reset()

  def reset(self):
    self.state = State()
    self.movenr = 0
    self.hasWinner = E

  def play(self, verbose=0):
    for i in range(0, 20):
      self.move_sequence(verbose)
      if self.hasWinner != E:
        break
    self.state.canGoatsMove = True
    while(self.movenr < MAX_MOVES and self.hasWinner == E):
      self.move_sequence(verbose)

    if self.hasWinner == T:
      self.goatBot.game_ended(False, self.state)
      self.tigerBot.game_ended(True, self.state)
    elif self.hasWinner == G:
      self.goatBot.game_ended(True, self.state)
      self.tigerBot.game_ended(False, self.state)

    return self.hasWinner

  def move_sequence(self, verbose):
    legalMoves = self.state.getLegalGoatMoves()
    if len(legalMoves) == 0:
      # raise Exception("{}: no legal moves for goat".format(self.movenr))
      self.hasWinner = T
      if verbose:
        print("no legal moves for goat")
      return
    goatMove = self.goatBot.getMove(self.state, legalMoves)
    if goatMove not in legalMoves:
      self.hasWinner = T
      if verbose:
        print("goat move {} is illegal, tiger wins".format(goatMove))
      return
    self.state.parseGoatMove(goatMove)

    if verbose > 0:
      print("{}: goat move: {}".format(self.movenr, goatMove))
      print(legalMoves)
      print_board(self.state.board)

    legalMoves = self.state.getLegalTigerMoves()
    if len(legalMoves) == 0:
      self.hasWinner = G
      if verbose:
        print("No legal move left for tigers, goats win!")
      return
    tigerMove = self.goatBot.getMove(self.state, legalMoves)
    if tigerMove not in legalMoves:
      self.hasWinner = G
      if verbose:
        print("tiger move {} is illegal, goat wins".format(tigerMove))
      return
    self.state.parseTigerMove(tigerMove)

    if verbose > 0:
      print("{}: tiger move: {}".format(self.movenr, tigerMove))
      print(legalMoves)
      print_board(self.state.board)
    if self.state.goatsEaten > 4:
      if verbose:
        print("5 goats have been eaten, tigers win!")
      self.hasWinner = T
      return
    self.movenr += 1


