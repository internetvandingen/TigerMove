from definitions import *
from printing import print_board

class State:
  def __init__(self, state=None):
    if state==None:
      self.board = self.get_start_board()
      self.canGoatsMove = False
      self.goatsEaten = 0
    else:
      self.board = state.board
      self.canGoatsMove = state.canGoatsMove
      self.goatsEaten = state.goatsEaten

  def get_start_board(self):
    return (T, E, E, E, T,
            E, E, E, E, E,
            E, E, E, E, E,
            E, E, E, E, E,
            T, E, E, E, T)

  def getLegalTigerMoves(self):
    available_moves = []
    for index in range(0, 25):
      if (self.board[index] == T):
        # moving 1 square
        squares = NEIGHBORS[index]
        for neighbor in squares:
          value = self.board[neighbor]
          if value == E:
            available_moves.append((index, neighbor))
          elif value == G:
            # check eating goats (jump over)
            extended_i = index//5 + (neighbor//5 - index//5)*2
            extended_j = index%5 + (neighbor%5 - index%5)*2
            if extended_i < 5 and extended_i > -1 and extended_j < 5 and extended_j > -1 and self.board[extended_i*5+extended_j] == E:
              available_moves.append((index, extended_i*5+extended_j))

    return available_moves

  def getLegalGoatMoves(self):
    available_moves = []
    if self.canGoatsMove:
      for index in range(0, 25):
        if (self.board[index] == G):
          squares = NEIGHBORS[index]
          for neighbor in squares:
            if self.board[neighbor] == E:
              available_moves.append((index, neighbor))
    else:
      for index in range(0, 25):
        if self.board[index] == E:
          available_moves.append(index)
    return available_moves

  def parseGoatMove(self, goatMove):
    if self.canGoatsMove:
      move_from = goatMove[0]
      move_to = goatMove[1]
      diff_y = move_to//5 - move_from//5
      diff_x = move_to%5 - move_from%5
      self.board = self.board[:move_from] + (E,) + self.board[move_from+1:]
      self.board = self.board[:move_to] + (G,) + self.board[move_to+1:]
    else:
      self.board = self.board[:goatMove] + (G,) + self.board[goatMove+1:]
    return E

  def parseTigerMove(self, tigerMove):
    move_from = tigerMove[0]
    move_to = tigerMove[1]
    diff_y = move_to//5 - move_from//5
    diff_x = move_to%5 - move_from%5
    if abs(diff_x)>1 or abs(diff_y)>1:
      goat_index = (move_from//5 + diff_y//2)*5 + (move_from%5 + diff_x//2)
      self.goatsEaten += 1
      self.board = self.board[:goat_index] + (E,) + self.board[goat_index+1:]
    self.board = self.board[:move_from] + (E,) + self.board[move_from+1:]
    self.board = self.board[:move_to] + (T,) + self.board[move_to+1:]

  def getWinner(self):
    if self.goatsEaten > 4:
      return T
    elif len(self.getLegalTigerMoves()) == 0:
      return G
    else:
      return E


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


