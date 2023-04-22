import sys

from PyQt5 import QtWidgets, QtGui
from app import AppShop


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setStyle('Breeze')
    app.setWindowIcon(QtGui.QIcon('ico.png'))
    window = AppShop()  # Создаём объект класса ExampleApp
    window.setWindowIcon(QtGui.QIcon('ico.png'))
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
