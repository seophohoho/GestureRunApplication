import sys
import subprocess
import mediapipe as mp
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton
from PyQt5.QtGui import QPainter, QColor, QBrush, QPalette, QPixmap

application_list = [
    'Terminal',
    'Calculator',
    'Notes',
    'Calendar',
    'Google Chrome',
    'Obsidian',
    'Todoist',
    'KakaoTalk',
    'Safari',
    'Postman',
    'Mail',
]


def launch_application(app_name):
    script = f"""
    tell application "{app_name}"
        if not (exists window 1) then reopen
        activate
    end tell
    """
    subprocess.Popen(["osascript", "-e", script])


def startCamera(selected_indices):
    print(selected_indices)
    # Mediapipe 손 모델 초기화
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8,
        max_num_hands=1)

    Draw = mp.solutions.drawing_utils

    # 웹캠 시작
    cap = cv2.VideoCapture(1)  # 기본 웹캠 사용

    def classify_gesture(landmarks):
        # 손가락 끝 인덱스
        tips = [4, 8, 12, 16, 20]

        # 손가락이 펴져 있는지 여부 확인
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
            launch_application(application_list[selected_indices[0]])
            return "rock"
        elif fingers == [1, 0, 0, 0, 0]:
            launch_application(application_list[selected_indices[1]])
            return "thumb"
        elif fingers == [0, 1, 0, 0, 0]:
            launch_application(application_list[selected_indices[2]])
            return "finger"
        elif fingers == [0, 0, 1, 0, 0]:
            launch_application(application_list[selected_indices[3]])
            return "fuck you"
        elif fingers == [0, 0, 0, 0, 1]:
            launch_application(application_list[selected_indices[4]])
            return "v"
        elif fingers == [1, 1, 0, 0, 0]:
            launch_application(application_list[selected_indices[5]])
            return "nike"
        elif fingers == [1, 1, 1, 0, 0]:
            launch_application(application_list[selected_indices[6]])
            return "three"
        elif fingers == [0, 1, 1, 1, 1]:
            launch_application(application_list[selected_indices[7]])
            return "four"
        elif fingers == [1, 1, 1, 1, 1]:
            launch_application(application_list[selected_indices[8]])
            return "five"
        elif fingers == [1, 0, 0, 0, 1]:
            launch_application(application_list[selected_indices[9]])
            return "promise"

    # 최근 N 프레임의 제스처를 저장할 버퍼
    N = 10
    gesture_buffer = []

    while True:
        # 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            break

        # 이미지를 좌우 반전
        frame = cv2.flip(frame, 1)

        # BGR 이미지를 RGB 이미지로 변환
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # RGB 이미지 처리
        results = hands.process(frameRGB)

        # 랜드마크 리스트 초기화
        landmarkList = []

        # 손이 이미지에 감지된 경우
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    # 이미지의 높이와 너비 가져오기
                    h, w, c = frame.shape

                    # 랜드마크의 x, y 좌표 계산
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarkList.append([id, cx, cy])

                # 랜드마크 그리기
                Draw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

            # 제스처 분류
            if landmarkList:
                gesture = classify_gesture(landmarkList)
                gesture_buffer.append(gesture)

                # 최근 N 프레임의 제스처가 모두 동일하면 출력
                if len(gesture_buffer) > N:
                    gesture_buffer.pop(0)
                if len(gesture_buffer) == N and gesture_buffer.count(gesture_buffer[0]) == N:
                    cv2.putText(frame, gesture_buffer[0], (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

        # 결과 이미지 출력
        cv2.imshow('Gesture Recognition', frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 자원 해제
    cap.release()
    cv2.destroyAllWindows()


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 700, 400)  # 윈도우 위치와 크기 설정
        self.setMinimumSize(480, 480)  # 최소 크기 설정
        self.setMaximumSize(480, 480)  # 최대 크기 설정
        self.setWindowTitle('GestureRunApplication')

        # QPalette로 배경 색상 설정 (Hex 코드 사용)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#aaaaaa"))  # Background color
        self.setPalette(palette)

        # QComboBox 추가
        self.combo_boxes = []
        combo_positions = [(90, 30), (320, 30),
                           (90, 110), (320, 110),
                           (90, 190), (320, 190),
                           (90, 270), (320, 270),
                           (90, 350), (320, 350)]  # 추가된 두 개의 QComboBox 위치

        for pos in combo_positions:
            combo = QComboBox(self)
            for app in application_list:
                combo.addItem(app)
            combo.move(pos[0], pos[1])  # QComboBox 위치 설정
            combo.setFixedWidth(150)
            combo.setFixedHeight(40)
            self.combo_boxes.append(combo)

        # 버튼 추가
        self.confirm_button = QPushButton('결정하기', self)
        self.confirm_button.setFixedWidth(100)
        self.confirm_button.setFixedHeight(40)
        self.confirm_button.move(int(self.width() / 2) - 140, 430)  # 결정하기 버튼 위치 설정
        self.confirm_button.clicked.connect(self.on_confirm_click)  # 결정하기 버튼 클릭 시 함수 실행

        self.quit_button = QPushButton('종료하기', self)
        self.quit_button.setFixedWidth(100)
        self.quit_button.setFixedHeight(40)
        self.quit_button.move(int(self.width() / 2) + 40, 430)  # 종료하기 버튼 위치 설정
        self.quit_button.clicked.connect(self.close)  # 종료하기 버튼 클릭 시 윈도우 닫기

        self.show()

    def on_confirm_click(self):
        selected_indices = [combo.currentIndex() for combo in self.combo_boxes]
        startCamera(selected_indices)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(255, 255, 250)))  # 정사각형 색상 설정 (흰색)

        # 10개의 서로 다른 정사각형 그리기
        rect_positions = [(20, 20), (250, 20),
                          (20, 100), (250, 100),
                          (20, 180), (250, 180),
                          (20, 260), (250, 260),
                          (20, 340), (250, 340)]  # 추가된 두 개의 정사각형 위치

        image_files = ['../public/0.png', '../public/1.png',
                       '../public/2.png', '../public/3.png',
                       '../public/4.png', '../public/5.png',
                       '../public/6.png', '../public/7.png',
                       '../public/8.png', '../public/9.png']  # 이미지 파일 경로

        for i, pos in enumerate(rect_positions):
            painter.drawRect(pos[0], pos[1], 60, 60)  # 정사각형 그리기

            if i < len(image_files):
                pixmap = QPixmap(image_files[i])
                painter.drawPixmap(pos[0], pos[1], 60, 60, pixmap)  # 이미지 그리기


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
