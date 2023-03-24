# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout.addWidget(self.tableView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_3 = QtWidgets.QMenu(self.menu)
        self.menu_3.setObjectName("menu_3")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_5 = QtWidgets.QMenu(self.menubar)
        self.menu_5.setObjectName("menu_5")
        self.menu_6 = QtWidgets.QMenu(self.menubar)
        self.menu_6.setObjectName("menu_6")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.show_nomenclature = QtWidgets.QAction(MainWindow)
        self.show_nomenclature.setObjectName("show_nomenclature")
        self.show_sells = QtWidgets.QAction(MainWindow)
        self.show_sells.setObjectName("show_sells")
        self.show_othercosts = QtWidgets.QAction(MainWindow)
        self.show_othercosts.setObjectName("show_othercosts")
        self.add_batch = QtWidgets.QAction(MainWindow)
        self.add_batch.setObjectName("add_batch")
        self.add_good = QtWidgets.QAction(MainWindow)
        self.add_good.setObjectName("add_good")
        self.add_other_costs = QtWidgets.QAction(MainWindow)
        self.add_other_costs.setObjectName("add_other_costs")
        self.add_sell = QtWidgets.QAction(MainWindow)
        self.add_sell.setObjectName("add_sell")
        self.balance_by_bacth = QtWidgets.QAction(MainWindow)
        self.balance_by_bacth.setObjectName("balance_by_bacth")
        self.all_balance = QtWidgets.QAction(MainWindow)
        self.all_balance.setObjectName("all_balance")
        self.fin_res_by_batch = QtWidgets.QAction(MainWindow)
        self.fin_res_by_batch.setObjectName("fin_res_by_batch")
        self.all_fin_res = QtWidgets.QAction(MainWindow)
        self.all_fin_res.setObjectName("all_fin_res")
        self.change_good = QtWidgets.QAction(MainWindow)
        self.change_good.setObjectName("change_good")
        self.delete_good = QtWidgets.QAction(MainWindow)
        self.delete_good.setObjectName("delete_good")
        self.chanhe_oth_cost = QtWidgets.QAction(MainWindow)
        self.chanhe_oth_cost.setObjectName("chanhe_oth_cost")
        self.change_batch = QtWidgets.QAction(MainWindow)
        self.change_batch.setObjectName("change_batch")
        self.change_sell = QtWidgets.QAction(MainWindow)
        self.change_sell.setObjectName("change_sell")
        self.delete_oth_cost = QtWidgets.QAction(MainWindow)
        self.delete_oth_cost.setObjectName("delete_oth_cost")
        self.delete_sell = QtWidgets.QAction(MainWindow)
        self.delete_sell.setObjectName("delete_sell")
        self.show_batches = QtWidgets.QAction(MainWindow)
        self.show_batches.setObjectName("show_batches")
        self.pl_fin_res_batch = QtWidgets.QAction(MainWindow)
        self.pl_fin_res_batch.setObjectName("pl_fin_res_batch")
        self.fin_result = QtWidgets.QAction(MainWindow)
        self.fin_result.setObjectName("fin_result")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.show_batches_ta = QtWidgets.QAction(MainWindow)
        self.show_batches_ta.setObjectName("show_batches_ta")
        self.menu_3.addAction(self.balance_by_bacth)
        self.menu_3.addAction(self.all_balance)
        self.menu.addAction(self.show_othercosts)
        self.menu.addAction(self.menu_3.menuAction())
        self.menu.addAction(self.fin_result)
        self.menu.addAction(self.action_3)
        self.menu.addAction(self.show_batches_ta)
        self.menu_2.addAction(self.add_batch)
        self.menu_2.addAction(self.add_good)
        self.menu_2.addAction(self.add_other_costs)
        self.menu_5.addAction(self.change_good)
        self.menu_6.addAction(self.delete_good)
        self.menu_6.addAction(self.delete_oth_cost)
        self.menu_6.addAction(self.delete_sell)
        self.menu_6.addAction(self.action_4)
        self.menu_4.addAction(self.action)
        self.menu_4.addAction(self.action_2)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_5.menuAction())
        self.menubar.addAction(self.menu_6.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "Показать"))
        self.menu_3.setTitle(_translate("MainWindow", "Товар"))
        self.menu_2.setTitle(_translate("MainWindow", "Добавить"))
        self.menu_5.setTitle(_translate("MainWindow", "Редактировать"))
        self.menu_6.setTitle(_translate("MainWindow", "Удалить"))
        self.menu_4.setTitle(_translate("MainWindow", "Продажа"))
        self.show_nomenclature.setText(_translate("MainWindow", "Номенклатура"))
        self.show_sells.setText(_translate("MainWindow", "Продажы"))
        self.show_othercosts.setText(_translate("MainWindow", "Прочие затраты"))
        self.add_batch.setText(_translate("MainWindow", "Партия"))
        self.add_good.setText(_translate("MainWindow", "Товар"))
        self.add_other_costs.setText(_translate("MainWindow", "Прочие затраты"))
        self.add_sell.setText(_translate("MainWindow", "Продажа"))
        self.balance_by_bacth.setText(_translate("MainWindow", "По партии"))
        self.all_balance.setText(_translate("MainWindow", "Общий"))
        self.fin_res_by_batch.setText(_translate("MainWindow", "По партии"))
        self.all_fin_res.setText(_translate("MainWindow", "Общий"))
        self.change_good.setText(_translate("MainWindow", "Товар"))
        self.delete_good.setText(_translate("MainWindow", "Товар"))
        self.chanhe_oth_cost.setText(_translate("MainWindow", "Прочие затраты"))
        self.change_batch.setText(_translate("MainWindow", "Партия"))
        self.change_sell.setText(_translate("MainWindow", "Продажа"))
        self.delete_oth_cost.setText(_translate("MainWindow", "Прочие затраты"))
        self.delete_sell.setText(_translate("MainWindow", "Отправку"))
        self.show_batches.setText(_translate("MainWindow", "Партии"))
        self.pl_fin_res_batch.setText(_translate("MainWindow", "Фин. результат (по партии)"))
        self.fin_result.setText(_translate("MainWindow", "Фин результат"))
        self.action.setText(_translate("MainWindow", "Добавить отправку"))
        self.action_2.setText(_translate("MainWindow", "Подтвердить продажу"))
        self.action_3.setText(_translate("MainWindow", "Отправки"))
        self.action_4.setText(_translate("MainWindow", "Нулевые остатки"))
        self.show_batches_ta.setText(_translate("MainWindow", "Партии"))
