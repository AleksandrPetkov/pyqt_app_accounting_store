from PyQt5 import QtSql, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel

from data_base import DB
from queres import DELETE_QUERES, QUERY_PATHES

from templates import main_win_template


class CTM(QSqlTableModel):
    def __init__(self, column=None):
        super().__init__()
        self.column = column

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if index.column() in self.column:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsEnabled


class MainWinTableTemplate(main_win_template.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db_1 = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db_1.setDatabaseName("shop.db")

    def get_editable_table(self, column, table, oper, del_val=None):
        name = 'Cумма'

        del_query = DELETE_QUERES[del_val]
        DB().ins_del_upd_data(del_query, (name,))

        t_model = CTM(column)
        t_model.setTable(table)
        t_model.select()
        t_model.setEditStrategy(CTM.OnRowChange)

        if oper == 'other_costs':
            row = t_model.rowCount()
            res = 0
            for i in range(0, row):
                res += int(t_model.data(t_model.index(i, 2)))
            t_model.insertRow(row)
            t_model.setData(t_model.index(row, 1), name)
            t_model.setData(t_model.index(row, 2), res)

        t_model.setHeaderData(0, Qt.Horizontal, 'Артикул')
        t_model.setHeaderData(1, Qt.Horizontal, 'Наименование')
        if oper == 'other_costs':
            t_model.setHeaderData(2, Qt.Horizontal, 'Сумма')
        self.tableView.setModel(t_model)
        self.tableView.resizeColumnsToContents()

    def get_all_table(self, query_path, oper=None, val=None):
        self.db_1.open()
        query = QtSql.QSqlQuery(self.db_1)
        query.prepare(query_path)
        if oper == 'good_by_batch':
            query.bindValue(0, val)
            query.bindValue(1, val)

        query.exec_()
        table_model = QtSql.QSqlQueryModel()
        table_model.setQuery(query)
        table_model.setHeaderData(0, Qt.Horizontal, 'Артикул')
        table_model.setHeaderData(1, Qt.Horizontal, 'Наименование')
        table_model.setHeaderData(2, Qt.Horizontal, 'Цена закупки')
        table_model.setHeaderData(3, Qt.Horizontal, 'Партия')
        table_model.setHeaderData(4, Qt.Horizontal, 'Закуплено единиц')
        table_model.setHeaderData(5, Qt.Horizontal, 'Продажная цена')
        table_model.setHeaderData(6, Qt.Horizontal, 'Продажи')
        table_model.setHeaderData(7, Qt.Horizontal, 'Остаток')

        if oper == 'good_by_batch':
            table_model.setHeaderData(8, Qt.Horizontal, 'Плановый доход')
        if oper == 'pre_sell':
            table_model.setHeaderData(0, Qt.Horizontal, '4 цифры накладной')
            table_model.setHeaderData(1, Qt.Horizontal, 'Артикул товара')
            table_model.setHeaderData(2, Qt.Horizontal, 'Количество проданного')
            table_model.setHeaderData(3, Qt.Horizontal, 'Скидка')
            table_model.setHeaderData(4, Qt.Horizontal, 'Место продажи')

        self.tableView.setModel(table_model)
        self.tableView.resizeColumnsToContents()
        self.db_1.close()

    def get_profit_table(self):
        batch = DB().get_batch_profit()
        costs = DB().get_sum_oth_costs()
        income = DB().get_total_profit()
        total_profit = int(income[0][1]) - int(batch[-1][1]) - int(costs[0][1])
        table_model = QtGui.QStandardItemModel()
        table_model.setHorizontalHeaderLabels(['Наименование', 'Сумма'])
        for i in batch:
            table_model.appendRow([QtGui.QStandardItem(i[0]),
                                  QtGui.QStandardItem(str(i[1]))])
        for i in costs:
            table_model.appendRow([QtGui.QStandardItem(i[0]),
                                  QtGui.QStandardItem(str(i[1]))])
        for i in income:
            table_model.appendRow([QtGui.QStandardItem(i[0]),
                                  QtGui.QStandardItem(str(i[1]))])
        table_model.appendRow([QtGui.QStandardItem('Фин. результат'),
                               QtGui.QStandardItem(str(total_profit))])
        self.tableView.setModel(table_model)
        self.tableView.resizeColumnsToContents()
        self.db_1.close()

