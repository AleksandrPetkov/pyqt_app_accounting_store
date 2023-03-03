from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

import data_base

from add_dialoges import AddBatchOthercostsDialog, AddGoodDialog, EditGoodDialog,\
    SearchDialog, EditSellBatch
from data_base import DB
from templates.main_win_table import MainWinTableTemplate


class AppShop(QtWidgets.QMainWindow, MainWinTableTemplate, DB):
    def __init__(self):
        super().__init__()

        self.add_batch.triggered.connect(self.add_batch_func)
        self.add_other_costs.triggered.connect(self.add_other_costs_func)
        self.add_sell.triggered.connect(self.add_sell_func)
        self.add_good.triggered.connect(self.add_good_func)

        self.show_nomenclature.triggered.connect(self.show_nomenclature_table)
        self.show_othercosts.triggered.connect(self.show_other_costs_table)
        self.balance_by_bacth.triggered.connect(self.show_balance_bybatch_table)
        self.all_balance.triggered.connect(self.show_all_balance_table)
        self.fin_result.triggered.connect(self.show_profit_table)

        self.show_batches.triggered.connect(self.show_batches_table)
        self.pl_fin_res_batch.triggered.connect(self.show_pl_fin_res_bybatch_table)

        self.change_good.triggered.connect(self.edit_good)
        self.change_sell.triggered.connect(self.edit_sell)
        self.change_batch.triggered.connect(self.edit_batch)
        self.chanhe_oth_cost.triggered.connect(self.edit_oth_costs)

        self.delete_good.triggered.connect(self.delete_good_func)
        self.delete_oth_cost.triggered.connect(self.delete_oth_cost_func)
        self.delete_sell.triggered.connect(self.delete_sell_func)

    def get_message(self, oper):
        if oper == 1:
            return QMessageBox.information(self, 'Внимание', 'Отмена операции!')
        if oper == 2:
            return QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
        if oper == 3:
            return QMessageBox.information(self, 'Отлично', 'Операция успешна!')

    def add_batch_func(self):
        title = 'Добавление партии'
        line_1 = 'Наименование:'
        line_2 = 'Сумма:'
        input_dialog = AddBatchOthercostsDialog(title, line_1, line_2)
        rez = input_dialog.exec()
        if not rez:
            self.get_message(1)
            return
        name = input_dialog.line_add_name.text()
        money = input_dialog.line_add_money.text()
        if not name or not money:
            self.get_message(2)
            self.add_batch_func()
            return
        if rez:
            query = data_base.QUERY_PATHES['add_batch']
            data = (name, money)
            self.insert_data(query, data)
            self.get_message(3)
            return

    def add_other_costs_func(self):
        title = 'Добавление других затрат'
        line_1 = 'Наименование:'
        line_2 = 'Сумма:'
        input_dialog = AddBatchOthercostsDialog(title, line_1, line_2)
        rez = input_dialog.exec()
        if not rez:
            self.get_message(1)
            return
        name = input_dialog.line_add_name.text()
        money = input_dialog.line_add_money.text()
        if not name or not money:
            self.get_message(2)
            self.add_other_costs_func()
            return
        if rez:
            query = data_base.QUERY_PATHES['add_oth_cost']
            data = (name, money)
            self.insert_data(query, data)
            self.get_message(3)
            return

    def add_sell_func(self):
        title = 'Добавление продажи'
        line_1 = 'Артикул:'
        line_2 = 'Количество:'
        input_dialog = AddBatchOthercostsDialog(title, line_1, line_2)
        rez = input_dialog.exec()
        if not rez:
            self.get_message(1)
            return
        name = input_dialog.line_add_name.text()
        money = input_dialog.line_add_money.text()
        if not name or not money:
            self.get_message(2)
            self.add_sell_func()
            return
        if rez:
            query = data_base.QUERY_PATHES['add_sell']
            data = (money, name)
            self.insert_data(query, data)
            self.get_message(3)
            return

    def add_good_func(self):
        input_dialog = AddGoodDialog()
        rez = input_dialog.exec()
        if not rez:
            self.get_message(1)
            return
        name = input_dialog.line_add_name.text()
        batch = input_dialog.line_add_batch.currentText()
        number = input_dialog.line_add_number.text()
        price = input_dialog.line_add_price.text()
        if not name or not number or not price:
            self.get_message(2)
            self.add_good_func()
            return
        if rez:
            query = data_base.QUERY_PATHES['add_good']
            data = (name, batch, number, price)
            self.insert_data(query, data)
            self.get_message(3)
            return

    def show_nomenclature_table(self):
        query_path = data_base.QUERY_PATHES['nomenclature']
        self.get_all_table(query_path)

    def show_all_balance_table(self):
        query_path = data_base.QUERY_PATHES['general_balance']
        self.get_all_table(query_path)

    def show_other_costs_table(self):
        query_path = data_base.QUERY_PATHES['other_costs']
        self.get_all_table(query_path, 1)

    def show_batches_table(self):
        query_path = data_base.QUERY_PATHES['batches']
        self.get_all_table(query_path, 1)

    def show_balance_bybatch_table(self):
        title = 'партии'
        path = data_base.QUERY_PATHES['get_batch_names']
        func = self.get_data(path)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if rez:
            val = input_dialog.line_add_batch.currentText()
            query_path = data_base.QUERY_PATHES['batch_balance']
            self.get_all_table(query_path, 2, val)

    def show_pl_fin_res_bybatch_table(self):
        title = 'партии'
        path = data_base.QUERY_PATHES['get_batch_names']
        func = self.get_data(path)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if rez:
            val = input_dialog.line_add_batch.currentText()
            query_path = data_base.QUERY_PATHES['plan_fin_res']
            self.get_all_table(query_path, 3, val)

    def show_profit_table(self):
        data = self.get_batch_profit()
        other_costs = self.get_sum_oth_costs()
        tot_profit = self.get_total_profit()
        self.get_profit_table(data, other_costs, tot_profit)

    def edit_good(self):
        title = 'товара'
        path_id = data_base.QUERY_PATHES['get_good_id']
        func = self.get_data(path_id)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if rez:
            art = input_dialog.line_add_batch.currentText()
            edit_dialog = EditGoodDialog(art)
            rez = edit_dialog.exec()
            if not rez:
                self.get_message(1)
                return
            if rez:
                path = data_base.QUERY_PATHES['update_good']
                art = edit_dialog.line_add_id.text()
                desc = edit_dialog.line_add_name.text()
                buy = edit_dialog.line_add_number.text()
                price = edit_dialog.line_add_price.text()
                sell = edit_dialog.line_add_sell.text()
                data = (desc, buy, price, sell, art)
                self.delete_update_data(path, data)
                self.get_message(3)
                return
        if not rez:
            self.get_message(1)
            return

    def edit_sell(self):
        title = 'продажи'
        oper = 1
        path_id = data_base.QUERY_PATHES['get_good_id']
        func = self.get_data(path_id)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if rez:
            path_data = data_base.QUERY_PATHES['get_current_sell']
            art = input_dialog.line_add_batch.currentText()
            func_2 = self.get_current_data_by_id(path_data, art)
            edit_dialog = EditSellBatch(title, func_2, oper)
            rez = edit_dialog.exec()
            if not rez:
                self.get_message(1)
                return
            if rez:
                path = data_base.QUERY_PATHES['update_sell']
                art = edit_dialog.line_add_id.text()
                sell = edit_dialog.line_add_money.text()
                data = (sell, art)
                self.delete_update_data(path, data)
                self.get_message(3)
                return
        if not rez:
            self.get_message(1)
            return

    def edit_batch(self):
        title = 'партии'
        oper = 1
        path_id = data_base.QUERY_PATHES['get_batch_id']
        func = self.get_data(path_id)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if rez:
            path_data = data_base.QUERY_PATHES['get_current_batch']
            art = input_dialog.line_add_batch.currentText()
            func_2 = self.get_current_data_by_id(path_data, art)
            edit_dialog = EditSellBatch(title, func_2, oper)
            rez = edit_dialog.exec()
            if not rez:
                self.get_message(1)
                return
            if rez:
                path = data_base.QUERY_PATHES['update_batch']
                art = edit_dialog.line_add_id.text()
                costs = edit_dialog.line_add_money.text()
                data = (costs, art)
                self.delete_update_data(path, data)
                self.get_message(3)
                return
        if not rez:
            self.get_message(1)
            return

    def edit_oth_costs(self):
        title = 'прочих затрат'
        path_id = data_base.QUERY_PATHES['get_oth_costs_id']
        func = self.get_data(path_id)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if rez:
            path_current = data_base.QUERY_PATHES['get_current_oth_costs']
            art = input_dialog.line_add_batch.currentText()
            func_2 = self.get_current_data_by_id(path_current, art)
            edit_dialog = EditSellBatch(title, func_2)
            rez = edit_dialog.exec()
            if not rez:
                self.get_message(1)
                return
            if rez:
                path = data_base.QUERY_PATHES['update_oth_cost']
                art = edit_dialog.line_add_id.text()
                desc = edit_dialog.line_add_name.text()
                costs = edit_dialog.line_add_money.text()
                data = (desc, costs, art)
                self.delete_update_data(path, data)
                self.get_message(3)
                return
        if not rez:
            self.get_message(1)
            return

    def delete_good_func(self):
        title = 'товара'
        path_id = data_base.QUERY_PATHES['get_good_id']
        func = self.get_data(path_id)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if rez:
            path = data_base.QUERY_PATHES['delete_good']
            art = input_dialog.line_add_batch.currentText()
            data = (art,)
            self.delete_update_data(path, data)
            self.get_message(3)
            return
        if not rez:
            self.get_message(1)
            return

    def delete_oth_cost_func(self):
        title = 'прочих затрат'
        path_id = data_base.QUERY_PATHES['get_oth_costs_id']
        func = self.get_data(path_id)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if rez:
            path = data_base.QUERY_PATHES['delete_oth_cost']
            art = input_dialog.line_add_batch.currentText()
            data = (art,)
            self.delete_update_data(path, data)
            self.get_message(3)
            return
        if not rez:
            self.get_message(1)
            return

    def delete_sell_func(self):
        title = 'продажи'
        path_id = data_base.QUERY_PATHES['get_good_id']
        func = self.get_data(path_id)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if rez:
            path = data_base.QUERY_PATHES['delete_sell']
            art = input_dialog.line_add_batch.currentText()
            data = (0, art)
            self.delete_update_data(path, data)
            self.get_message(3)
            return
        if not rez:
            self.get_message(1)
            return
