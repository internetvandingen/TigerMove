E =  0 # empty
T = -1 # tiger
G =  1 # goat

MAX_MOVES = 50


NEIGHBORS = (
  (1,5,6),
  (0,2,6),
  (1,3,6,7,8),
  (2,4,8),
  (3,8,9),
  (0,6,10),
  (0,1,2,5,7,10,11,12),
  (2,6,8,12),
  (2,3,4,7,9,12,13,14),
  (4,8,14),
  (5,6,11,15,16),
  (6,10,12,16),
  (6,7,8,11,13,16,17,18),
  (8,12,14,18),
  (8,9,13,18,19),
  (10,16,20),
  (10,11,12,15,17,20,21,22),
  (12,16,18,22),
  (12,13,14,17,19,22,23,24),
  (14,18,24),
  (15,16,21),
  (16,20,22),
  (16,17,18,21,23),
  (18,22,24),
  (18,19,23))
