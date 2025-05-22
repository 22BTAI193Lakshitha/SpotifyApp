import cv2
import mediapipe as mp
import pyautogui
import time
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Virtual keyboard layout (you can expand this)
keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M']]

key_size = 60
start_x, start_y = 50, 100

cap = cv2.VideoCapture(0)
last_click_time = 0
click_delay = 1  # seconds

def draw_keyboard(img):
    for i, row in enumerate(keys):
        for j, key in enumerate(row):
            x = start_x + j * key_size
            y = start_y + i * key_size
            cv2.rectangle(img, (x, y), (x + key_size, y + key_size), (255, 0, 0), 2)
            cv2.putText(img, key, (x + 20, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

def get_key_at_pos(x, y):
    for i, row in enumerate(keys):
        for j, key in enumerate(row):
            key_x = start_x + j * key_size
            key_y = start_y + i * key_size
            if key_x < x < key_x + key_size and key_y < y < key_y + key_size:
                return key
    return None

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    draw_keyboard(img)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            index_tip = lm_list[8]
            thumb_tip = lm_list[4]

            cv2.circle(img, index_tip, 10, (0, 255, 0), cv2.FILLED)

            distance = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])
            if distance < 40:
                current_time = time.time()
                if current_time - last_click_time > click_delay:
                    key = get_key_at_pos(index_tip[0], index_tip[1])
                    if key:
                        pyautogui.typewrite(key.lower())
                        last_click_time = current_time

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
