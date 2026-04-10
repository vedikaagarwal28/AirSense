# AirSense Final with Auto App Detection + Smooth Scroll + Screenshot Gesture + Text Selection
import sys, threading, time, math
from collections import deque
import os, subprocess
import datetime

import cv2, mediapipe as mp, pyautogui

# ----------------------------- CONFIG -----------------------------
SMOOTHING = 4.0
PINCH_THRESHOLD = 0.04
PINCH_FRAMES = 3
MIN_CLICK_INTERVAL = 0.4
SCROLL_SENSITIVITY = 50
FPS_TARGET = 30

SCROLL_MICRO_STEPS = 8
SCROLL_STEP_DELAY = 0.005
SCROLL_CLAMP_PIX = 600

SCREENSHOT_COOLDOWN = 1.8

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

shared = {
    "gesture": "idle",
    "status_text": "Starting...",
    "running": True,
    "selecting": False
}

prev_x = prev_y = 0.0


# ----------------------------- FOLDERS -----------------------------
USER = os.environ["USERNAME"]
DESKTOP = rf"C:\Users\{USER}\Desktop"


# ----------------------------- SCROLL -----------------------------
def smooth_scroll_pixels(p):
    if p == 0: return
    p = max(min(p, SCROLL_CLAMP_PIX), -SCROLL_CLAMP_PIX)
    step = p / SCROLL_MICRO_STEPS
    for _ in range(SCROLL_MICRO_STEPS):
        pyautogui.scroll(int(step))
        time.sleep(SCROLL_STEP_DELAY)


# ----------------------------- CV THREAD -----------------------------
def cv_worker():
    global prev_x, prev_y
    last_screenshot_time = 0

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not found.")
        shared["running"] = False
        return

    screen_w, screen_h = pyautogui.size()

    pinch_count = 0
    last_click_time = 0
    avg_y_history = deque(maxlen=6)
    pinch_start = 0

    while shared["running"]:
        ok, frame = cap.read()
        if not ok: continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)

        gesture = "idle"
        now = time.time()

        if res.multi_hand_landmarks:

            # --- detect right hand ---
            right_hand_index = None
            for i, handedness in enumerate(res.multi_handedness):
                if handedness.classification[0].label == "Right":
                    right_hand_index = i
                    break

            if right_hand_index is None:
                shared["gesture"] = "idle"
                shared["status_text"] = "No Right Hand"
                continue

            lm = res.multi_hand_landmarks[right_hand_index].landmark

            # ------------ LANDMARKS ------------
            ix, iy = lm[8].x, lm[8].y
            tx, ty = lm[4].x, lm[4].y

            # ------------ MOVEMENT ------------
            target_x = ix * screen_w
            target_y = iy * screen_h

            curr_x = prev_x + (target_x - prev_x) / SMOOTHING
            curr_y = prev_y + (target_y - prev_y) / SMOOTHING
            prev_x, prev_y = curr_x, curr_y

            pyautogui.moveTo(curr_x, curr_y)

            # ------------------------------------------------------
            #  PINCH CLICK + PINCH HOLD TEXT SELECTION
            # ------------------------------------------------------
            pinch_dist = math.hypot(ix - tx, iy - ty)
            PINCH_HOLD_TIME = 0.25

            if pinch_dist < PINCH_THRESHOLD:
                if pinch_count == 0:
                    pinch_start = now
                pinch_count += 1
            else:
                # if was selecting, stop on release
                if shared["selecting"]:
                    pyautogui.mouseUp()
                    shared["selecting"] = False
                    gesture = "select_end"

                pinch_count = 0

            # -- long pinch = start selection --
            if pinch_count > 0 and not shared["selecting"]:
                if now - pinch_start > PINCH_HOLD_TIME:
                    pyautogui.mouseDown()
                    shared["selecting"] = True
                    gesture = "select_start"

            # -- short pinch = click --
            if pinch_count >= PINCH_FRAMES:
                if not shared["selecting"]:
                    if now - pinch_start < PINCH_HOLD_TIME:
                        if now - last_click_time > MIN_CLICK_INTERVAL:
                            pyautogui.click()
                            last_click_time = now
                            gesture = "click"

            # ------------------------------------------------------
            # SCREENSHOT
            # ------------------------------------------------------
            my = lm[12].y
            py_f = lm[20].y

            thumb_up = ty < lm[3].y
            index_up = iy < lm[6].y
            pinky_up = py_f < lm[18].y

            middle_down = my > lm[9].y
            ring_down   = lm[16].y > lm[14].y

            if thumb_up and index_up and pinky_up and middle_down and ring_down:
                if now - last_screenshot_time > SCREENSHOT_COOLDOWN:
                    filename = f"{DESKTOP}\\screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"
                    ss = pyautogui.screenshot()
                    ss.save(filename)
                    print("Screenshot saved:", filename)
                    last_screenshot_time = now
                    gesture = "screenshot"

            # ------------------------------------------------------
            # SCROLL (Two Finger Up)
            # ------------------------------------------------------
            middle_up = my < lm[10].y
            if index_up and middle_up:
                avg_y_history.append((iy + my) / 2 * screen_h)
                if len(avg_y_history) >= 2:
                    dy = avg_y_history[-1] - avg_y_history[0]
                    scroll_pixels = -dy * (SCROLL_SENSITIVITY / 40.0)
                    if abs(scroll_pixels) > 0.1:
                        smooth_scroll_pixels(scroll_pixels)
            else:
                avg_y_history.clear()

        shared["gesture"] = gesture
        shared["status_text"] = f"Gesture: {gesture}"

    cap.release()


# ----------------------------- MAIN -----------------------------
def main():
    t1 = threading.Thread(target=cv_worker, daemon=True)
    t1.start()

    while shared["running"]:
        time.sleep(0.1)


if __name__ == "__main__":
    main()