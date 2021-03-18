from definitions import *
from printing import print_board

class Engine:
  def __init__(self, tigerBot, goatBot):
    self.tigerBot = tigerBot
    self.goatBot = goatBot
    self.reset()

  def set_board(self, board):
    self.board = board

  def get_board(self):
    return self.board

  def reset(self):
    self.board = self.get_start_board()
    self.canGoatsMove = False
    self.goatsEaten = 0
    self.movenr = 0
    self.hasWinner = E

  def get_start_board(self):
    return (T, E, E, E, T,
            E, E, E, E, E,
            E, E, E, E, E,
            E, E, E, E, E,
            T, E, E, E, T)

  def play(self, verbose=0):
    for i in range(0, 20):
      self.move_sequence(verbose)
      if self.hasWinner != E:
        break
    self.canGoatsMove = True
    while(self.movenr < MAX_MOVES and self.hasWinner == E):
      self.move_sequence(verbose)

    if self.hasWinner == T:
      self.goatBot.game_ended(False, self.board)
      self.tigerBot.game_ended(True, self.board)
    elif self.hasWinner == G:
      self.goatBot.game_ended(True, self.board)
      self.tigerBot.game_ended(False, self.board)

    return self.hasWinner

  def move_sequence(self, verbose):
    legalMoves = self.getLegalGoatMoves(self.board, self.canGoatsMove)
    if len(legalMoves) == 0:
      # raise Exception("{}: no legal moves for goat".format(self.movenr))
      self.hasWinner = T
      if verbose:
        print("no legal moves for goat")
      return
    goatMove = self.goatBot.getMove(self.board, self.canGoatsMove, legalMoves)
    if goatMove not in legalMoves:
      self.hasWinner = T
      if verbose:
        print("goat move {} is illegal, tiger wins".format(goatMove))
      return
    self.parseGoatMove(goatMove)

    if verbose > 0:
      print("{}: goat move: {}".format(self.movenr, goatMove))
      print(legalMoves)
      print_board(self.board)

    legalMoves = self.getLegalTigerMoves(self.board, self.canGoatsMove)
    if len(legalMoves) == 0:
      self.hasWinner = G
      if verbose:
        print("No legal move left for tigers, goats win!")
      return
    tigerMove = self.goatBot.getMove(self.board, self.canGoatsMove, legalMoves)
    if tigerMove not in legalMoves:
      self.hasWinner = G
      if verbose:
        print("tiger move {} is illegal, goat wins".format(tigerMove))
      return
    self.parseTigerMove(tigerMove)

    if verbose > 0:
      print("{}: tiger move: {}".format(self.movenr, tigerMove))
      print(legalMoves)
      print_board(self.board)
    if self.goatsEaten > 4:
      if verbose:
        print("5 goats have been eaten, tigers win!")
      self.hasWinner = T
      return
    self.movenr += 1

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

  def getLegalTigerMoves(self, board, canGoatsMove):
    available_moves = []
    for index in range(0, 25):
      if (board[index] == T):
        # moving 1 square
        squares = NEIGHBORS[index]
        for neighbor in squares:
          value = board[neighbor]
          if value == E:
            available_moves.append((index, neighbor))
          elif value == G:
            # check eating goats (jump over)
            extended_i = index//5 + (neighbor//5 - index//5)*2
            extended_j = index%5 + (neighbor%5 - index%5)*2
            if extended_i < 5 and extended_i > -1 and extended_j < 5 and extended_j > -1 and board[extended_i*5+extended_j] == E:
              available_moves.append((index, extended_i*5+extended_j))

    return available_moves

  def getLegalGoatMoves(self, board, canGoatsMove):
    available_moves = []
    if canGoatsMove:
      for index in range(0, 25):
        if (board[index] == G):
          squares = NEIGHBORS[index]
          for neighbor in squares:
            if board[neighbor] == E:
              available_moves.append((index, neighbor))
    else:
      for index in range(0, 25):
        if board[index] == E:
          available_moves.append(index)
    return available_moves

