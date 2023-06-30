import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QDialog, QFormLayout, QDialogButtonBox, QVBoxLayout, QComboBox, QSpinBox, \
    QDateEdit, QGridLayout, QHBoxLayout, QLabel, QPushButton

from data_base import DB
from queres import QUERY_PATHES
from validators import int_valid


from PyQt5 import QtCore, QtGui, QtWidgets


class AddSellDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.click_count = 3

        self.art = ''
        self.size = ''

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.db = DB()
        self.validator = int_valid()
        self.title = 'Накладная по продаже'
        self.setWindowTitle(self.title)
        self.resize(594, 130)

        button_add_good = QPushButton('Добавить товар')
        self.main_layout.addWidget(button_add_good, 0, 3)
        button_add_good.setEnabled(False)
        self.main_layout.addWidget(QLabel('Скидка:'), 2, 3, alignment=Qt.AlignmentFlag.AlignTop)

        button_confirm_note = QPushButton('Подтвердить накладную')
        self.main_layout.addWidget(button_confirm_note, 0, 4)
        button_confirm_note.setEnabled(False)

        self.main_layout.addWidget(QLabel('4 посл. цифры накладной'), 0, 0)
        self.line_add_num = QLineEdit()

        self.main_layout.addWidget(self.line_add_num, 1, 0)
        self.main_layout.addWidget(QLabel('Товар:'), 2, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.line_add_num.textChanged.connect(lambda text: button_add_good.setEnabled(bool(text)))

        self.main_layout.addWidget(QLabel('Где продано:'), 0, 1)
        self.line_sell_place = QtWidgets.QComboBox()
        path = QUERY_PATHES['get_place_names']
        list_as = self.db.get_data_list(path)
        for _ in list_as:
            self.line_sell_place.addItem(_)
        self.main_layout.addWidget(self.line_sell_place, 1, 1)
        self.main_layout.addWidget(QLabel('Размер:'), 2, 1, alignment=Qt.AlignmentFlag.AlignTop)

        self.main_layout.addWidget(QLabel('Дата продажи:'), 0, 2)
        now = datetime.datetime.now()
        self.line_date = QDateEdit(now)
        self.main_layout.addWidget(self.line_date, 1, 2)
        self.main_layout.addWidget(QLabel('Количество:'), 2, 2, alignment=Qt.AlignmentFlag.AlignTop)

        def add_good_form():
            button_confirm_note.setEnabled(False)
            button_add_good.setEnabled(False)

            self.line_add_art = QComboBox()
            func = self.db.get_good_id_name_list()
            self.line_add_art.addItem('-----')
            for _ in func:
                self.line_add_art.addItem(str(_))
            self.line_add_art.activated[str].connect(add_size_form)
            self.main_layout.addWidget(self.line_add_art, self.click_count+1, 0, alignment=Qt.AlignmentFlag.AlignTop)

            self.line_size = QComboBox()
            self.line_size.addItem('-----')
            size_list = ['0-1мес(56см)', '1-3мес(62см)', '3-6мес(68см)', '6-9мес(74см)', '9-12мес(80см)',
                         '12-18мес(86см)',
                         '18-24мес(92см)', '24-36мес(98см)']
            for _ in size_list:
                self.line_size.addItem(_)
            self.line_size.activated[str].connect(add_val_form)
            self.main_layout.addWidget(self.line_size, self.click_count + 1, 1, alignment=Qt.AlignmentFlag.AlignTop)

            self.line_discount = QLineEdit()
            self.line_discount.setText('0')
            self.line_discount.setValidator(self.validator)
            self.main_layout.addWidget(self.line_discount, self.click_count+1, 3, alignment=Qt.AlignmentFlag.AlignTop)
            self.click_count += 1

        def add_size_form(arg):
                self.art = arg.split()[0]

        def add_val_form(arg):
            self.size = arg
            self.line_add_val = QSpinBox()
            if self.art != '-----' and self.size != '-----':
                size_dict_2 = {
                                '0-1мес(56см)': 'get_first', '1-3мес(62см)': 'get_second',
                                '3-6мес(68см)': 'get_third', '6-9мес(74см)': 'get_fourth',
                                '9-12мес(80см)': 'get_fifth', '12-18мес(86см)': 'get_sixth',
                                '18-24мес(92см)': 'get_seventh', '24-36мес(98см)': 'get_eighth'
                            }

                size_balance = self.db.get_data_with_param(QUERY_PATHES[size_dict_2[self.size]], self.art)[0][0]
                self.line_add_val.setMaximum(size_balance)
            self.main_layout.addWidget(self.line_add_val, self.click_count, 2, alignment=Qt.AlignmentFlag.AlignTop)

            self.line_add_val.textChanged.connect(lambda text: button_confirm_note.setEnabled(bool(text)))
            self.line_add_val.textChanged.connect(lambda text: button_add_good.setEnabled(bool(text)))

        button_add_good.clicked.connect(add_good_form)
        button_confirm_note.clicked.connect(self.accept)


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


class EditGoodDialog2(BaseDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Изменение товара')
        self.validator = int_valid()
        self.line_add_id = QComboBox()
        self.line_add_id.addItem('----')
        func = self.db.get_good_id_name_list()
        for _ in func:
            self.line_add_id.addItem(str(_))
        self.line_add_id.activated[str].connect(self.db_data)

        self.line_add_name = QLineEdit()
        self.line_add_buy_price = QLineEdit()
        self.line_add_batch = QComboBox()

        self.line_add_number = QLineEdit()
        self.line_balance = QLineEdit()
        self.line_add_price = QLineEdit()

        self.first_size = QSpinBox()
        self.second_size = QSpinBox()
        self.third_size = QSpinBox()
        self.fourth_size = QSpinBox()
        self.fifth_size = QSpinBox()
        self.sixth_size = QSpinBox()
        self.seventh_size = QSpinBox()
        self.eighth_size = QSpinBox()

        self.form_layout.addRow('Артикул:', self.line_add_id)
        self.form_layout.addRow('Наименование:', self.line_add_name)
        self.form_layout.addRow('Цена закупки:', self.line_add_buy_price)
        self.form_layout.addRow('Партия:', self.line_add_batch)
        self.form_layout.addRow('Количество:', self.line_add_number)
        self.form_layout.addRow('Остаток:', self.line_balance)
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

    def db_data(self, id_str):
        self.good_id = id_str.split()[0]
        if self.line_add_id.currentText() != '----':
            query = QUERY_PATHES['get_current_good_edit']
            art, desc, b_price, batch, num, price, balance = self.db.get_data_with_param(query, self.good_id)[0]
            query_size = QUERY_PATHES['get_size_by_good']
            _, _, first, second, third, fourth, fifth, sixth, seventh, eighth = \
                self.db.get_data_with_param(query_size, art)[0]
            result = (
                art, desc, b_price, batch, num, price, balance,
                first, second, third, fourth, fifth, sixth, seventh, eighth
            )
            return self.fill_lines(result)
        else:
            result = (None, None, None, None, None, None, None, 0, 0, 0, 0, 0, 0, 0, 0)
            return self.fill_lines(result)

    def fill_lines(self, data):
        art, desc, b_price, batch, num, price, balance, first, second, third, fourth, fifth, sixth, seventh, eighth = data
        self.line_add_id.setCurrentText(str(art))
        self.line_add_name.setText(str(desc))
        self.line_add_buy_price.setText(str(b_price))
        self.line_add_buy_price.setValidator(self.validator)

        self.line_add_batch.clear()
        path = QUERY_PATHES['get_batch_names']
        list_as = self.db.get_data_list(path)
        for _ in list_as:
            self.line_add_batch.addItem(_)
        self.line_add_batch.setCurrentIndex(self.line_add_batch.findText(batch))

        self.line_add_number.setText(str(num))
        self.line_add_number.setValidator(self.validator)
        self.line_balance.setText(str(balance))
        self.line_balance.setReadOnly(True)
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
