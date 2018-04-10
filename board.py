import numpy as np
import copy

class Board(object):
  '''
  A board for a game of TicTacToe.
  '''
  def __init__(self):
    self.PLAYER_1 = "O"
    self.PLAYER_2 = "X"
    self.BLANK = "-"
    self.new_game()
  
  def new_game(self):
    '''
    Resets the board.
    '''
    self._cur_player = self.PLAYER_1
    self._board = np.full((3,3), self.BLANK)

  def move(self, position=(0,0)):
    '''
    Places a piece on the board at the specified position. Returns True if the current player has won after having made the move.
    '''
    if not isinstance(position[0], int) or not isinstance(position[1], int):
      raise ValueError("A tuple of integers is expected as the position value")
    if self._board[position[0]][position[1]] != self.BLANK:
      raise ValueError("The specified position is occupied.")

    self._board[position[0]][position[1]] = self._cur_player

    if self._is_winner(self._cur_player):
      return True

    is_player_1_turn = self._cur_player == self.PLAYER_1
    self._cur_player = self.PLAYER_2 if is_player_1_turn else self.PLAYER_1
    return False
  
  def deep_copy(self):
    '''
    Returns a deep copy of the board.
    '''
    return copy.deepcopy(self)

  def player_1_turn(self):
    '''
    Returns a boolean value, whether it's currently player 1's turn.
    '''
    return self._cur_player == self.PLAYER_1

  def player_2_turn(self):  
    '''
    Returns a boolean value, whether it's currently player 2's turn.
    '''
    return not self._cur_player == self.PLAYER_2

  def has_blank_positions(self):
    '''
    Returns a boolean value, whether there are anymore spaces left on the board.
    '''
    return self.BLANK in self._board

  def available_positions(self):
    '''
    Returns a list of tuples containing the (x,y) positions that are still available on the board.
    '''
    board = self._board
    positions = []
    for i in range(0, 3):
      for j in range(0, 3):
        if board[i][j] == self.BLANK:
          positions.append((i, j)) 
    return positions

  def check_winner(self):
    '''
    Returns a duple of boolean values, the first represent whether player 1 has won, and the second value represents whether player 2 has won.
    '''
    player_1_win = self._is_winner(self.PLAYER_1)
    player_2_win = self._is_winner(self.PLAYER_2)
    return (player_1_win, player_2_win)
    
  def print_board(self):
    print(self._board)

  def _is_winner(self, player):
    board = self._board
    rows = np.array(board)
    columns = np.array([ board[:, i] for i in range(0, 3) ])
    diagonals = np.array([np.diagonal(board), [board[0][2], board[1][1], board[2][0]]])
    slices = np.concatenate((rows, columns, diagonals))

    # Creates a boolean mask
    result = np.isin(slices, np.full((3), player))
    # np.sum() should sum all of the boolean values, where True=1 and False=0
    return 3 in [np.sum(r) for r in result]
