from definitions import *

PADDING = "  "

def print_board(board):
  print("")
  i=0
  print_row(board, i)
  i+=1
  print(PADDING+"   | \\ | / | \\ | / |")
  print_row(board, i)
  i+=1
  print(PADDING+"   | / | \\ | / | \\ |")
  print_row(board, i)
  i+=1
  print(PADDING+"   | \\ | / | \\ | / |")
  print_row(board, i)
  print(PADDING+"   | / | \\ | / | \\ |")
  i+=1
  print_row(board, i)
  print("")

def print_row(board, i):
  print(PADDING+"{:2d} {} — {} — {} — {} — {}".format(i*5,
    print_square(board[i*5+0]),
    print_square(board[i*5+1]),
    print_square(board[i*5+2]),
    print_square(board[i*5+3]),
    print_square(board[i*5+4])))

def print_square(square):
  if square == E:
    return " "
  elif square == G:
    return "o"
  elif square == T:
    return "#"
  else:
    return "."
