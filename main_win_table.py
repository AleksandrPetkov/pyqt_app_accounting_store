from PyQt5 import QtSql, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel

from data_base import DB
from queres import DELETE_QUERES

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

        if del_val:
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
        if oper == 'batch':
            t_model.setHeaderData(2, Qt.Horizontal, 'Сумма')
        self.tableView.setModel(t_model)
        self.tableView.resizeColumnsToContents()

    def get_noneditable_table(self, query_path, header_list, data=None, oper=None):
        self.db_1.open()
        query = QtSql.QSqlQuery(self.db_1)
        query.prepare(query_path)
        if oper == 'show_size':
            query.bindValue(0, data)
        if oper == 'show_profit_by_order':
            past_1, now_1, past_2, now_2 = data
            query.bindValue(0, past_1)
            query.bindValue(1, now_1)
            query.bindValue(2, past_1)
            query.bindValue(3, now_2)
        if oper == 'good_by_batch':
            query.bindValue(0, data)
            query.bindValue(1, data)
        query.exec_()
        table_model = QtSql.QSqlQueryModel()
        table_model.setQuery(query)
        for num, header in zip(range(len(header_list)), header_list):
            table_model.setHeaderData(num, Qt.Horizontal, header)
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
