import pygame
import random
import tetrominos as tt

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# Variables Globales
s_width = 1600
s_height = 900
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS
shapes = [tt.S, tt.Z, tt.I, tt.O, tt.J, tt.L, tt.T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape

class Piece(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_pos={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid

def convert_shape_format(shape):
    # positions = []
    # formato = shape.shape[shape.rotation % len(shape.shape)]

    # for i, line in enumerate(formato):
    #     row = list(line)
    #     for j, column in enumerate(row):
    #         if column == "0":
    #             positions.append((shape.x + j, shape.y + i))
    
    # for i, pos in enumerate(positions):
    #     positions[i]= (pos[0] -2, pos[1] - 4)
    pass

def valid_space(shape, grid):
    pass

def check_lost(positions):
    pass

def get_shape(shapes):
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):  
    pass
   
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy+i*block_size), (sx+play_width, sy+i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j*block_size, sy), (sx + j*block_size, sy+play_height))


def clear_rows(grid, locked):
    pass

def draw_next_shape(shape, surface):
    pass

def draw_window(surface, grid):
    surface.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render("Tetris", 1, (255,255,255))

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)
    pygame.display.update()

def main(win):
    run = True
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    current_piece = get_shape(shapes)
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x  -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x  += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y  += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.rotation  += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        draw_window(win, grid)

def main_menu(win): 
    main(win)
    pass


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")
main_menu(win)  # start game