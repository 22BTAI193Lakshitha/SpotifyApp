# utils.py
import cv2

import time

def cooldown_passed(last_action, cooldown):
    return time.time() - last_action > cooldown

def overlay_text(img, text, position):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

