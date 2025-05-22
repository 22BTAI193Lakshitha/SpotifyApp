import cv2
import mediapipe as mp
import pyautogui
import time
from gestures import get_gesture
from utils import cooldown_passed, overlay_text

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
last_action_time = time.time()
cooldown = 2  # seconds

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            gesture = get_gesture(lm_list)

            if gesture and cooldown_passed(last_action_time, cooldown):
                overlay_text(img, gesture, (50, 50))
                last_action_time = time.time()

                # Map gesture to Spotify controls
                if gesture == "Play":
                    pyautogui.press("playpause")
                elif gesture == "Pause":
                    pyautogui.press("playpause")
                elif gesture == "Next":
                    pyautogui.hotkey("ctrl", "right")
                elif gesture == "Previous":
                    pyautogui.hotkey("ctrl", "left")
                elif gesture == "Volume Up":
                    pyautogui.press("volumeup")
                elif gesture == "Volume Down":
                    pyautogui.press("volumedown")

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Spotify Gesture Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
