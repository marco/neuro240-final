import random
import copy
import turtle

X_MAX = 6
Y_MAX = 16
CELL_SIZE = 30
SHAPES = [
  # Line:
  [(0, 0), (1, 0), (2, 0), (3, 0)],
  [(0, 0), (0, 1), (0, 2), (0, 3)],

  # Cube:
  [(0, 0), (0, 1), (1, 0), (1, 1)],

  # L:
  [(0, 0), (0, 1), (0, 2), (1, 2)],
  [(0, 0), (0, 1), (1, 0), (2, 0)],
  [(0, 0), (1, 0), (1, 1), (1, 2)],
  [(0, 0), (1, 0), (2, 0), (0, -1)],

  # Z:
  [(0, 0), (0, 1), (1, 1), (1, 2)],
  [(0, 0), (1, 0), (1, -1), (2, -1)],

  # T:
  [(0, 0), (1, 0), (1, 1), (2, 0)],
  [(0, 0), (0, 1), (-1, 1), (0, 2)],
  [(0, 0), (0, 1), (1, 1), (0, 2)],
  [(0, 0), (1, 0), (1, -1), (2, 0)],
]
COLORS = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

class Game:
  def __init__(self):
    self.placed_pieces = []
    self.active_piece = random_start_piece()
    self.game_over = False
    self.score = 0
    self.steps = 0

  def numerical_representation(self):
    depths = self.column_depths_from_max()
    min_depth_found = min(depths)
    max_depth_represented = 2
    adjusted_depths = [min(d - min_depth_found, max_depth_represented) for d in depths]

    list_representation = adjusted_depths + [self.active_piece.shape_id, self.active_piece.start[0]]
    return tuple(list_representation)

  def column_depths_from_max(self):
    highest_points = {}

    for piece in self.placed_pieces:
      for tile in piece.get_tile_positions():
        if tile[1] < highest_points.get(tile[0], Y_MAX):
          highest_points[tile[0]] = tile[1]

    return [highest_points.get(i, Y_MAX) for i in range(X_MAX)]

  def step(self, x_action):
    if self.game_over:
      return

    self.steps += 1

    self.active_piece.start = (self.active_piece.start[0] + x_action, self.active_piece.start[1] + 1)

    if self.check_piece_touch():
      self.mark_active_as_placed()

      if self.check_piece_touch():
        self.game_over = True
        return

    self.process_rows()

  def process_rows(self):
    for j in reversed(range(Y_MAX)):
      if self.check_row_full(j):
        self.score += 1

        for p, piece in reversed(list(enumerate(self.placed_pieces))):
          for x, tile in reversed(list(enumerate(piece.get_tile_positions()))):
            if tile[1] == j:
              self.placed_pieces[p].shape.pop(x)
        for p, piece in reversed(list(enumerate(self.placed_pieces))):
          for x, tile in enumerate(piece.get_tile_positions()):
            if tile[1] < j:
              self.placed_pieces[p].shape[x] = (piece.shape[x][0], piece.shape[x][1] + 1)

  def check_row_full(self, j):
    for i in range(X_MAX):
      if not self.check_tile_at_position(i, j):
        return False

    return True

  def check_tile_at_position(self, i, j):
    for piece in self.placed_pieces:
      if (i, j) in piece.get_tile_positions():
        return True

    return False

  def mark_active_as_placed(self):
    self.placed_pieces.append(self.active_piece)
    self.active_piece = random_start_piece()

  def check_piece_touch(self):
    for other_piece in self.placed_pieces:
      for other_tile in other_piece.get_tile_positions():
        for active_tile in self.active_piece.get_tile_positions():
          if active_tile[0] == other_tile[0] and active_tile[1] + 1 == other_tile[1]:
            return True

    for active_tile in self.active_piece.get_tile_positions():
      if active_tile[1] + 1 >= Y_MAX:
        return True

    return False

  def draw(self):
    turtle.clear()

    for piece in self.placed_pieces:
      piece.draw_piece()

    self.active_piece.draw_piece()

class Piece:
  def __init__(self, start, shape_id, color):
    self.start = start
    self.shape = copy.deepcopy(SHAPES[shape_id])
    self.shape_id = shape_id
    self.color = color

  def get_tile_positions(self):
    return [(self.start[0] + offset[0], self.start[1] + offset[1]) for offset in self.shape]

  def draw_piece(self):
    for offset in self.shape:
      draw_cell(self.start[0] + offset[0], self.start[1] + offset[1], self.color)

def random_start_piece():
  return Piece(
    (random.choice(range(X_MAX)), 0),
    random.choice(range(len(SHAPES))),
    random.choice(COLORS)
  )

def draw_cell(x, y, color_):
  turtle.color('black', color_)
  turtle.begin_fill()
  turtle.goto(x * CELL_SIZE, y * CELL_SIZE)
  turtle.seth(0)
  turtle.forward(CELL_SIZE)
  turtle.rt(90)
  turtle.forward(CELL_SIZE)
  turtle.rt(90)
  turtle.forward(CELL_SIZE)
  turtle.rt(90)
  turtle.forward(CELL_SIZE)
  turtle.rt(90)
  turtle.end_fill()

def turtle_on_click(x, y):
  game.step(0)
  game.draw()

def configure_turtle():
  turtle.setworldcoordinates(-CELL_SIZE, Y_MAX * CELL_SIZE, Y_MAX * CELL_SIZE, -CELL_SIZE)
  turtle.penup()
  turtle.speed(0)
  turtle.tracer(False)
  turtle.onscreenclick(turtle_on_click)

