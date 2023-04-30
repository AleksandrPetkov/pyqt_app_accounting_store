from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from dialoges import AddBatchOthercostsSellDialog, AddGoodDialog, \
    SearchDialog, AddSellDialog, SearchDateDialog, EditGoodDialog2
from data_base import DB
from main_win_table import MainWinTableTemplate
from queres import QUERY_PATHES, ADD_QUERES, UPDATE_QUERES, DELETE_QUERES


class AppShop(QtWidgets.QMainWindow, MainWinTableTemplate, DB):
    def __init__(self):
        super().__init__()

        self.add_batch.triggered.connect(self.add_batch_func)
        self.add_other_costs.triggered.connect(self.add_other_costs_func)
        self.add_good.triggered.connect(self.add_good_func)
        self.action.triggered.connect(self.add_pre_sell_func)
        self.action_2.triggered.connect(self.submit_sell_func)
        self.add_sell_pl.triggered.connect(self.add_sell_place)

        self.show_othercosts.triggered.connect(self.show_other_costs_table)
        self.balance_by_bacth.triggered.connect(self.show_goods_bybatch_table)
        self.all_balance.triggered.connect(self.show_goods_table)
        self.fin_result.triggered.connect(self.show_profit_table)
        self.action_3.triggered.connect(self.show_pre_sell_table)
        self.show_batches_ta.triggered.connect(self.show_batches_table)
        self.order_place.triggered.connect(self.show_places_table)
        self.size_by_cloth.triggered.connect(self.show_size_by_id_table)
        self.fin_res_by_order.triggered.connect(self.show_profit_by_order)

        self.change_good.triggered.connect(self.edit_good)

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
        if oper == 4:
            return QMessageBox.information(self, 'Внимание', 'Недостаточно товара этого размера!')
        if oper == 5:
            return QMessageBox.information(self, 'Внимание',
                                           'Количество закупленного товара не'
                                           'совпадает с количеством размеров!')

    def add_batch_func(self):
        title = 'Добавление партии'
        line_1 = 'Наименование:'
        oper = 'add_batch'
        input_dialog = AddBatchOthercostsSellDialog(title, line_1, None, oper)
        rez = input_dialog.exec()
        if not rez:
            self.get_message(1)
            return
        name = input_dialog.line_add_name.text()
        if not name:
            self.get_message(2)
            self.add_batch_func()
            return
        if rez:
            query = ADD_QUERES['add_batch']
            data = (name,)
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

    def add_pre_sell_func(self, data=None):
        input_dialog = AddSellDialog(data)
        rez = input_dialog.exec()

        num = input_dialog.line_add_num.text()
        art = input_dialog.line_add_art.currentText().split()[0]
        size = input_dialog.line_size.currentText()
        sell_p = self.get_data_with_param(QUERY_PATHES['get_current_good'], art)[0][5]
        val = input_dialog.line_add_val.text()
        discount = input_dialog.line_discount.text()
        place_id = input_dialog.line_sell_place.currentText()
        date = input_dialog.line_date.date().toPyDate()

        check_art = input_dialog.line_add_art.currentIndex()
        check_size = input_dialog.line_size.currentIndex()
        check_place = input_dialog.line_sell_place.currentIndex()
        check_date = input_dialog.line_date.date()
        data_check = (num, check_art, check_size, val, discount, check_place, check_date)

        if not rez:
            self.get_message(1)
            return

        if not num or not art or not val:
            self.get_message(2)
            self.add_pre_sell_func(data_check)
            return

        if rez:
            size_dict_2 = {
                '0-1мес(56см)': 'get_first', '1-3мес(62см)': 'get_second',
                '3-6мес(68см)': 'get_third', '6-9мес(74см)': 'get_fourth',
                '9-12мес(80см)': 'get_fifth', '12-18мес(86см)': 'get_sixth',
                '18-24мес(92см)': 'get_seventh', '24-36мес(98см)': 'get_eighth'
            }
            size_balance = self.get_data_with_param(QUERY_PATHES[size_dict_2[size]], art)[0][0]
            if size_balance >= int(val):
                func = self.get_data_list(QUERY_PATHES['get_note_num'])
                size_dict = {
                    '0-1мес(56см)': 'update_first_sell', '1-3мес(62см)': 'update_second_sell',
                    '3-6мес(68см)': 'update_third_sell', '6-9мес(74см)': 'update_fourth_sell',
                    '9-12мес(80см)': 'update_fifth_sell', '12-18мес(86см)': 'update_sixth_sell',
                    '18-24мес(92см)': 'update_seventh_sell', '24-36мес(98см)': 'update_eighth_sell'
                }
                size_query = UPDATE_QUERES[size_dict[size]]
                query_data = (int(val), art)
                self.ins_del_upd_data(size_query, query_data)

                if int(num) not in func:
                    query_1 = ADD_QUERES['add_deliv_note']
                    data_1 = (num, place_id)
                    self.ins_del_upd_data(query_1, data_1)
                query = ADD_QUERES['add_pre_sell']
                data = (num, art, sell_p, val, discount, size, date)
                self.ins_del_upd_data(query, data)
                quere_1 = ADD_QUERES['add_sell']
                self.ins_del_upd_data(quere_1, (val, art))
                self.get_message(3)
                return
            else:
                self.get_message(4)
                self.add_pre_sell_func(data_check)
                return

    def add_good_func(self, data_1=None):
        input_dialog = AddGoodDialog(data_1)
        rez = input_dialog.exec()
        if not rez:
            self.get_message(1)
            return
        name = input_dialog.line_add_name.text()
        buy_price = input_dialog.line_add_buy_price.text()
        quere_b_id = QUERY_PATHES['get_batch_id_by_name']
        batch = self.get_data_with_param(quere_b_id, input_dialog.line_add_batch.currentText())[0][0]
        number = input_dialog.line_add_number.text()
        price = input_dialog.line_add_price.text()

        first = input_dialog.first_size.text()
        second = input_dialog.second_size.text()
        third = input_dialog.third_size.text()
        fourth = input_dialog.fourth_size.text()
        fifth = input_dialog.fifth_size.text()
        sixth = input_dialog.sixth_size.text()
        seventh = input_dialog.seventh_size.text()
        eighth = input_dialog.eighth_size.text()

        current_index = input_dialog.line_add_batch.currentIndex()

        data_check = (name, buy_price, current_index, number, price, first, second,
                      third, fourth, fifth, sixth, seventh, eighth)

        if not name or not number or not price:
            self.get_message(2)
            self.add_good_func(data_check)
            return
        if int(number) != sum([int(_) for _ in [first, second, third, fourth, fifth, sixth, seventh, eighth]]):
            self.get_message(5)
            self.add_good_func(data_check)
            return
        if rez:
            query = ADD_QUERES['add_good']
            data = (name, buy_price, batch, number, price)
            self.ins_del_upd_data(query, data)

            query_2 = QUERY_PATHES['get_buy_price']
            last_ins_id = self.get_data_without_param(query_2)[0][0]
            costs = int(buy_price) * int(number)
            data_list = (costs, last_ins_id)
            query_3 = ADD_QUERES['add_batch_cost']
            self.ins_del_upd_data(query_3, data_list)

            last_ins_good_id = self.get_data_without_param(QUERY_PATHES['get_last_good_id'])[0][0]
            query_4 = ADD_QUERES['add_good_to_size']
            data_list_2 = (last_ins_good_id, name)
            self.ins_del_upd_data(query_4, data_list_2)

            query_size = ADD_QUERES['add_size']
            data = (first, second, third, fourth, fifth, sixth,
                    seventh, eighth, last_ins_good_id)
            self.ins_del_upd_data(query_size, data)
            self.get_message(3)
            return

    def add_sell_place(self):
        title = 'Добавление места продажи'
        line_1 = 'Наименование:'
        oper = 'add_sell_place'
        input_dialog = AddBatchOthercostsSellDialog(title, line_1, None, oper)
        rez = input_dialog.exec()
        if not rez:
            self.get_message(1)
            return
        if rez:
            place_name = input_dialog.line_add_name.text()
            query = ADD_QUERES['add_sell_place']
            data = (place_name,)
            self.ins_del_upd_data(query, data)
            self.get_message(3)
            return

    def submit_sell_func(self):
        title = 'отправки'
        path_id = QUERY_PATHES['get_note_num']
        func = self.get_data_list(path_id)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if not rez:
            self.get_message(1)
            return
        if rez:
            quere = QUERY_PATHES['get_pre_sell']
            sell_id = input_dialog.line_add_batch.currentText()
            pre_sells = self.get_data_with_param(quere, sell_id)
            for elem in pre_sells:
                good_id, sell_price, value, discount, size, date = elem
                # quere_1 = ADD_QUERES['add_sell']
                # self.ins_del_upd_data(quere_1, (value, good_id))

                good_n, buy_price = self.get_data_with_param(QUERY_PATHES['get_good_n_buy_p'], good_id)[0]
                data_income = (sell_id, good_id, good_n, size, buy_price, sell_price, value, discount, date)
                quere_2 = ADD_QUERES['add_income']
                self.ins_del_upd_data(quere_2, data_income)
            quere_3 = ADD_QUERES['add_place_stat']
            place_n = self.get_data_with_param(QUERY_PATHES['get_place_names_note'], sell_id)[0][0]
            self.ins_del_upd_data(quere_3, (1, place_n))
            quere_4 = DELETE_QUERES['delete_pre_sell']
            self.ins_del_upd_data(quere_4, (sell_id,))
            quere_5 = DELETE_QUERES['delete_note']
            self.ins_del_upd_data(quere_5, (sell_id,))
            self.get_message(3)
            return

    def show_other_costs_table(self):
        self.get_editable_table([1, 2], 'other_costs', 'other_costs', 'delete_oth_sum')

    def show_goods_table(self):
        query_path = QUERY_PATHES['general_balance']
        header_list = ['Артикул', 'Наименование', 'Цена закупки', 'Партия',
                       'Закуплено единиц', 'Продажная цена', 'Продажи', 'Остаток']
        self.get_noneditable_table(query_path, header_list)

    def show_goods_bybatch_table(self):
        title = 'партии'
        path = QUERY_PATHES['get_batch_names']
        func = self.get_data_list(path)
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if rez:
            quere_b_id = QUERY_PATHES['get_batch_id_by_name']
            data = self.get_data_with_param(quere_b_id, input_dialog.line_add_batch.currentText())[0][0]
            query_path = QUERY_PATHES['batch_balance']
            header_list = ['Артикул', 'Наименование', 'Цена закупки', 'Партия',
                           'Закуплено единиц', 'Продажная цена', 'Продажи', 'Остаток', 'Плановый доход']
            self.get_noneditable_table(query_path, header_list, data, 'good_by_batch')

    def show_batches_table(self):
        self.get_editable_table([1], 'batch', '0', 'delete_batch_sum')

    def show_profit_table(self):
        name = 'Cумма'
        del_query = DELETE_QUERES['delete_oth_sum']
        del_query_2 = DELETE_QUERES['delete_batch_sum']
        self.ins_del_upd_data(del_query, (name,))
        self.ins_del_upd_data(del_query_2, (name,))
        self.get_profit_table()

    def show_profit_by_order(self):
        title = 'по дате'
        input_dialog = SearchDateDialog(title)
        rez = input_dialog.exec()
        if rez:
            past_date = input_dialog.line_date_past.date().toPyDate().isoformat()
            now_date = input_dialog.line_date_now.date().toPyDate().isoformat()
            data = (past_date, now_date, past_date, now_date)
            query = QUERY_PATHES['get_income_by_date']
            header_list = ['№ накладной', 'Артикул', 'Наименование', 'Размер', 'Цена закупки', 'Цена продажи',
                           'Продано ед.', 'Скидка', 'Прибыль', 'Дата']
            oper = 'show_profit_by_order'
            self.get_noneditable_table(query, header_list, data, oper)

    def show_pre_sell_table(self):
        query_path = QUERY_PATHES['pre_sell']
        header_list = ['4 цифры накладной', 'Артикул товара',
                       'Количество проданного', 'Скидка', 'Место продажи']
        self.get_noneditable_table(query_path, header_list)

    def show_places_table(self):
        query_path = QUERY_PATHES['get_places']
        header_list = ['Наименование', 'Количество заказов']
        self.get_noneditable_table(query_path, header_list)

    def show_size_by_id_table(self):
        title = 'товара'
        func = self.get_good_id_name_list()
        input_dialog = SearchDialog(title, func)
        input_dialog.exec()
        art = input_dialog.line_add_batch.currentText().split()[0]
        query = QUERY_PATHES['get_size_by_good']
        header_list = ['Артикул', 'Наименование', '0-1мес(56см)', '1-3мес(62см)', '3-6мес(68см)', '6-9мес(74см)',
                       '9-12мес(80см)', '12-18мес(86см)', '18-24мес(92см)', '24-36мес(98см)']
        oper = 'show_size'
        self.get_noneditable_table(query, header_list, art, oper)

    def edit_good(self, data=None):
        edit_dialog = EditGoodDialog2(data)
        rez = edit_dialog.exec()

        art_1 = edit_dialog.line_add_id.currentText().split()[0]
        desc = edit_dialog.line_add_name.text()
        b_price = edit_dialog.line_add_buy_price.text()
        batch = edit_dialog.line_add_batch.currentText()
        buy = edit_dialog.line_add_number.text()
        price = edit_dialog.line_add_price.text()

        first = edit_dialog.first_size.text()
        second = edit_dialog.second_size.text()
        third = edit_dialog.third_size.text()
        fourth = edit_dialog.fourth_size.text()
        fifth = edit_dialog.fifth_size.text()
        sixth = edit_dialog.sixth_size.text()
        seventh = edit_dialog.seventh_size.text()
        eighth = edit_dialog.eighth_size.text()
        sizes = [first, second, third, fourth, fifth, sixth, seventh, eighth]

        if art_1 != '----':
            buy_old, balance = self.get_data_with_param(QUERY_PATHES['get_good_balance'], art_1)[0]

        if not rez:
            self.get_message(1)
            return

        if (int(buy) - int(buy_old) + int(balance)) != sum([int(_) for _ in sizes]):
            self.get_message(5)
            return

        if rez:
            query_b = QUERY_PATHES['get_current_good']
            old_b_price, batch_n, old_b_num = self.get_data_with_param(query_b, edit_dialog.good_id)[0][2:5]
            path = UPDATE_QUERES['update_good']
            data = (desc, b_price, buy, price, art_1)
            self.ins_del_upd_data(path, data)
            minus = - int(old_b_price)*int(old_b_num)
            plus = int(b_price)*int(buy)
            quere_b_id = QUERY_PATHES['get_batch_id_by_name']
            batch_id_old = self.get_data_with_param(quere_b_id, batch_n)[0][0]
            batch_id_new = self.get_data_with_param(quere_b_id, batch)[0][0]
            data_minus = [minus, batch_id_old]
            data_plus = [plus, batch_id_new]
            query_3 = ADD_QUERES['add_batch_cost']
            self.ins_del_upd_data(query_3, data_minus)
            self.ins_del_upd_data(query_3, data_plus)
            query_up_size = UPDATE_QUERES['update_size']
            data_size = (desc, first, second, third, fourth, fifth, sixth, seventh, eighth, art_1)
            self.ins_del_upd_data(query_up_size, data_size)
            self.get_message(3)
            return

    def delete_func(self, params):
        title, quere_get, quere_del = params
        title = title
        path_id = QUERY_PATHES[quere_get]
        func = self.get_data_list(path_id)
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
        func = self.get_good_id_name_list()
        input_dialog = SearchDialog(title, func)
        rez = input_dialog.exec()
        if rez:
            art = input_dialog.line_add_batch.currentText().split()[0]
            quere_7 = QUERY_PATHES['get_good_bp_bn']
            asdf = self.get_data_with_param(quere_7, art)[0]
            b_price, b_id, b_num = asdf
            upd_batch = int(b_price)*int(b_num)
            quere_upd = UPDATE_QUERES['update_batch']
            self.ins_del_upd_data(quere_upd, (upd_batch, b_id))
            quere_4 = DELETE_QUERES['delete_good']
            self.ins_del_upd_data(quere_4, (art,))
            self.get_message(3)
            return
        if not rez:
            self.get_message(1)
            return

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
        note_id = self.get_data_list(quere_get)
        input_dialog = SearchDialog(title, note_id)
        rez = input_dialog.exec()
        if rez:
            art = input_dialog.line_add_batch.currentText()
            size_info = self.get_data_with_param(QUERY_PATHES['get_size_info'], art)

            size_dict = {'0-1мес(56см)': 'update_first_dellsell', '1-3мес(62см)': 'update_second_dellsell',
                         '3-6мес(68см)': 'update_third_dellsell', '6-9мес(74см)': 'update_fourth_dellsell',
                         '9-12мес(80см)': 'update_fifth_dellsell', '12-18мес(86см)': 'update_sixth_dellsell',
                         '18-24мес(92см)': 'update_seventh_dellsell', '24-36мес(98см)': 'update_eighth_dellsell'}
            for elem in size_info:
                good_id, value, size = elem
                size_query = UPDATE_QUERES[size_dict[size]]
                query_data = (int(value), good_id)
                self.ins_del_upd_data(size_query, query_data)

            quere = QUERY_PATHES['get_pre_sell']
            pre_sells = self.get_data_with_param(quere, art)
            for elem in pre_sells:
                good_id, _, value, _, _, _ = elem
                quere_6 = ADD_QUERES['add_del_sell']
                self.ins_del_upd_data(quere_6, (int(value), good_id))
            quere_4 = DELETE_QUERES['delete_pre_sell']
            self.ins_del_upd_data(quere_4, (art,))
            quere_5 = DELETE_QUERES['delete_note']
            self.ins_del_upd_data(quere_5, (art,))
            self.get_message(3)
            return
        if not rez:
            self.get_message(1)
            return
