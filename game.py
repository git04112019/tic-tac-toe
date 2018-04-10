from board import Board

class Game(object):
  '''
  A game of TicTacToe.
  '''
  def __init__(self):
    self.new_game()

  def new_game(self):
    self._board = Board()

    ended = False
    while not ended:
      board = self._board

      if board.player_1_turn():
        next_move = self._get_user_input()
        print(f"Player has input {next_move}")
      else:
        try:
          next_move = self._get_ai_move()
          print(f"Computer has input {next_move}")
        except NotImplementedError:
          next_move = self._get_user_input()
          print(f"Player 2 has input {next_move}")

      if not next_move:
        print("Exiting...")
        return
      
      if board.move(next_move) or not board.has_blank_positions():
        ended = True
        status = board.check_winner()
        if status[0]:
          print("The player has won!")
        elif status[1]:
          print("The computer has won...")
        else:
          print ("It's a tie!")

      board.print_board()

  def _get_user_input(self):
    '''
    Attempts to get a valid board position from the user in the format of 'x,y', where x and y are integers between 0 and 2 inclusive. Loops until a valid input is received.
    '''
    has_valid_input = False

    while not has_valid_input:
      try:
        print("Enter your next move (should be 'x,y' pair indicating position on the board):")
        user_input = input()
        if user_input == "exit":
          return False

        inputs = tuple(map(int, user_input.split(',')))
        if len(inputs) != 2:
          raise ValueError("User input is invalid. Please enter a pair of (x,y) value separated by comma, e.g. 1,2.")
        elif inputs not in self._board.available_positions():
          raise ValueError("Position is already occupied, please select another one.")
        else: 
          has_valid_input = True
          return inputs
      except ValueError as e:
        print(f"Failed to parse input: {e}")
  
  def _get_ai_move(self):
    board = self._board
    self.node_counter = 0
    move = self._get_next_move(board)[0]
    print(f"{self.node_counter} nodes explored.")
    return move

  def _get_next_move(self, board, is_max=True, step=0, alpha=-float('inf'), beta=float('inf')):
    '''
    The board in which the next move should be returned.
    '''
    step -= 1    
    positions = board.available_positions()
    best_pos = positions[0]

    for i in range(0, len(positions)):
      position = positions[i]
      pos_val = self._get_pos_value(position, board, is_max, step, alpha, beta)
      
      if is_max:
        if pos_val > alpha: 
          alpha = pos_val
          best_pos = position
      else:
        if pos_val < beta:
          beta = pos_val
          best_pos = position

      if (is_max and beta < alpha) or (not is_max and alpha > beta):
        break
        
    return (best_pos, alpha if is_max else beta)

  def _get_pos_value(self, position, board, is_max, step, alpha, beta):
    '''
    Returns a value for a given position.
    '''
    self.node_counter += 1
    copy = board.deep_copy()
    
    if copy.move(position):
      val = float('inf') if is_max else -float('inf')
      return val
    elif not copy.has_blank_positions():
      # Ideally an heuristic should be used to score the board after a certain
      # number of steps, but this will do since the search space is limited.
      return step
    else:
      return self._get_next_move(copy, not is_max, step, alpha, beta)[1]


game = Game()