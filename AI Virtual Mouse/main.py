import cv2
import mediapipe as mp
import pyautogui
import random
import util
import time
import math
from pynput.mouse import Button, Controller
import ctypes  # For volume control on Windows

mouse = Controller()
screen_width, screen_height = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

volume = ctypes.windll.user32
VOLUME_STEP = 2

prev_mouse = (0, 0)
last_action_time = 0
gesture_cooldown = 0.6


def debounce_action():
    global last_action_time
    current = time.time()
    if current - last_action_time >= gesture_cooldown:
        last_action_time = current
        return True
    return False


def move_mouse(index_tip, prev_pos, smoothing=2):
    x = int(index_tip.x * screen_width)
    y = int(index_tip.y * screen_height / 2)
    smooth_x = prev_pos[0] + (x - prev_pos[0]) // smoothing
    smooth_y = prev_pos[1] + (y - prev_pos[1]) // smoothing
    pyautogui.moveTo(smooth_x, smooth_y, _pause=False)
    return smooth_x, smooth_y


def get_pinch_distance(landmark_list):
    x1, y1 = landmark_list[4]  # Thumb tip
    x2, y2 = landmark_list[8]  # Index tip
    return math.hypot(x2 - x1, y2 - y1)


def angle_between_points(p1, p2, p3):
    a = math.sqrt((p2[0]-p3[0])**2 + (p2[1]-p3[1])**2)
    b = math.sqrt((p1[0]-p3[0])**2 + (p1[1]-p3[1])**2)
    c = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    if b * c == 0:
        return 0
    angle = math.acos((b**2 + c**2 - a**2) / (2 * b * c))
    return math.degrees(angle)


def is_volume_up(landmark_list):
    angle = angle_between_points(landmark_list[4], landmark_list[5], landmark_list[8])
    dist = get_pinch_distance(landmark_list)
    return dist > 0.07 and 30 <= angle <= 45


def is_volume_down(landmark_list):
    dist = get_pinch_distance(landmark_list)
    return dist < 0.035


def is_finger_extended(landmark_list, finger_tip, pip_joint):
    return landmark_list[finger_tip][1] < landmark_list[pip_joint][1]


def all_fingers_closed(landmark_list):
    fingers = [(8, 6), (12, 10), (16, 14), (20, 18)]
    return all(landmark_list[tip][1] > landmark_list[pip][1] for tip, pip in fingers)


def detect_gesture(frame, landmark_list, processed, prev_pos):
    gesture_detected = False

    if len(landmark_list) >= 21:
        index_tip = processed.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        index_up = is_finger_extended(landmark_list, 8, 6)
        middle_up = is_finger_extended(landmark_list, 12, 10)
        ring_down = not is_finger_extended(landmark_list, 16, 14)
        pinky_down = not is_finger_extended(landmark_list, 20, 18)
        thumb_down = not is_finger_extended(landmark_list, 4, 3)

        # Screenshot with closed fist
        if not index_up and not middle_up and ring_down and pinky_down and thumb_down:
            if debounce_action():
                im1 = pyautogui.screenshot()
                label = random.randint(1, 1000)
                im1.save(f'my_screenshot_{label}.png')
                cv2.putText(frame, "📸 Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                gesture_detected = True

        # Left Click: Flick gesture with index finger
        elif index_up and not middle_up and ring_down and pinky_down and thumb_down:
            if debounce_action():
                mouse.press(Button.left)
                time.sleep(0.05)
                mouse.release(Button.left)
                cv2.putText(frame, "👆 Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                gesture_detected = True

        # Right Click: Flick gesture with middle finger
        elif not index_up and middle_up and ring_down and pinky_down and thumb_down:
            if debounce_action():
                mouse.press(Button.right)
                time.sleep(0.05)
                mouse.release(Button.right)
                cv2.putText(frame, "👉 Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                gesture_detected = True

        # Double Click: Index and middle fingers up, rest down
        elif index_up and middle_up and ring_down and pinky_down and thumb_down:
            if debounce_action():
                pyautogui.doubleClick()
                cv2.putText(frame, "✌️ Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                gesture_detected = True

        elif is_volume_up(landmark_list):
            if debounce_action():
                for _ in range(VOLUME_STEP):
                    volume.keybd_event(0xAF, 0, 0, 0)
                cv2.putText(frame, "🔊 Volume Up", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 200, 0), 2)
                gesture_detected = True

        elif is_volume_down(landmark_list):
            if debounce_action():
                for _ in range(VOLUME_STEP):
                    volume.keybd_event(0xAE, 0, 0, 0)
                cv2.putText(frame, "🔉 Volume Down", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 100, 0), 2)
                gesture_detected = True

        if not gesture_detected:
            prev_pos = move_mouse(index_tip, prev_pos)

    return prev_pos


def main():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    prev_pos = (0, 0)
    p_time = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(rgb_frame)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            prev_pos = detect_gesture(frame, landmark_list, processed, prev_pos)

            c_time = time.time()
            fps = int(1 / (c_time - p_time)) if c_time != p_time else 0
            p_time = c_time
            cv2.putText(frame, f'FPS: {fps}', (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 100), 2)

            cv2.imshow('AI Virtual Mouse', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
