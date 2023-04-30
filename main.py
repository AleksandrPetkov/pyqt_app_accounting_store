import sys

from PyQt5 import QtWidgets, QtGui
from app import AppShop
import os

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setWindowIcon(QtGui.QIcon('ico.png'))
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'media', 'ico.png')))
    app.setStyle('Breeze')
    window = AppShop()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
# pyinstaller main.spec
