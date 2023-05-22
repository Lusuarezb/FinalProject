import cv2
import mediapipe as mp
import numpy as np


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
                    hands_drawing, x_pos, x_boundaries, fall_speed):
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
    
    _, frame = camera_captured.read() # Capture the video frame by frame
    frame = cv2.flip(frame, 1)

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    fixed_x = x_pos
    fall_speed_down = fall_speed

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
                    # Hand gesture of an open hand.
                    if (y[8] > y[5] and y[12] > y[9] and y[16] > y[13] 
                        and y[20] > y[17]):
                        center_x = int((x[5] + x[17]) / 2)
                        fixed_x = int(
                            np.interp(
                                center_x, [0, window_width],
                                [x_boundaries[0], x_boundaries[1] + 1]
                            )
                        )
                        # print("Open")

                    # Hand gesture of a closed fist.
                    elif ((y[8] < y[5] and y[12] < y[9] and y[16] < y[13] 
                        and y[20] < y[17]) and (y[3] > y[2])):
                        fall_speed_down = 0.1
                        # print("Down")
                    else:  # No gesture detected.
                        # print("No gesture")
                        pass

            hands_drawing.draw_landmarks(frame, hand_side,
                                        hands_detector.HAND_CONNECTIONS)
    else: # No hand detected
        fixed_x = x_pos
        # print("No hand detected")

    cv2.imshow('Camera', frame) # Display the live camera

    return fixed_x, fall_speed_down


def camera_window():
    """Displays the camera in a separate window."""

    camera_captured, hands, hands_detector, hands_drawing = camera_settings()
    hand_controller(camera_captured, hands, hands_detector, hands_drawing)
