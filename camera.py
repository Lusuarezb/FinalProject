from ctypes import windll
import cv2
import mediapipe as mp
import numpy as np


def menu_camera_settings():
    """Sets the initial camera settings for the camera window displayed
    alongside the main menu.
    
    Returns:
    the camera object and the window name.
    """

    camera_captured = cv2.VideoCapture(0) # Set camera
    window_name = "Camera"
    cv2.namedWindow(window_name)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_AUTOSIZE,
                          cv2.WINDOW_AUTOSIZE)

    return camera_captured, window_name


def menu_camera_window(camera_captured, window_name):
    """Displays the camera in a separate window while in the main menu."""

    ret, frame = camera_captured.read()  # Read a frame from the camera
    frame = cv2.flip(frame, 1)

    # Check if the frame is empty
    if ret:
        user = windll.user32
        screen_width, screen_height = (
            user.GetSystemMetrics(0), user.GetSystemMetrics(1)
        )
        window_width, window_height = cv2.getWindowImageRect('Camera')[2:]
        cv2.moveWindow(window_name,
                       (int(screen_width / 2) - int(window_width * 1.05)),
                        int((screen_height - window_height) / 2))
        
        cv2.imshow(window_name, frame)  # Display the frame in the window


def camera_settings():
    """Sets the basic settings for the camera.
    
    Returns:
    the camera object, hand detector object and the hand connections.
    """

    camera_captured = cv2.VideoCapture(0) # Set camera

    # Getting hands controllers
    hands_detector = mp.solutions.hands
    hands = hands_detector.Hands(max_num_hands = 1)
    hands_drawing = mp.solutions.drawing_utils

    return camera_captured, hands, hands_detector, hands_drawing


def hand_controller(camera_captured, window_width, hands, hands_detector,
                    hands_drawing, x_pos, x_boundaries, fall_speed_real,
                    is_rotating, has_rotated):
    """Controls the hand's movement and returns the corresponding movement.
    
    Inputs:
    camera_captured -> camera object.
    window_width -> width of the game's window.
    hands -> hands detected.
    hands_detector -> hand detector object.
    hands_drawing -> hand connections to be displayed.
    x_pos -> current position of the current piece.
    x_boundaries -> piece positions.

    Returns:
    x position for the piece to move.
    """
    
    _, frame = camera_captured.read()  # Capture the video frame by frame
    frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    fixed_x = x_pos
    fall_speed_down = fall_speed_real

    window_name = "Camera"
    cv2.namedWindow(window_name)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_AUTOSIZE,
                          cv2.WINDOW_AUTOSIZE)

    user = windll.user32
    screen_width, screen_height = (
        user.GetSystemMetrics(0), user.GetSystemMetrics(1)
    )
    window_width, window_height = cv2.getWindowImageRect('Camera')[2:]

    if results.multi_hand_landmarks: # Hand detected
        for hand_side in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_side.landmark):
                h, w, c = frame.shape
                if id == 0:
                    x = []
                    y = []
                x.append(int((lm.x) * w))
                y.append(int((1 - lm.y) * h))

                if len(x) > 20: # When all coordinates are set
                    # Hand gesture of an open hand -> move piece.
                    if ((y[8] > y[5] and y[12] > y[9] and y[16] > y[13] 
                        and y[20] > y[17])
                        and (x[4] >= x[3] > x[5] > x[9] or x[4] < x[5] < x[9])):
                        center_x = int((x[5] + x[17]) / 2)
                        fixed_x = int(
                            np.interp(
                                center_x, [0, window_width],
                                [x_boundaries[0], x_boundaries[1] + 1]
                            )
                        )
                        is_rotating = False
                        has_rotated = False
                        fall_speed_down = fall_speed_real

                    # Hand gesture of an open hand with thumb inside -> rotate.
                    elif ((y[8] > y[5] and y[12] > y[9] and y[16] > y[13] 
                        and y[20] > y[17])
                        and ((x[4] < x[3] and x[5] > x[9])
                             or (x[4] > x[3] and x[5] < x[9]))):
                        is_rotating = True

                    # Hand gesture of a closed fist -> drop.
                    elif ((y[8] < y[5] and y[12] < y[9] and y[16] < y[13] 
                        and y[20] < y[17]) and (y[3] > y[2])):
                        # rotate_time = 0
                        is_rotating = False
                        has_rotated = False
                        fall_speed_down = 0.01

                    else:  # No gesture detected.
                        pass

            hands_drawing.draw_landmarks(frame, hand_side,
                                        hands_detector.HAND_CONNECTIONS)
    else: # No hand detected
        fixed_x = x_pos

    cv2.moveWindow(window_name,
                   (int(screen_width / 2) - int(window_width * 1.05)),
                   int((screen_height - window_height) / 2))
    cv2.imshow(window_name, frame) # Display the live camera

    return fixed_x, fall_speed_down, is_rotating, has_rotated
