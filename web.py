import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

SCREEN_SIZE = [600, 450]
lst = []


class Programm(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        # map_request = "http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=0.002,0.002&l=map"
        toponym_to_find = " ".join(sys.argv[1:])

        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        toponym_lattitude, toponym_longitude = lst[0], lst[1]
        delta = '0.005'
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        # response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            # print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

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
        print(lst)
        self.hide()
        self.window = Programm()
        self.window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Request()
    ex.show()
    sys.exit(app.exec())
