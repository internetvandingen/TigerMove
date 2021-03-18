from definitions import *

class State:
  def __init__(self, state=None):
    if state==None:
      self.board = self.get_start_board()
      self.canGoatsMove = False
      self.goatsEaten = 0
      self.movenr = 0
      self.whosTurn = G
    else:
      self.board = state.board
      self.canGoatsMove = state.canGoatsMove
      self.goatsEaten = state.goatsEaten
      self.movenr = state.movenr
      self.whosTurn = state.whosTurn

  def get_start_board(self):
    return (T, E, E, E, T,
            E, E, E, E, E,
            E, E, E, E, E,
            E, E, E, E, E,
            T, E, E, E, T)

  def getLegalMoves(self):
    if self.whosTurn == T:
      return self._getLegalTigerMoves()
    else:
      return self._getLegalGoatMoves()

  def _getLegalTigerMoves(self):
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

  def _getLegalGoatMoves(self):
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

  def parseMove(self, move):
    if self.whosTurn == T:
      self._parseTigerMove(move)
      if self.movenr == 20:
        self.canGoatsMove = True
    else:
      self.movenr += 1
      self._parseGoatMove(move)
    self.whosTurn *= -1


  def _parseGoatMove(self, goatMove):
    if self.canGoatsMove:
      move_from = goatMove[0]
      move_to = goatMove[1]
      diff_y = move_to//5 - move_from//5
      diff_x = move_to%5 - move_from%5
      self.board = self.board[:move_from] + (E,) + self.board[move_from+1:]
      self.board = self.board[:move_to] + (G,) + self.board[move_to+1:]
    else:
      self.board = self.board[:goatMove] + (G,) + self.board[goatMove+1:]

  def _parseTigerMove(self, tigerMove):
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
    elif len(self._getLegalTigerMoves()) == 0:
      return G
    else:
      return E
