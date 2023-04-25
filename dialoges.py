import datetime

from PyQt5.QtWidgets import QLineEdit, QDialog, QFormLayout, QDialogButtonBox, QVBoxLayout, QComboBox, QSpinBox, \
    QDateEdit, QMessageBox

from data_base import DB
from queres import QUERY_PATHES
from validators import int_valid


class BaseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.form_layout = QFormLayout()
        self.main_layout = QVBoxLayout()

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.db = DB()


class AddBatchOthercostsSellDialog(BaseDialog):
    def __init__(self, title, line_1, line_2, oper):
        super().__init__()
        self.validator = int_valid()
        self.title = title
        self.line_1 = line_1
        if oper != 'add_batch' and oper != 'add_sell_place':
            self.line_2 = line_2
        self.setWindowTitle(self.title)

        self.line_add_name = QLineEdit()
        if oper != 'add_batch' and oper != 'add_sell_place':
            self.line_add_money = QLineEdit()
            self.line_add_money.setValidator(self.validator)

        self.form_layout.addRow(self.line_1, self.line_add_name)
        if oper != 'add_batch' and oper != 'add_sell_place':
            self.form_layout.addRow(self.line_2, self.line_add_money)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)


class AddSellDialog(BaseDialog):
    def __init__(self, data=None):
        super().__init__()
        self.validator = int_valid()
        self.title = 'Добавление продажи'
        self.setWindowTitle(self.title)

        self.line_add_num = QLineEdit()
        self.line_add_num.setValidator(self.validator)
        self.line_add_art = QComboBox()
        func = self.db.get_good_id_name_list()
        for _ in func:
            self.line_add_art.addItem(str(_))

        self.line_size = QComboBox()
        size_list = ['0-1мес(56см)', '1-3мес(62см)', '3-6мес(68см)', '6-9мес(74см)', '9-12мес(80см)', '12-18мес(86см)',
                     '18-24мес(92см)', '24-36мес(98см)']
        for _ in size_list:
            self.line_size.addItem(_)
        self.line_add_val = QLineEdit()
        self.line_add_val.setValidator(self.validator)
        self.line_discount = QLineEdit()
        self.line_discount.setText('0')
        self.line_discount.setValidator(self.validator)
        self.line_sell_place = QComboBox()
        path = QUERY_PATHES['get_place_names']
        list_as = self.db.get_data_list(path)
        for _ in list_as:
            self.line_sell_place.addItem(_)
        now = datetime.datetime.now()
        self.line_date = QDateEdit(now)

        if data:
            note_num, good_id, size, value, disc, sell_pl, date = data
            self.line_add_num.setText(note_num)
            self.line_add_art.setCurrentIndex(good_id)
            self.line_size.setCurrentIndex(size)
            self.line_add_val.setText(value)
            self.line_discount.setText(disc)
            self.line_sell_place.setCurrentIndex(sell_pl)
            self.line_date.setDate(date)

        self.form_layout.addRow('4 посл. цифры накладной', self.line_add_num)
        self.form_layout.addRow('Артикул товара:', self.line_add_art)
        self.form_layout.addRow('Размер', self.line_size)
        self.form_layout.addRow('Количество:', self.line_add_val)
        self.form_layout.addRow('Скидка:', self.line_discount)
        self.form_layout.addRow('Где продано:', self.line_sell_place)
        self.form_layout.addRow('Дата продажи:', self.line_date)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)


class AddGoodDialog(BaseDialog):
    def __init__(self, data=None):
        super().__init__()
        self.validator = int_valid()
        self.setWindowTitle('Добавление товара')

        self.line_add_name = QLineEdit()
        self.line_add_buy_price = QLineEdit()
        self.line_add_buy_price.setValidator(self.validator)
        self.line_add_batch = QComboBox()
        self.line_add_number = QLineEdit()
        self.line_add_number.setValidator(self.validator)
        self.line_add_price = QLineEdit()
        self.line_add_price.setValidator(self.validator)

        path = QUERY_PATHES['get_batch_names']
        list_as = self.db.get_data_list(path)
        for _ in list_as:
            self.line_add_batch.addItem(_)

        self.first_size = QSpinBox()
        self.second_size = QSpinBox()
        self.third_size = QSpinBox()
        self.fourth_size = QSpinBox()
        self.fifth_size = QSpinBox()
        self.sixth_size = QSpinBox()
        self.seventh_size = QSpinBox()
        self.eighth_size = QSpinBox()

        if data:
            name, b_price, batch, number, s_price, first, second, third, fourth, fifth, sixth, seventh, eighth = data
            self.line_add_name.setText(name)
            self.line_add_buy_price.setText(b_price)
            self.line_add_batch.setCurrentIndex(batch)
            self.line_add_number.setText(number)
            self.line_add_price.setText(s_price)
            self.first_size.setValue(int(first))
            self.second_size.setValue(int(second))
            self.third_size.setValue(int(third))
            self.fourth_size.setValue(int(fourth))
            self.fifth_size.setValue(int(fifth))
            self.sixth_size.setValue(int(sixth))
            self.seventh_size.setValue(int(seventh))
            self.eighth_size.setValue(int(eighth))

        self.form_layout.addRow('Наименование:', self.line_add_name)
        self.form_layout.addRow('Цена закупки:', self.line_add_buy_price)
        self.form_layout.addRow('Партия:', self.line_add_batch)
        self.form_layout.addRow('Количество:', self.line_add_number)
        self.form_layout.addRow('Цена продажи:', self.line_add_price)

        self.form_layout.addRow('Кол-во 0-1мес(56см)', self.first_size)
        self.form_layout.addRow('Кол-во 1-3мес(62см)', self.second_size)
        self.form_layout.addRow('Кол-во 3-6мес(68см)', self.third_size)
        self.form_layout.addRow('Кол-во 6-9мес(74см)', self.fourth_size)
        self.form_layout.addRow('Кол-во 9-12мес(80см)', self.fifth_size)
        self.form_layout.addRow('Кол-во 12-18мес(86см)', self.sixth_size)
        self.form_layout.addRow('Кол-во 18-24мес(92см)', self.seventh_size)
        self.form_layout.addRow('Кол-во 24-36мес(98см)', self.eighth_size)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)

        self.setLayout(self.main_layout)


