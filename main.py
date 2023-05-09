# TODO:
# Comentarios en Ingles - Luis
# Snake Case - Luis 
# 80 Caracteres horizontal - David
# Separar en scripts - David
# Espaciado entre operadores y valores - David

from camera import *
from piece import *
from window import *

# Global Variables
s_width = 1600     # Width of window
s_height = 900     # Height of window
play_width = 300   # Total width of the box where pieces are falling
play_height = 600  # Total height of the box where pieces are falling
blockSize = 30     # Size of the block, this size makes the box have 10x20 blocks
top_left_x = (s_width - play_width) // 2  # Top left position of the "play" window
top_left_y = s_height - play_height       # Top left position of the "play" window

def main(win):
    """Main execution of the game.

    Inputs:
    win  surface object with the screen to display.
    """
    # Variables needed to run the game
    run = True 
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    current_piece = get_shape() 
    next_piece = get_shape()
    clock = pygame.time.Clock() 
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0
    old_hand_position = 5 # This is needed to keep the piece in the position it was before the hand disappears or moves

    # Camera
    camera_captured, hands, hands_detector, hands_drawing = camera_settings()
    window_width = camera_captured.get(3)

    # Main loop that runs the game
    while run:
        # List that contains the valid positions of the current piece
        current_piece_position_array = (
            shape_valid_positions[shapes.index(current_piece.shape)]
        )
        # List that contains the valid position of the current piece with the current rotation
        position_values = (
            current_piece_position_array[current_piece.rotation 
                                         % len(current_piece_position_array)]
        )
        # Max value of the previous list, needed to fix the hand positioning
        max_position_value = max(
            current_piece_position_array[current_piece.rotation 
                                         % len(current_piece_position_array)]
        )
        # Position of the hand, this determines the position of the piece
        hand_position = hand_controller(camera_captured, window_width, hands,
                                        hands_detector, hands_drawing,
                                        current_piece.x, position_values)

        # Fixing the position of the hand in case it goes out of bounds
        if hand_position >= (max_position_value + 1):
            hand_position = max_position_value

        # Creating the grid again with the corresponding positions locked
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime() # Time for the pieces to fall
        level_time += clock.get_rawtime() # Time to increase the difficulty
        clock.tick()

        current_piece.x = hand_position # Moving the piece where the hand is

        # Increasing level difficulty every 5 seconds
        if level_time / 1000 > 5:
            level_time = 0

            if fall_speed > 0.12:
                fall_speed -= -0.01

        # Piece falls one step every second
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        
        # Verifiying if the piece is in a valid space
        if not(valid_space(current_piece, grid)):
            direction = get_direction(current_piece.x, old_hand_position)

            if(direction == "right"):
                current_piece.x -= 1
                print("Right")
            else:
                print("Left")
                current_piece.x += 1

        # Position of the piece in the previous frame
        old_hand_position = hand_position

        # Check game events
        for event in pygame.event.get():
            # Quit when you click on the X button
            if event.type == pygame.QUIT:
                run = False
            
            # Keyboard inputs
            if event.type == pygame.KEYDOWN:
                # Make the piece fall faster when pressing DOWN key
                if event.key == pygame.K_DOWN:
                    current_piece.y  += 1

                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1

                # Make the piece rotate when pressing UP key
                if event.key == pygame.K_UP:
                    current_piece.rotation  += 1

                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        # Convert the piece from a list of dots and 0s to valid positions
        shapePos = convert_shape_format(current_piece)
        
        # Color the grid with the current piece color
        for i in range(len(shapePos)):
            x, y = shapePos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        
        # Lock the current piece in the grid and get the next one
        if change_piece:
            for pos in shapePos:
                p = (pos [0], pos[1])
                locked_positions[p] = current_piece.color
            
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        # Draw the game window
        draw_window(top_left_x, top_left_y, play_height, play_width, blockSize, win,
                    grid, score)
        
        # Draw the next shape in the right of the screen
        draw_next_shape(next_piece, win, top_left_x, top_left_y, play_height, play_width,
                        blockSize)
        
        pygame.display.update() # Update to show the changes made

        # Check if the player lost the game
        if check_lost(locked_positions):
            draw_text_middle(win, "You Lost!", 80, (255, 255, 255), top_left_x,
                             top_left_y, play_height, play_width)
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
        win.fill((0, 0, 0)) # Black background

        draw_text_middle(win, "Press any key to play!", 60, (255, 255, 255),
                         top_left_x, top_left_y, play_height, play_width)
        pygame.display.update()
        
        # Events in main menu
        for event in pygame.event.get():
            # Quit when X is pressed on the game window
            if event.type == pygame.QUIT:
                run = False
            # Run the game when any key is pressed
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()



win = pygame.display.set_mode((s_width, s_height)) # Surface object to display everything
pygame.font.init() 
pygame.display.set_caption("Tetris") # Name of the game window
main_menu(win)  #Start
