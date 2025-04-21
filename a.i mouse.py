
import cv2
import math
import pyautogui
import mediapipe as mp
import numpy as np

# Webcam capture
cap = cv2.VideoCapture(0)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Get screen size
screen_w, screen_h = pyautogui.size()

# Frame reduction margin (to avoid edge detection issues)
frameR = 100

while True:
    success, img = cap.read()
    if not success:
        break

    # Flip the image for a mirror view
    img = cv2.flip(img, 1)
    h, w, c = img.shape

    # Convert to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            # Draw hand landmarks
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get index finger tip (id 8) and thumb tip (id 4)
            x1, y1 = lm_list[4][1], lm_list[4][2]  # Thumb
            x2, y2 = lm_list[8][1], lm_list[8][2]  # Index

            # Move the mouse to index finger tip location
            screen_x = np.interp(x2, (frameR, w - frameR), (0, screen_w))
            screen_y = np.interp(y2, (frameR, h - frameR), (0, screen_h))
            pyautogui.moveTo(screen_x, screen_y)

            # Check distance between thumb and index fingers
            distance = math.hypot(x2 - x1, y2 - y1)
            if distance < 30:
                pyautogui.click()
                cv2.circle(img, ((x1 + x2)//2, (y1 + y2)//2), 10, (0, 255, 0), cv2.FILLED)

    # Show webcam feed
    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
