from PyQt5 import QtSql, QtGui
from PyQt5.QtCore import Qt

from templates import main_win_template


class MainWinTableTemplate(main_win_template.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db_1 = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db_1.setDatabaseName("shop.db")

    def get_all_table(self, query_path, oper=None, val=None):
        self.db_1.open()
        query = QtSql.QSqlQuery(self.db_1)
        query.prepare(query_path)
        if oper == 2:
            query.bindValue(0, val)
            query.bindValue(1, val)
        if oper == 3:
            query.bindValue(0, val)
            query.bindValue(1, val)
            query.bindValue(2, val)

        query.exec_()
        table_model = QtSql.QSqlQueryModel()
        table_model.setQuery(query)
        table_model.setHeaderData(0, Qt.Horizontal, 'Артикул')
        table_model.setHeaderData(1, Qt.Horizontal, 'Наименование')
        table_model.setHeaderData(2, Qt.Horizontal, 'Партия')
        table_model.setHeaderData(3, Qt.Horizontal, 'Закуплено единиц')
        table_model.setHeaderData(4, Qt.Horizontal, 'Продажная цена')
        table_model.setHeaderData(5, Qt.Horizontal, 'Продажи')
        table_model.setHeaderData(6, Qt.Horizontal, 'Остаток')

        if oper == 1:
            table_model.setHeaderData(2, Qt.Horizontal, 'Сумма')
        if oper == 3:
            table_model.setHeaderData(5, Qt.Horizontal, 'Плановый доход')

        self.tableView.setModel(table_model)
        self.tableView.resizeColumnsToContents()
        self.db_1.close()

    def get_profit_table(self, data, oth_costs, tot_prof):
        table_model = QtGui.QStandardItemModel()
        table_model.setHorizontalHeaderLabels(['Партия', 'Фин. результат'])
        for i in data:
            table_model.appendRow([QtGui.QStandardItem(i[0]),
                                  QtGui.QStandardItem(str(i[1]))])
        table_model.appendRow([QtGui.QStandardItem('Всего прочих затрат'),
                              QtGui.QStandardItem(str(oth_costs))])
        table_model.appendRow([QtGui.QStandardItem('Общая прибыль'),
                              QtGui.QStandardItem(str(tot_prof))])
        self.tableView.setModel(table_model)
        self.tableView.resizeColumnsToContents()
        self.db_1.close()
