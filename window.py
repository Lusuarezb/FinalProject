import pygame

from piece import convert_shape_format

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""


def create_guide_grid():
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(1)]
    return grid


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
    """Verifies if the player lost with the most upper occupied position."""

    for pos in positions:
        _, y = pos
        if y < 1:
            return True
    return False


def draw_start_button(win, offset):
    """Displays the start game button on the main menu.
    
    Inputs:
    win -> display object in which to draw the text.

    Returns:
    button coordinates.
    """

    window_width = win.get_width()
    window_height = win.get_height()

    start_button_color = (255, 255, 255)
    start_button_text_color = (255, 0, 0)
    font = pygame.font.SysFont('comicsans', 35)
    start_text = "Start game"
    start_text_width, start_text_height = font.size(start_text)
    start_button_text = font.render(start_text, True,
                                         start_button_text_color)

    start_button_coords = {
        "up": (window_height - start_text_height) / 2 - offset,
        "down": (window_height + start_text_height) / 2 + offset,
        "left": (window_width - start_text_width) / 2 - offset,
        "right": (window_width + start_text_width) / 2 + offset
    }

    pygame.draw.rect(surface = win, color = start_button_color,
                     rect = (start_button_coords["left"],
                             start_button_coords["up"],
                             start_text_width + offset * 2,
                             start_text_height + offset * 2),
                     width = 0)
    win.blit(start_button_text, (start_button_coords["left"] + offset,
              start_button_coords["up"]))

    return start_button_coords


def draw_theme_button(win, offset, theme):
    """Displays the theme selector button on the main menu.
    
    Inputs:
    win -> display object in which to draw the text.

    Returns:
    button coordinates.
    """

    window_width = win.get_width()
    window_height = win.get_height()

    theme_button_color = (255, 255, 255)
    theme_button_text_color = (0, 0, 255)
    font = pygame.font.SysFont('comicsans', 25)
    theme_text = f"Theme selected: {theme}"
    theme_text_width, theme_text_height = font.size(theme_text)
    theme_button_text = font.render(theme_text, True,
                                         theme_button_text_color)

    theme_button_coords = {
        "up": (window_height / 2 - theme_text_height) * 3 / 2 - offset,
        "down": (window_height / 2 + theme_text_height) * 3 / 2 + offset,
        "left": (window_width - theme_text_width) / 2 - offset,
        "right": (window_width + theme_text_width) / 2 + offset
    }

    pygame.draw.rect(surface = win, color = theme_button_color,
                     rect = (theme_button_coords["left"],
                             theme_button_coords["up"],
                             theme_text_width + offset * 2,
                             theme_text_height + offset * 2),
                     width = 0)
    win.blit(theme_button_text, (theme_button_coords["left"] + offset,
              theme_button_coords["up"] + offset))

    return theme_button_coords


def draw_instructions_button(win):
    """"""

    return


def draw_text_middle(surface, text, size, color, topLeftX, topLeftY, playHeight,
                     playWidth):
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


def draw_guide_grid(surface, guide_grid, topLeftX, topLeftY, blockSize):
    """Displays the handguide position in a separate grid.
    
    Inputs:
    surface -> display object in which to draw the grid.
    guide_grid -> array with the guide grid.
    topLeftX -> x position of the top left of the grid.
    topLeftY -> y position of the top left of the grid.
    blockSize -> size of each block of the grid.
    """

    sx = topLeftX
    sy = topLeftY - 50
    for i in range(len(guide_grid)):
        for j in range(len(guide_grid[i])):
            pygame.draw.rect(surface, (128, 128, 128), (int(sx + j * blockSize), 
                            int(sy + i * blockSize), blockSize, blockSize), 1)


def clear_rows(grid, locked, destruction_sound):
    """When a row is completed, it destroys the row and plays a sound.
    
    Inputs:
    grid -> array with the game's grid
    locked -> array with the locked positions.
    destruction_sound -> sound to be played when destroyed.
    """

    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]

        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            
            pygame.mixer.Sound.play(destruction_sound)

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


def draw_window(topLeftX, topLeftY, playHeight, playWidth, blockSize, surface, grid, guide_grid,
                score = 0):
    """"""

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render("Tetris", 1, (255, 255, 255))

    surface.blit(label,
                 (topLeftX + playWidth / 2 - (label.get_width() / 2), 30)
    )

    # Score
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Score: " + str(score), 1, (255, 255, 255))

    sx = topLeftX + playWidth + 50
    sy = topLeftY + playHeight / 2 - 150
    syy = topLeftY - 50

    surface.blit(label, (sx + 10, sy - 90))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (topLeftX + j * blockSize,
                              topLeftY + i * blockSize, blockSize, blockSize), 0)
            
    for i in range(len(guide_grid)):
        for j in range(len(guide_grid[i])):
            pygame.draw.rect(surface, guide_grid[i][j],
                             (topLeftX + j * blockSize,
                              syy + i * blockSize, blockSize, blockSize), 0)

    pygame.draw.rect(surface, (255, 0, 0),
                     (topLeftX, topLeftY, playWidth, playHeight), 4)
    
    pygame.draw.rect(surface, (255, 0, 0),
                     (topLeftX, topLeftY, playWidth, playHeight), 4)

    draw_grid(surface, grid, topLeftX, topLeftY, playHeight, playWidth,
              blockSize)
    
    draw_guide_grid(surface, guide_grid, topLeftX, topLeftY, blockSize)


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


def convert_frame(frame):
    """Converts the given frame to video surface for pygame."""

    video_surf = pygame.image.frombuffer(
              frame.tobytes(), frame.shape[1::-1], "BGR"
    )
    return video_surf