class SearchDialog(BaseDialog):
    def __init__(self, title, func):
        super().__init__()
        self.setWindowTitle(f'Поиск {title}')
        self.line_add_batch = QComboBox()

        list_as = func
        for _ in list_as:
            self.line_add_batch.addItem(str(_))

        self.form_layout.addRow('Артикул:', self.line_add_batch)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)


class SearchDateDialog(BaseDialog):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(f'Поиск {title}')
        past = datetime.datetime.now() - datetime.timedelta(days=7)
        self.line_date_past = QDateEdit(past)
        now = datetime.datetime.now()
        self.line_date_now = QDateEdit(now)

        self.form_layout.addRow('Начало периода:', self.line_date_past)
        self.form_layout.addRow('Конец периода:', self.line_date_now)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)


class EditGoodDialog(BaseDialog):
    def __init__(self, art):
        super().__init__()
        self.setWindowTitle('Изменение товара')
        self.validator = int_valid()
        self.line_add_id = QLineEdit()
        self.line_add_name = QLineEdit()
        self.line_add_buy_price = QLineEdit()
        self.line_add_batch = QLineEdit()
        self.line_add_number = QLineEdit()
        self.line_add_price = QLineEdit()

        self.first_size = QSpinBox()
        self.second_size = QSpinBox()
        self.third_size = QSpinBox()
        self.fourth_size = QSpinBox()
        self.fifth_size = QSpinBox()
        self.sixth_size = QSpinBox()
        self.seventh_size = QSpinBox()
        self.eighth_size = QSpinBox()


        query = QUERY_PATHES['get_current_good']
        art, desc, b_price, batch, num, price = self.db.get_data_with_param(query, art)[0]
        query_size = QUERY_PATHES['get_size_by_good']
        _, _, first, second, third, fourth, fifth, sixth, seventh, eighth =\
            self.db.get_data_with_param(query_size, art)[0]
        self.line_add_id.setText(str(art))
        self.line_add_id.setReadOnly(True)
        self.line_add_name.setText(str(desc))
        self.line_add_buy_price.setText(str(b_price))
        self.line_add_buy_price.setValidator(self.validator)
        self.line_add_batch.setText(str(batch))
        self.line_add_batch.setReadOnly(True)
        self.line_add_number.setText(str(num))
        self.line_add_number.setValidator(self.validator)
        self.line_add_price.setText(str(price))
        self.line_add_price.setValidator(self.validator)

        self.first_size.setValue(first)
        self.second_size.setValue(second)
        self.third_size.setValue(third)
        self.fourth_size.setValue(fourth)
        self.fifth_size.setValue(fifth)
        self.sixth_size.setValue(sixth)
        self.seventh_size.setValue(seventh)
        self.eighth_size.setValue(eighth)

        self.form_layout.addRow('Артикул:', self.line_add_id)
        self.form_layout.addRow('Наименование:', self.line_add_name)
        self.form_layout.addRow('Цена закупки:', self.line_add_buy_price)
        self.form_layout.addRow('Партия:', self.line_add_batch)
        self.form_layout.addRow('Количество:', self.line_add_number)
        self.form_layout.addRow('Цена продажи:', self.line_add_price)

        self.form_layout.addRow('Кол-во 0-1мес(56см)', self.first_size)
        self.form_layout.addRow('Кол-во 1-3мес(62см)', self.second_size)
        self.form_layout.addRow('Кол-во 3-6мес(68см)', self.third_size)
        self.form_layout.addRow('Кол-во 6-9мес(74см)', self.fourth_size)
        self.form_layout.addRow('Кол-во 9-12мес(80см)', self.fifth_size)
        self.form_layout.addRow('Кол-во 12-18мес(86см)', self.sixth_size)
        self.form_layout.addRow('Кол-во 18-24мес(92см)', self.seventh_size)
        self.form_layout.addRow('Кол-во 24-36мес(98см)', self.eighth_size)

        self.main_layout.addLayout(self.form_layout)
        self. main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)

