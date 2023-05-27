import os

from camera import *
from piece import *
from themes import *
from window import *

# Window size and configuration variables.
s_width, s_height = 900, 900  # Width and height of the window.
user = windll.user32
screen_width, screen_height = (user.GetSystemMetrics(0),
                               user.GetSystemMetrics(1))
x_position, y_position = int(screen_width / 2), int((screen_height - s_height) / 2)  # x and y position of the window.
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x_position}, {y_position}"

# Global Variables
play_width = 300  # Total width of the box where pieces are falling
play_height = 600  # Total height of the box where pieces are falling
blockSize = 30  # Size of the block, this size makes the box have 10x20 blocks

top_left_x = (s_width - play_width) // 2  # Top left position of the "play" window
top_left_y = s_height - play_height # Top left position of the "play" window

guide_left_x = top_left_x
guide_left_y = top_left_y - 50

themes_list = ["Normal", "Metal"]
theme_counter = 0

win = pygame.display.set_mode((s_width, s_height)) # Surface object to display everything

pygame.font.init()
pygame.display.set_caption("Tetris") # Name of the game window


def main(win, theme):
    """Main execution of the game.

    Inputs:
    win  surface object with the screen to display.
    """

    # Variables needed to run the game
    run_game = True 
    locked_positions = {}
    grid = create_grid(locked_positions)
    guide_grid = create_guide_grid()
    change_piece = False
    current_piece = get_shape() 
    next_piece = get_shape()
    clock = pygame.time.Clock() 
    fall_time = 0
    fall_speed_real = 0.27
    fall_speed = fall_speed_real
    level_time = 0
    score = 0
    sounds = select_sounds(theme)
    colors = select_colors(theme)

    pygame.mixer.music.play(loops = -1)

    # Camera
    camera_captured, hands, hands_detector, hands_drawing = camera_settings()
    window_width = camera_captured.get(3)

    video_background = cv2.VideoCapture("media/Normal/Background.mp4")

    # Main loop that runs the game
    while run_game:
        # Video background
        ret, frame = video_background.read()
        if not ret:
            video_background.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        frame = cv2.resize(frame, (s_width, s_height))
        frame_surface = convert_frame(frame)
        win.blit(frame_surface, (0, 0))

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
        # Position of the hand to determine the position of the piece and
        # speed of the piece.
        hand_position, fall_speed_down = hand_controller(
                                         camera_captured,
                                         window_width, hands,
                                         hands_detector, hands_drawing,
                                         current_piece.x, position_values,
                                         fall_speed_real
        )

        fall_speed = fall_speed_down

        # Fixing the position of the hand in case it goes out of bounds
        if hand_position >= (max_position_value + 1):
            hand_position = max_position_value

        # Creating the grid again with the corresponding positions locked
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime() # Time for the pieces to fall
        level_time += clock.get_rawtime() # Time to increase the difficulty
        clock.tick()

        if(current_piece.x != hand_position):
            dif_pos = hand_position - current_piece.x
            if (dif_pos > 0):
                current_piece.x += 1
                if not(valid_space(current_piece, grid)):
                    current_piece.x -= 1

            else:
                current_piece.x -= 1
                if not(valid_space(current_piece, grid)):
                    current_piece.x += 1

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

        # Position of the piece in the previous frame
        old_hand_position = hand_position

        # Check game events
        for event in pygame.event.get():
            # Quit when you click on the X button
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                run_game = False
            
            # Keyboard inputs
            if event.type == pygame.KEYDOWN:
                # Make the piece rotate when pressing UP key
                if event.key == pygame.K_UP:
                    current_piece.rotation  += 1
                    pygame.mixer.Sound.play(sounds["rotate"])

                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        # Convert the piece from a list of dots and 0s to valid positions
        shape_pos = convert_shape_format(current_piece)
        
        # Color the grid with the current piece color
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # Color the guide grid with the current hand position
        for i in range(len(guide_grid)):
            for j in range(len(guide_grid[i])):
                if j == hand_position:
                    guide_grid[i][j] = (255, 255, 255)
                else:
                    guide_grid[i][j] = (0, 0, 0)

        # Lock the current piece in the grid and get the next one
        if change_piece:
            pygame.mixer.Sound.play(sounds["place"])

            for pos in shape_pos:
                p = (pos [0], pos[1])
                locked_positions[p] = current_piece.color
            
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            fall_speed = fall_speed_real  # Reset the speed.
            score += clear_rows(grid, locked_positions, sounds["clear_row"]) * 10

        # Draw the game window
        draw_window(top_left_x, top_left_y, play_height, play_width, blockSize,
                    win, grid, guide_grid, score)
        
        # Draw the next shape in the right of the screen
        draw_next_shape(next_piece, win, top_left_x, top_left_y, play_height,
                        play_width, blockSize)
        
        pygame.display.flip()  # Show the video background.
        pygame.display.update() # Update to show the changes made.

        # Check if the player lost the game.
        if check_lost(locked_positions):
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(sounds["lose"])

            draw_text_middle(win, "You Lost!", 80, (255, 255, 255), top_left_x,
                             top_left_y, play_height, play_width)
            pygame.display.update()
            pygame.time.delay(1500)
            run_game = False


def main_menu(win):
    """Displays the main menu of the game.
    
    Inputs:
    win -> surface object with the screen to display.
    """

    run = True
    global theme_counter
    theme = themes_list[theme_counter % 2]
    # Camera settings for the main menu.
    camera_captured_menu, window_name_menu = menu_camera_settings()

    while run:
        win.fill((0, 0, 0)) # Black background
        mouse_position = pygame.mouse.get_pos()

        # Displays the buttons.
        offset = 5
        start_button_coords = draw_start_button(win, offset)
        theme_button_coords = draw_theme_button(win, offset, theme)

        pygame.display.update()

        # Display the camera while in the main menu.
        menu_camera_window(camera_captured_menu, window_name_menu)
        
        # Events in main menu
        for event in pygame.event.get():
            # Checks if the player clicked the start button.
            if ((event.type == pygame.MOUSEBUTTONDOWN)
            and (mouse_position[0] >= start_button_coords["left"]
                 and mouse_position[0] <= start_button_coords["right"])
            and (mouse_position[1] >= start_button_coords["up"]
                 and mouse_position[1] <= start_button_coords["down"])):
                main(win, theme)  # Run the game.
                # Change the camera when the game is over.
                camera_captured_menu, window_name_menu = menu_camera_settings()

            # Checks if the player clicked the theme button.
            if ((event.type == pygame.MOUSEBUTTONDOWN)
            and (mouse_position[0] >= theme_button_coords["left"]
                 and mouse_position[0] <= theme_button_coords["right"])
            and (mouse_position[1] >= theme_button_coords["up"]
                 and mouse_position[1] <= theme_button_coords["down"])):
                theme_counter += 1

                if theme_counter >= len(themes_list):
                    theme_counter = 0
                
                theme = themes_list[theme_counter]

            # Quit when X is pressed on the game window
            if event.type == pygame.QUIT:
                run = False

    pygame.display.quit()


main_menu(win)  # Start
