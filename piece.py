from random import choice

from tetrominos import *

# Shape formats, positions and colors
shapes = [S, Z, I, O, J, L, T]
shape_valid_positions = [pos_S, pos_Z, pos_I, pos_O, pos_J, pos_L, pos_T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0),
                (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def get_shape():
    """Returns the next shape to be played."""

    return Piece(5, 0, choice(shapes))


def convert_shape_format(shape):
    """Converts the shape array of the given shape to a positions array.
    
    Inputs:
    shape -> Piece object.

    Returns:
    array with the shape's positions.
    """

    positions = []
    shape_format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)

        for j, column in enumerate(row):
            if column == "0":
                positions.append((shape.x + j, shape.y + i))
    
    for i, pos in enumerate(positions):
        positions[i]= (pos[0] - 2, pos[1] - 4)
    
    return positions
