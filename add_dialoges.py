from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir, QFile, QIODevice
from PyQt5.QtWidgets import QLineEdit, QDialog, QFormLayout, QDialogButtonBox, QVBoxLayout, QComboBox, QPushButton, \
    QHBoxLayout, QFileDialog

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
        if oper != 'add_batch':
            self.line_2 = line_2
        self.setWindowTitle(self.title)

        self.line_add_name = QLineEdit()
        if oper != 'add_batch':
            self.line_add_money = QLineEdit()
            self.line_add_money.setValidator(self.validator)

        self.form_layout.addRow(self.line_1, self.line_add_name)
        if oper != 'add_batch':
            self.form_layout.addRow(self.line_2, self.line_add_money)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)


class AddSellDialog(BaseDialog):
    def __init__(self):
        super().__init__()
        self.validator = int_valid()
        self.title = 'Добавление продажи'
        self.line_1 = '4 посл. цифры накладной'
        self.line_2 = 'Артикул товара:'
        self.line_3 = 'Количество:'
        self.line_4 = 'Скидка:'
        self.line_5 = 'Где продано:'
        self.setWindowTitle(self.title)

        self.line_add_num = QLineEdit()
        self.line_add_num.setValidator(self.validator)
        self.line_add_art = QLineEdit()
        self.line_add_art.setValidator(self.validator)
        self.line_add_val = QLineEdit()
        self.line_add_val.setValidator(self.validator)
        self.line_discount = QLineEdit()
        self.line_discount.setText('0')
        self.line_discount.setValidator(self.validator)
        self.line_sell_place = QComboBox()

        path = QUERY_PATHES['get_place_names']
        list_as = self.db.get_data(path)
        for _ in list_as:
            self.line_sell_place.addItem(_)

        self.form_layout.addRow(self.line_1, self.line_add_num)
        self.form_layout.addRow(self.line_2, self.line_add_art)
        self.form_layout.addRow(self.line_3, self.line_add_val)
        self.form_layout.addRow(self.line_4, self.line_discount)
        self.form_layout.addRow(self.line_5, self.line_sell_place)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)


class AddGoodDialog(BaseDialog):
    def __init__(self):
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
        list_as = self.db.get_data(path)
        for _ in list_as:
            self.line_add_batch.addItem(_)

        self.form_layout.addRow('Наименование:', self.line_add_name)
        self.form_layout.addRow('Цена закупки:', self.line_add_buy_price)
        self.form_layout.addRow('Партия:', self.line_add_batch)
        self.form_layout.addRow('Количество:', self.line_add_number)
        self.form_layout.addRow('Цена продажи:', self.line_add_price)


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
        # self.line_add_sell = QLineEdit()

        query = QUERY_PATHES['get_current_good']
        art, desc, b_price, batch, num, price = self.db.get_current_data_by_id(query, art) #, sell
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
        # self.line_add_sell.setText(str(sell))
        # self.line_add_sell.setValidator(self.validator)

        self.form_layout.addRow('Артикул:', self.line_add_id)
        self.form_layout.addRow('Наименование:', self.line_add_name)
        self.form_layout.addRow('Цена закупки:', self.line_add_buy_price)
        self.form_layout.addRow('Партия:', self.line_add_batch)
        self.form_layout.addRow('Количество:', self.line_add_number)
        self.form_layout.addRow('Цена продажи:', self.line_add_price)
        # self.form_layout.addRow('Продано:', self.line_add_sell)

        self.main_layout.addLayout(self.form_layout)
        self. main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)


# class EditSellBatch(BaseDialog):
#     def __init__(self, title, func, oper=None):
#         super().__init__()
#         self.setWindowTitle(f'Изменение {title}')
#         self.validator = int_valid()
#         self.line_add_id = QLineEdit()
#         self.line_add_name = QLineEdit()
#         self.line_add_money = QLineEdit()
#         self.operation = oper
#
#         art, desc, money = func
#         self.line_add_id.setText(str(art))
#         self.line_add_id.setReadOnly(True)
#         self.line_add_name.setText(str(desc))
#         if self.operation == 1:
#             self.line_add_name.setReadOnly(True)
#         self.line_add_money.setText(str(money))
#         self.line_add_money.setValidator(self.validator)
#
#         self.form_layout.addRow('Артикул:', self.line_add_id)
#         self.form_layout.addRow('Наименование:', self.line_add_name)
#         self.form_layout.addRow('Количество/Сумма:', self.line_add_money)
#
#         self.main_layout.addLayout(self.form_layout)
#         self.main_layout.addWidget(self.button_box)
#         self.setLayout(self.main_layout)
