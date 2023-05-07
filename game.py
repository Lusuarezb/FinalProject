import random

import pygame

from camera import *
from tetrominos import *

# TODO:
# Comentarios en Ingles - Luis
# Snake Case - Luis 
# 80 Caracteres horizontal - David
# Separar en scripts - David
# Espaciado entre operadores y valores - David

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# Global Variables
s_width = 1600
s_height = 900
playWidth = 300  # meaning 300 // 10 = 30 width per block
playHeight = 600  # meaning 600 // 20 = 30 height per block
blockSize = 30

topLeftX = (s_width - playWidth) // 2
topLeftY = s_height - playHeight

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


def get_shape():
    """Returns the next shape to be played."""

    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
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
   

def draw_grid(surface, grid):
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
     

def draw_next_shape(shape, surface):
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


def draw_window(surface, grid, score = 0):
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

    draw_grid(surface, grid)
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


def main(win):
    """Main execution of the game.

    Inputs:
    win  surface object with the screen to display.
    """

    run = True
    lockedPositions = {}
    grid = create_grid(lockedPositions)
    changePiece = False
    currentPiece = get_shape()
    nextPiece = get_shape()
    clock = pygame.time.Clock()
    fallTime = 0
    fallSpeed = 0.27
    levelTime = 0
    score = 0

    # Direction
    old_hand_position = 5

    # Camera
    camera_captured, hands, hands_detector, hands_drawing = camera_settings()
    window_width = camera_captured.get(3)

    while run:
        current_piece_position_array = (
            shape_valid_positions[shapes.index(currentPiece.shape)]
        )
        position_values = (
            current_piece_position_array[currentPiece.rotation 
                                         % len(current_piece_position_array)]
        )
        max_position_value = max(
            current_piece_position_array[currentPiece.rotation 
                                         % len(current_piece_position_array)]
        )
        hand_position = hand_controller(camera_captured, window_width, hands,
                                        hands_detector, hands_drawing,
                                        currentPiece.x, position_values)

        if hand_position >= (max_position_value + 1):
            hand_position = max_position_value

        grid = create_grid(lockedPositions)
        fallTime += clock.get_rawtime()
        levelTime += clock.get_rawtime()
        clock.tick()

        if levelTime / 1000 > 5:
            levelTime = 0

            if fallSpeed > 0.12:
                fallSpeed -= -0.01

        if fallTime / 1000 >= fallSpeed:
            fallTime = 0
            currentPiece.y += 1
            if not(valid_space(currentPiece, grid)) and currentPiece.y > 0:
                currentPiece.y -= 1
                changePiece = True
        
        currentPiece.x = hand_position

        if not(valid_space(currentPiece, grid)):
            direction = get_direction(currentPiece.x, old_hand_position)

            if(direction == "right"):
                currentPiece.x -= 1
                print("Right")
            else:
                print("Left")
                currentPiece.x += 1

        # print(currentPiece.x, hand_position)

        old_hand_position = hand_position

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_LEFT:
                #     currentPiece.x  -= 1
                #     if not(valid_space(currentPiece, grid)):
                #         currentPiece.x += 1

                # if event.key == pygame.K_RIGHT:
                #     currentPiece.x  += 1
                #     if not(valid_space(currentPiece, grid)):
                #         currentPiece.x -= 1
                if event.key == pygame.K_DOWN:
                    currentPiece.y  += 1

                    if not(valid_space(currentPiece, grid)):
                        currentPiece.y -= 1

                if event.key == pygame.K_UP:
                    currentPiece.rotation  += 1

                    if not(valid_space(currentPiece, grid)):
                        currentPiece.rotation -= 1

        shapePos = convert_shape_format(currentPiece)
        
        for i in range(len(shapePos)):
            x, y = shapePos[i]
            if y > -1:
                grid[y][x] = currentPiece.color
        
        if changePiece:
            for pos in shapePos:
                p = (pos [0], pos[1])
                lockedPositions[p] = currentPiece.color
            
            currentPiece = nextPiece
            nextPiece = get_shape()
            changePiece = False
            score += clear_rows(grid, lockedPositions) * 10

        draw_window(win, grid, score)
        draw_next_shape(nextPiece, win)
        pygame.display.update()

        if check_lost(lockedPositions):
            draw_text_middle(win, "You Lost!", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False


def main_menu(win):
    """Displays the main menu of the game.
    
    Inputs:
    win -> surface object with the screen to display.
    """

    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, "Press any key to play!", 60, (255, 255, 255))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")
main_menu(win)  # start game