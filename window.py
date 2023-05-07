import pygame

from piece import convert_shape_format

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

def create_grid(locked_pos = {}):
    """Creates the game's grid positions. The grid consists of each cell, and
    each cell contains...

    Inputs:
    locked_pos -> dictionary with ...

    Returns:
    array with the grid positions.
    """

    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def valid_space(shape, grid):
    """Checks if the shape is occupying valid spaces.
    
    Inputs:
    shape -> Piece object.
    grid -> array with the grid positions.

    Returns:
    boolean indicating whether the shape is occupying valid spaces.
    """

    accepted_pos = [[(j, i) for j in range(10)
                     if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub] # Hacer la lista unidimensional
    shape_formatted = convert_shape_format(shape)

    for pos in shape_formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    """"""

    for pos in positions:
        _, y = pos
        if y < 1:
            return True
    return False


def draw_text_middle(surface, text, size, color, topLeftX, topLeftY, playHeight, playWidth):
    """Writes the given text in the middle of the screen (surface).
    
    Inputs:
    surface -> display object in which to draw the text.
    text -> (string) text to be displayed.
    size -> (int) size of the text.
    color -> (tuple) RGB formatted color of the text.
    """

    font = pygame.font.SysFont("comicsans", size, bold = True)
    label = font.render(text, 1, color)
    surface.blit(
        label, (topLeftX + playWidth / 2 - (label.get_width() / 2),
                topLeftY + playHeight / 2 - label.get_height() / 2)
    )
   

def draw_grid(surface, grid, topLeftX, topLeftY, playHeight, playWidth,
              blockSize):
    """Displays the game's grid in the given surface (screen).
    
    Inputs:
    surface -> display object in which to draw the text.
    grid -> array with the game's grid.
    """

    sx = topLeftX
    sy = topLeftY

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * blockSize),
                         (sx + playWidth, sy + i * blockSize))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * blockSize, sy),
                             (sx + j * blockSize, sy + playHeight))


def clear_rows(grid, locked):
    """"""

    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]

        if (0, 0, 0) not in row:
            inc += 1
            ind = i

            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]: # Sort list by Y value
            x, y = key

            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    
    return inc
     

def draw_next_shape(shape, surface, topLeftX, topLeftY, playHeight, playWidth,
                    blockSize):
    """"""

    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next Shape", 1, (255, 255, 255))

    sx = topLeftX + playWidth + 50
    sy = topLeftY + playHeight / 2 - 150
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * blockSize, sy + i * blockSize,
                                  blockSize, blockSize), 0)
                pygame.draw.rect(surface,
                                 (128,128,128),
                                 (int(sx + j * 30), int(sy + i * 30), 30, 30),
                                 1)
                
    
    surface.blit(label, (sx + 10, sy - 50))


def draw_window(topLeftX, topLeftY, playHeight, playWidth, blockSize, surface, grid,
                score = 0):
    """"""

    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render("Tetris", 1, (255, 255, 255))

    surface.blit(label,
                 (topLeftX + playWidth / 2 - (label.get_width() / 2), 30)) # Tetris 

    # Score
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Score: " + str(score), 1, (255, 255, 255))

    sx = topLeftX + playWidth + 50
    sy = topLeftY + playHeight / 2 - 150

    surface.blit(label, (sx + 10, sy - 90))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (topLeftX + j * blockSize,
                              topLeftY + i * blockSize, blockSize, blockSize), 0)

    pygame.draw.rect(surface, (255, 0, 0),
                     (topLeftX, topLeftY, playWidth, playHeight), 4)

    draw_grid(surface, grid, topLeftX, topLeftY, playHeight, playWidth,
              blockSize)
    #pygame.display.update()


def get_direction(old_x, new_x):
    """Returns the movement's direction of the current shape given the
    previous and current X position.
    
    Inputs:
    old_x -> int with the previous X position.
    new_x -> int with the current X position.

    Returns:
    string the movement's direction.
    """

    if new_x - old_x > 0:
        return "right"
    else:
        return "left"
