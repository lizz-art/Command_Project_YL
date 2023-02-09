import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5 import QtCore

SCREEN_SIZE = [600, 450]
lst = []


class Programm(QWidget):
    def __init__(self):
        super().__init__()
        self.delta = '0.005'
        self.toponym_lattitude, self.toponym_longitude = lst[0], lst[1]
        self.getImage()
        self.initUI()

    def getImage(self):
        try:
            map_params = {
                "ll": ",".join([self.toponym_longitude, self.toponym_lattitude]),
                "spn": ",".join([self.delta, self.delta]),
                "l": "map"
            }

            map_api_server = "http://static-maps.yandex.ru/1.x/"
            response = requests.get(map_api_server, params=map_params)

            if not response:
                print("Ошибка выполнения запроса:")
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)

            # Запишем полученное изображение в файл.
            self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)
        except Exception as e:
            print(e)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        k = 0.005
        k_height = float(self.delta)
        k_width = float(self.delta)
        if event.key() == QtCore.Qt.Key_PageDown:
            if float(self.delta) < k * 100:
                self.delta = str(float(self.delta) + k)
                self.getImage()
                self.image.setPixmap(QPixmap('map.png'))
                self.image.show()
        if event.key() == QtCore.Qt.Key_PageUp:
            if float(self.delta) > k:
                self.delta = str(float(self.delta) - k)
                self.getImage()
                self.image.setPixmap(QPixmap('map.png'))
                self.image.show()
        if event.key() == QtCore.Qt.Key_Down:
            self.toponym_lattitude = str(float(self.toponym_lattitude) - k_height)
            self.getImage()
            self.image.setPixmap(QPixmap('map.png'))
            self.image.show()
        if event.key() == QtCore.Qt.Key_Up:
            self.toponym_lattitude = str(float(self.toponym_lattitude) + k_height)
            self.getImage()
            self.image.setPixmap(QPixmap('map.png'))
            self.image.show()
        if event.key() == QtCore.Qt.Key_Left:
            self.toponym_longitude = str(float(self.toponym_longitude) - k_width)
            self.getImage()
            self.image.setPixmap(QPixmap('map.png'))
            self.image.show()
        if event.key() == QtCore.Qt.Key_Right:
            self.toponym_longitude = str(float(self.toponym_longitude) + k_width)
            self.getImage()
            self.image.setPixmap(QPixmap('map.png'))
            self.image.show()
        event.accept()


class Request(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.name_input = QLineEdit(self)
        self.name_input.resize(300, 25)
        self.name_input.move(100, 100)

        self.btn = QPushButton('Поиск', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(100, 150)
        self.btn.clicked.connect(self.run)

    def run(self):
        global lst
        lst += self.name_input.text().split(', ')
        self.hide()
        self.window = Programm()
        self.window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Request()
    ex.show()
    sys.exit(app.exec())
