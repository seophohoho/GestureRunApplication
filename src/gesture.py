import subprocess
import time

import cv2
import mediapipe as mp
from constants import app_lst, max_recognition_time, camera_text


def launch_application(app_name):
    script = f'do shell script "open -a \\"{app_name}\\""'
    subprocess.Popen(["osascript", "-e", script])


def check_gesture(landmarks, idx):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    for tip in tips:
        if tip == 4:  # 엄지
            if landmarks[tip][1] < landmarks[tip - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:  # 다른 손가락
            if landmarks[tip][2] < landmarks[tip - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

    if fingers == [0, 0, 0, 0, 0]:
        launch_application(app_lst[idx[0]])
        return "rock"
    elif fingers == [1, 0, 0, 0, 0]:
        launch_application(app_lst[idx[1]])
        return "thumb"
    elif fingers == [0, 1, 0, 0, 0]:
        launch_application(app_lst[idx[2]])
        return "finger"
    elif fingers == [0, 0, 1, 0, 0]:
        launch_application(app_lst[idx[3]])
        return "fuck you"
    elif fingers == [0, 1, 1, 0, 0]:
        launch_application(app_lst[idx[4]])
        return "v"
    elif fingers == [1, 1, 0, 0, 0]:
        launch_application(app_lst[idx[5]])
        return "nike"
    elif fingers == [0, 1, 1, 1, 0]:
        launch_application(app_lst[idx[6]])
        return "three"
    elif fingers == [0, 1, 1, 1, 1]:
        launch_application(app_lst[idx[7]])
        return "four"
    elif fingers == [1, 1, 1, 1, 1]:
        launch_application(app_lst[idx[8]])
        return "five"
    elif fingers == [1, 0, 0, 0, 1]:
        launch_application(app_lst[idx[9]])
        return "promise"


def start_camera(select_idx):
    cam = cv2.VideoCapture(1)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8,
        max_num_hands=1
    )

    Draw = mp.solutions.drawing_utils
    gesture_buffer = []
    last_recognition_time = time.time()
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)  # 이미지 좌우 반전을 해줘야 함.
        cv2.putText(frame, camera_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # cv2의 이미지는 BGR이기 때문에, RGB로 변환해줘야 한다.

        results = hands.process(frameRGB)  # RGB 이미지 처리

        landmark_lst = []

        # 손이 이미지에 감지된 경우
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = frame.shape  # 프레임의 width, height
                    cx, cy = int(lm.x * w), int(lm.y * h)  # 랜드마크 x, y 좌표
                    landmark_lst.append([id, cx, cy])

                Draw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)  # 랜드마크 그려줌

            if landmark_lst and time.time() - last_recognition_time > max_recognition_time:
                gesture = check_gesture(landmark_lst, select_idx)
                # gesture_buffer.append(gesture)
                last_recognition_time = time.time()  # 시간 초기화
                cv2.putText(
                    frame,
                    gesture,
                    (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (255, 0, 0),
                    3
                )

                # # 최근 N 프레임의 제스처가 모두 동일하다면
                # if len(gesture_buffer) > max_gesture_buffer:
                #     gesture_buffer.pop(0)
                # if len(gesture_buffer) == max_gesture_buffer and gesture_buffer.count(
                #         gesture_buffer[0]) == max_gesture_buffer:

        cv2.imshow('Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
