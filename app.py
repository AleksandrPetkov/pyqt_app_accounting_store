import sqlite3

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from add_dialoges import AddBatchOthercostsSellDialog, AddGoodDialog, EditGoodDialog,\
    SearchDialog, AddSellDialog
from data_base import DB
from templates.main_win_table import MainWinTableTemplate
from queres import QUERY_PATHES, ADD_QUERES, UPDATE_QUERES, DELETE_QUERES


class AppShop(QtWidgets.QMainWindow, MainWinTableTemplate, DB):
    def __init__(self):
        super().__init__()

        self.add_batch.triggered.connect(self.add_batch_func)
        self.add_other_costs.triggered.connect(self.add_other_costs_func)
        # self.add_sell.triggered.connect(self.add_pre_sell_func)
        self.add_good.triggered.connect(self.add_good_func)
        self.action.triggered.connect(self.add_pre_sell_func)
        self.action_2.triggered.connect(self.submit_sell_func)

        # self.show_nomenclature.triggered.connect(self.show_nomenclature_table)
        self.show_othercosts.triggered.connect(self.show_other_costs_table)
        self.balance_by_bacth.triggered.connect(self.show_goods_bybatch_table)
        self.all_balance.triggered.connect(self.show_goods_table)
        self.fin_result.triggered.connect(self.show_profit_table)
        self.action_3.triggered.connect(self.show_pre_sell_table)

        # self.show_batches.triggered.connect(self.show_batches_table)
        # self.pl_fin_res_batch.triggered.connect(self.show_pl_fin_res_bybatch_table)

        self.change_good.triggered.connect(self.edit_good)
        # self.change_sell.triggered.connect(self.edit_sell)
        # self.change_batch.triggered.connect(self.edit_batch)
        # self.chanhe_oth_cost.triggered.connect(self.edit_oth_costs)

        self.delete_good.triggered.connect(self.delete_good_func)
        self.delete_oth_cost.triggered.connect(self.delete_oth_cost_func)
        self.action_4.triggered.connect(self.delete_0_balance_func)
        self.delete_sell.triggered.connect(self.delete_pre_sell_func)

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
        oper = 'add_batch'
        # line_2 = 'Сумма:'
        input_dialog = AddBatchOthercostsSellDialog(title, line_1, None, oper) #, line_2
        rez = input_dialog.exec()
        if not rez:
            self.get_message(1)
            return
        name = input_dialog.line_add_name.text()
        # money = input_dialog.line_add_money.text()
        if not name :#or not money
            self.get_message(2)
            self.add_batch_func()
            return
        if rez:
            query = ADD_QUERES['add_batch']
            data = (name,) #, money
            self.ins_del_upd_data(query, data)
            self.get_message(3)
            return

    def add_other_costs_func(self):
        title = 'Добавление других затрат'
        line_1 = 'Наименование:'
        line_2 = 'Сумма:'
        oper = 'add_oth_costs'
        input_dialog = AddBatchOthercostsSellDialog(title, line_1, line_2, oper)
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
            query = ADD_QUERES['add_oth_cost']
            data = (name, money)
            self.ins_del_upd_data(query, data)
            self.get_message(3)
            return

    def add_pre_sell_func(self):
        input_dialog = AddSellDialog()
        rez = input_dialog.exec()
        if not rez:
            self.get_message(1)
            return
        num = input_dialog.line_add_num.text()
        art = input_dialog.line_add_art.text()
        sell_p = self.get_current_data_by_id(QUERY_PATHES['get_current_good'], art)[5]
        val = input_dialog.line_add_val.text()
        discount = input_dialog.line_discount.text()
        place_id = input_dialog.line_sell_place.currentText()
        if not num or not art or not val:
            self.get_message(2)
            self.add_pre_sell_func()
            return
        if rez:
            func = self.get_data(QUERY_PATHES['get_note_num'])
            if int(num) not in func:
                query_1 = ADD_QUERES['add_deliv_note']
                data_1 = (num, place_id)
                self.ins_del_upd_data(query_1, data_1)
            query = ADD_QUERES['add_pre_sell']
            data = (num, art, sell_p, val, discount)
            self.ins_del_upd_data(query, data)
            self.get_message(3)
            return

    def add_good_func(self):
        input_dialog = AddGoodDialog()
        rez = input_dialog.exec()
        if not rez:
            self.get_message(1)
            return
        name = input_dialog.line_add_name.text()
        buy_price = input_dialog.line_add_buy_price.text()
        quere_b_id = QUERY_PATHES['get_batch_id_by_name']
        batch = self.get_id(quere_b_id, input_dialog.line_add_batch.currentText())
        number = input_dialog.line_add_number.text()
        price = input_dialog.line_add_price.text()
        if not name or not number or not price:
            self.get_message(2)
            self.add_good_func()
            return
        if rez:
            query = ADD_QUERES['add_good']
            data = (name, buy_price, batch, number, price)
            self.ins_del_upd_data(query, data)
            query_2 = QUERY_PATHES['get_buy_price']
            last_ins_id = self.get_data_2(query_2)
            costs = int(buy_price) * int(number)
            data_list = (costs, last_ins_id)
            query_3 = ADD_QUERES['add_batch_cost']
            self.ins_del_upd_data(query_3, data_list)
            self.get_message(3)
            return

    def submit_sell_func(self):
        title = 'отправки'
        path_id = QUERY_PATHES['get_note_num']
        func = self.get_data(path_id)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if not rez:
            self.get_message(1)
            return
        if rez:
            quere = QUERY_PATHES['get_pre_sell']
            sell_id = input_dialog.line_add_batch.currentText()
            pre_sells = self.get_pre_sell(quere, sell_id)
            for elem in pre_sells:
                good_id, sell_price, sell, discount = elem
                quere_1 = ADD_QUERES['add_sell']
                self.ins_del_upd_data(quere_1, (sell, good_id))
                income = int(sell_price) * int(sell) - int(discount)
                quere_2 = ADD_QUERES['add_income']
                self.ins_del_upd_data(quere_2, (sell_id, good_id, income))
            quere_3 = ADD_QUERES['add_place_stat']
            place_n = self.get_id(QUERY_PATHES['get_place_names_note'], sell_id)
            self.ins_del_upd_data(quere_3, (1, place_n))
            quere_4 = DELETE_QUERES['delete_pre_sell']
            self.ins_del_upd_data(quere_4, (sell_id,))
            quere_5 = DELETE_QUERES['delete_note']
            self.ins_del_upd_data(quere_5, (sell_id,))
            self.get_message(3)
            return

    def show_other_costs_table(self):
        # query_path = data_base.QUERY_PATHES['other_costs']
        # self.get_all_table(query_path, 1)
        self.get_editable_table([1, 2], 'other_costs', 'delete_oth_sum')

    def show_goods_table(self):
        query_path = QUERY_PATHES['general_balance']
        self.get_all_table(query_path)

    def show_goods_bybatch_table(self):
        title = 'партии'
        path = QUERY_PATHES['get_batch_names']
        func = self.get_data(path)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if rez:
            quere_b_id = QUERY_PATHES['get_batch_id_by_name']
            val = self.get_id(quere_b_id, input_dialog.line_add_batch.currentText())
            query_path = QUERY_PATHES['batch_balance']
            self.get_all_table(query_path, 'good_by_batch', val)

    def show_batches_table(self):
        self.get_editable_table([1], 'batch', 'delete_batch_sum')

    def show_profit_table(self):
        name = 'Cумма'
        del_query = DELETE_QUERES['delete_oth_sum']
        del_query_2 = DELETE_QUERES['delete_batch_sum']
        self.ins_del_upd_data(del_query, (name,))
        self.ins_del_upd_data(del_query_2, (name,))
        self.get_profit_table()

    def show_pre_sell_table(self):
        query_path = QUERY_PATHES['pre_sell']
        self.get_all_table(query_path, 'pre_sell')

    def edit_good(self):
        title = 'товара'
        path_id = QUERY_PATHES['get_good_id']
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
                query_b = QUERY_PATHES['get_current_good']
                old_b_price, batch_n, old_b_num = self.get_current_data_by_id(query_b, art)[2:5]
                path = UPDATE_QUERES['update_good']
                art = edit_dialog.line_add_id.text()
                desc = edit_dialog.line_add_name.text()
                b_price = edit_dialog.line_add_buy_price.text()
                buy = edit_dialog.line_add_number.text()
                price = edit_dialog.line_add_price.text()
                data = (desc, b_price, buy, price, art)
                self.ins_del_upd_data(path, data)
                diff = int(b_price)*int(buy) - int(old_b_price)*int(old_b_num)
                quere_b_id = QUERY_PATHES['get_batch_id_by_name']
                batch_id = self.get_id(quere_b_id, batch_n)
                data_list = [diff, batch_id]
                query_3 = ADD_QUERES['add_batch_cost']
                self.ins_del_upd_data(query_3, data_list)
                self.get_message(3)
                return
        if not rez:
            self.get_message(1)
            return

    def delete_func(self, params):
        title, quere_get, quere_del = params
        title = title
        path_id = QUERY_PATHES[quere_get]
        func = self.get_data(path_id)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if rez:
            path = DELETE_QUERES[quere_del]
            art = input_dialog.line_add_batch.currentText()
            data = (art,)
            self.ins_del_upd_data(path, data)
            self.get_message(3)
            return
        if not rez:
            self.get_message(1)
            return

    def delete_good_func(self):
        title = 'товара'
        quere_get = 'get_good_id'
        quere_del = 'delete_good'
        params = [title, quere_get, quere_del]
        return self.delete_func(params)

    def delete_oth_cost_func(self):
        title = 'прочих затрат'
        quere_get = 'get_oth_costs_id'
        qure_del = 'delete_oth_cost'
        params = [title, quere_get, qure_del]
        return self.delete_func(params)

    def delete_0_balance_func(self):
        quere_del = DELETE_QUERES['delete_0_balance']
        self.ins_del_upd_data(quere_del, (0,))
        return self.get_message(3)

    def delete_pre_sell_func(self):
        title = 'отправки'
        quere_get = QUERY_PATHES['get_note_num']
        note_id = self.get_data(quere_get)
        input_dialog = SearchDialog(title, note_id)
        rez = input_dialog.exec()
        if rez:
            art = input_dialog.line_add_batch.currentText()
            quere_4 = DELETE_QUERES['delete_pre_sell']
            self.ins_del_upd_data(quere_4, (art,))
            quere_5 = DELETE_QUERES['delete_note']
            self.ins_del_upd_data(quere_5, (art,))
            self.get_message(3)
            return
        if not rez:
            self.get_message(1)
            return



