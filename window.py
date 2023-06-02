import pygame

from piece import convert_shape_format
from themes import select_font

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


def draw_start_button(win, offset, font):
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
    # font = pygame.font.SysFont('comicsans', 35)
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
              start_button_coords["up"] + offset))

    return start_button_coords


def draw_theme_button(win, offset, theme, font):
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


def draw_text_middle(surface, text, font, color):
    """Writes the given text in the middle of the screen (surface).
    
    Inputs:
    surface -> display object in which to draw the text.
    text -> (string) text to be displayed.
    size -> (int) size of the text.
    color -> (tuple) RGB formatted color of the text.
    """

    label = font.render(text, 1, color)
    window_width = surface.get_width()
    window_height = surface.get_height()
    text_width = label.get_width()
    text_height = label.get_height()
    offset = 10

    coords = {
        "up": (window_height - text_height) / 2 - offset,
        "down": (window_height + text_height) / 2 + offset,
        "left": (window_width - text_width) / 2 - offset,
        "right": (window_width + text_width) / 2 + offset
    }

    pygame.draw.rect(surface = surface, color = (255, 0, 0),
                     rect = (coords["left"],
                             coords["up"],
                             text_width + offset * 2,
                             text_height + offset * 2),
                     border_radius = 0,
                     width = 0)
    
    surface.blit(label, (coords["left"] + offset,
              coords["up"] + offset))
   

def draw_grid(surface, grid, top_left_x, top_left_y, play_height, play_width,
              block_size):
    """Displays the game's grid in the given surface (screen).
    
    Inputs:
    surface -> display object in which to draw the text.
    grid -> array with the game's grid.
    """

    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size),
                         (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


def draw_guide_grid(surface, guide_grid, top_left_x, top_left_y, block_size):
    """Displays the handguide position in a separate grid.
    
    Inputs:
    surface -> display object in which to draw the grid.
    guide_grid -> array with the guide grid.
    top_left_x -> x position of the top left of the grid.
    top_left_y -> y position of the top left of the grid.
    block_size -> size of each block of the grid.
    """

    sx = top_left_x
    sy = top_left_y - 50
    for i in range(len(guide_grid)):
        for j in range(len(guide_grid[i])):
            pygame.draw.rect(surface, (128, 128, 128), (int(sx + j * block_size), 
                            int(sy + i * block_size), block_size, block_size), 1)


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
     

def draw_next_shape(shape, surface, top_left_x, top_left_y, play_height, play_width,
                    block_size, theme):
    """"""

    if theme == "normal":
        label_font = select_font(theme, 35)
    else:
        label_font = select_font(theme, 45)
    
    label = label_font.render("Next Shape:", 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 150
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size,
                                  block_size, block_size), 0)
                pygame.draw.rect(surface,
                                 (128,128,128),
                                 (int(sx + j * 30), int(sy + i * 30), 30, 30),
                                 1)
                
    surface.blit(label, (sx + 10, sy - 50))


def draw_window(top_left_x, top_left_y, play_height, play_width, block_size, surface,
                grid, guide_grid, theme, score = 0):
    """"""

    if theme == "normal":
        title_font = select_font(theme, 70)
        label_font = select_font(theme, 35)
    else:
        title_font = select_font(theme, 70)
        label_font = select_font(theme, 45)
    
    label = title_font.render("Hand Tetris", 1, (255, 255, 255))

    surface.blit(label,
                 (top_left_x + play_width / 2 - (label.get_width() / 2), 40)
    )

    # Score
    label = label_font.render("Score: " + str(score), 1, (255, 255, 255))

    score_x = top_left_x + play_width + 50
    score_y = top_left_y + play_height / 2 - 180
    top_left_y -= 80
    guide_top_left_y = top_left_y - 50

    surface.blit(label, (score_x + 10, score_y - 90))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size,
                              top_left_y + i * block_size, block_size, block_size), 0)
            
    for i in range(len(guide_grid)):
        for j in range(len(guide_grid[i])):
            pygame.draw.rect(surface, guide_grid[i][j],
                             (top_left_x + j * block_size,
                              guide_top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0),
                     (top_left_x, top_left_y, play_width, play_height), 4)
    
    pygame.draw.rect(surface, (255, 0, 0),
                     (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid, top_left_x, top_left_y, play_height, play_width,
              block_size)
    
    draw_guide_grid(surface, guide_grid, top_left_x, top_left_y, block_size)


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
