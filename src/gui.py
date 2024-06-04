import sys

from PyQt5.QtWidgets import QWidget, QApplication, QComboBox, QPushButton
from PyQt5.QtGui import QPalette, QColor, QPainter, QBrush, QPixmap
from constants import title,bg_color_hex,app_lst,gesture_icon_path
from gesture import start_camera
class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def create_window(self):
        self.setWindowTitle(title)
        self.setGeometry(300, 300, 480, 480)
        self.setMinimumSize(480, 480)
        self.setMaximumSize(480, 480)

        bg_color = QPalette()
        bg_color.setColor(QPalette.Window, QColor(bg_color_hex))
        self.setPalette(bg_color)

    def create_dropdown(self):
        self.boxes = []
        boxes_pos = [
            (90, 30), (320, 30),
            (90, 110), (320, 110),
            (90, 190), (320, 190),
            (90, 270), (320, 270),
            (90, 350), (320, 350)
        ]

        for pos in boxes_pos:
            box = QComboBox(self)
            box.move(pos[0], pos[1])
            box.setFixedWidth(150)
            box.setFixedHeight(40)
            self.boxes.append(box)
            for app in app_lst:
                box.addItem(app)

    def create_button(self):
        self.confirm_btn = QPushButton('Confirm', self)
        self.confirm_btn.setFixedWidth(100)
        self.confirm_btn.setFixedHeight(40)
        self.confirm_btn.move(int(self.width() / 2) - 140, 430)
        self.confirm_btn.clicked.connect(self.confirm_click_handler)

        self.quit_btn = QPushButton('Exit', self)
        self.quit_btn.setFixedWidth(100)
        self.quit_btn.setFixedHeight(40)
        self.quit_btn.move(int(self.width() / 2) + 40, 430)
        self.quit_btn.clicked.connect(self.close)

    def confirm_click_handler(self):
        select_idx = [box.currentIndex() for box in self.boxes]
        start_camera(select_idx)
    def paintEvent(self,event):
        box_color = QPainter(self)
        box_color.setBrush(QBrush(QColor(255, 255, 250)))

        boxes_pos = [
            (20, 20), (250, 20),
            (20, 100), (250, 100),
            (20, 180), (250, 180),
            (20, 260), (250, 260),
            (20, 340), (250, 340)
        ]

        for i, pos in enumerate(boxes_pos):
            box_color.drawRect(pos[0], pos[1], 60, 60)
            if i < len(gesture_icon_path):
                pixmap = QPixmap(gesture_icon_path[i])
                box_color.drawPixmap(pos[0], pos[1], 60, 60, pixmap)

    def init(self):
        self.create_window()
        self.create_dropdown()
        self.create_button()

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())