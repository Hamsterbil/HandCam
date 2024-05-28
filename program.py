import cv2
import mediapipe as mp
import pyautogui
#Create a window showing camera feed
cap = cv2.VideoCapture(0)
print()

#Create a mediapipe hands object
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
hands.max_num_hands = 1
hands.min_detection_confidence = 1.0
hands.min_tracking_confidence = 1.0
hands.static_image_mode = False

pyautogui.FAILSAFE = False

scrolling, clicking, draw = False, False, False
show_cam = input("Show camera feed? (y/n): ").lower() == 'y'
in_tablet_mode = input("Are you in tablet mode? (y/n): ").lower() == 'y'
screen_width, screen_height = pyautogui.size()
screen_center = (screen_width // 2, screen_height // 2)
start_pos = []

def mouse_control(thumb, index_finger, ring_finger,):
    global scrolling, clicking, start_pos
    x1, y1, z1 = int(thumb.x * screen_width), int(thumb.y * screen_height), thumb.z
    x2, y2, z2 = int(index_finger.x * screen_width), int(index_finger.y * screen_height), index_finger.z
    x3, y3, z3 = int(ring_finger.x * screen_width), int(ring_finger.y * screen_height), ring_finger.z
    mouse = pyautogui.position()

    #Thumb + Index finger = Scroll
    if abs(x2 - x1) < 50 and abs(y2 - y1) < 50 and abs(z2 - z1) < 0.1:
        if not scrolling:
            start_pos = [x2, y2]
        scrolling = True
        pyautogui.scroll(start_pos[1] - y2, x=start_pos[0], y=start_pos[1], _pause=False)
    
    #Thumb + ring finger = Drag
    elif abs(x3 - x1) < 50 and abs(y3 - y1) < 50 and abs(z3 - z1) < 0.1:
        if not clicking:
            pyautogui.mouseDown(button='left', _pause=False)
        clicking = True

    else:
        if scrolling: scrolling = False
        if clicking:
            pyautogui.mouseUp(button='left', _pause=False)
            clicking = False

    #vector from center to index
    if not scrolling:
        vec = (x2 - screen_center[0], y2 - screen_center[1])
        dist_from_center = ((vec[0] ** 2) + (vec[1] ** 2)) ** 0.5
        edge_factor = 2.71828 ** (dist_from_center / 1000)
        pos = (screen_center[0] + vec[0] * edge_factor, screen_center[1] + vec[1] * edge_factor)

        #Very smooth mouse movement with easing and no delay and no jitter
        if abs(mouse[0] - pos[0]) > 7 or abs(mouse[1] - pos[1]) > 7:
            try:
                pyautogui.moveTo(pos[0], pos[1], _pause=False)
            except:
                print("Mouse out of screen bounds")
                pass

def draw_landmarks(image, landmarks):
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    for landmark in landmarks:
        x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
        cv2.circle(image, (x, y), 10, (0, 255, 0), -1)
    
    #Write "Scrolling" and "clicking" text. Green if active, red if inactive
    cv2.putText(image, "Scrolling", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if scrolling else (0, 0, 255), 2)
    cv2.putText(image, "clicking", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if clicking else (0, 0, 255), 2)

while True:
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a later selfie-view display. If in tablet mode flip upside down
    image = cv2.flip(image, 1) if not in_tablet_mode else cv2.flip(image, 0)
    # To improve performance, optionally mark the image as not writeable to pass by reference
    image.flags.writeable = False
    # Process the image
    results = hands.process(image)


    # if in_tablet_mode:
    #     ctypes.windll.user32.ShowCursor(True)

    image.flags.writeable = True
    #Hand detection and tracking
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb = hand_landmarks.landmark[4]
            index_finger = hand_landmarks.landmark[8]
            ring_finger = hand_landmarks.landmark[12]

            mouse_control(thumb, index_finger, ring_finger) 

            if draw and show_cam:
                draw_landmarks(image, [thumb, index_finger, ring_finger])

    if show_cam:
        cv2.imshow('Camera Feed', image)
        if cv2.waitKey(5) & 0xFF == 32:
            draw = not draw

        if cv2.waitKey(5) & 0xFF == 27:
            break