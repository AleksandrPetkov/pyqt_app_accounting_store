from PyQt5 import QtCore, QtGui


def int_valid():
    rx = QtCore.QRegExp("[0-9]{100}")
    val = QtGui.QRegExpValidator(rx)
    return val
