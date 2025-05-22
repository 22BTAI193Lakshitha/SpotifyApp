def get_finger_states(lm_list):
    tips = [8, 12, 16, 20]  # Index to Pinky tips
    states = []

    for tip in tips:
        state = 1 if lm_list[tip][1] < lm_list[tip - 2][1] else 0
        states.append(state)
    return states

def get_gesture(lm_list):
    fingers = get_finger_states(lm_list)

    if sum(fingers) == 0:
        return "Pause"
    elif sum(fingers) == 5:
        return "Play"
    elif fingers == [1, 1, 0, 0]:
        return "Volume Up"
    elif fingers == [0, 0, 1, 1]:
        return "Volume Down"
    elif fingers == [0, 0, 0, 1]:
        return "Next"
    elif fingers == [1, 1, 1, 1]:
        return "Previous"
    return None
