import cv2
import mediapipe as mp
import numpy as np

def camera_settings():
    camera_captured = cv2.VideoCapture(0) # Set camera

    # Getting hands controllers
    hands_detector = mp.solutions.hands
    hands = hands_detector.Hands(max_num_hands = 1)
    hands_drawing = mp.solutions.drawing_utils

    return camera_captured, hands, hands_detector, hands_drawing

def hand_controller(camera_captured, window_width, hands, hands_detector, hands_drawing, x_pos):
    _, frame = camera_captured.read() # Capture the video frame by frame
    frame = cv2.flip(frame, 1)

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    results = hands.process(image)
    

    fixed_x = 5

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
                    if (y[8] > y[5] and y[12] > y[9] and y[16] > y[13] 
                        and y[20] > y[17]):
                        center_x = int((x[5] + x[17])/2)
                        center_y = int(camera_captured.get(4)) - int((y[0] + y[9])/2)
                        cv2.circle(frame, center=(center_x, center_y),
                                radius = 5, color = (0, 0, 255),
                                thickness = -1)
                        #print("Movement")
                        fixed_x = int(np.interp(center_x, [0, window_width], [0, 10]))
                    elif ((not (y[8] > y[5] and y[12] > y[9] and y[16] > y[13] 
                        and y[20] > y[17])) and ((x[0] > x[3] > x[4])
                                                or (x[0] < x[3] < x[4]))):
                        #print("Go down")
                        pass
                    else:
                        #print("Do nothing")
                        pass

            hands_drawing.draw_landmarks(frame, hand_side,
                                        hands_detector.HAND_CONNECTIONS)
    else: # No hand detected
        fixed_x = x_pos

    # cv2.namedWindow("Cámara")
    cv2.imshow('Camera', frame) # Display the live camera

    return fixed_x 
    
def camera_window():
    camera_captured, hands, hands_detector, hands_drawing = camera_settings()
    hand_controller(camera_captured, hands, hands_detector, hands_drawing)