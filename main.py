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
s_width = 1600
s_height = 900
playWidth = 300  # meaning 300 // 10 = 30 width per block
playHeight = 600  # meaning 600 // 20 = 30 height per block
blockSize = 30

topLeftX = (s_width - playWidth) // 2
topLeftY = s_height - playHeight

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

        draw_window(topLeftX, topLeftY, playHeight, playWidth, blockSize, win,
                    grid, score)
        draw_next_shape(nextPiece, win, topLeftX, topLeftY, playHeight, playWidth,
                        blockSize)
        pygame.display.update()

        if check_lost(lockedPositions):
            draw_text_middle(win, "You Lost!", 80, (255, 255, 255), topLeftX,
                             topLeftY, playHeight, playWidth)
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
pygame.font.init()
pygame.display.set_caption("Tetris")
main_menu(win)  # start game
