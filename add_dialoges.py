from PyQt5.QtWidgets import QLineEdit, QDialog, QFormLayout, QDialogButtonBox, QVBoxLayout, QComboBox

import data_base
from data_base import DB
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


class AddBatchOthercostsDialog(BaseDialog):
    def __init__(self, title, line_1, line_2):
        super().__init__()
        self.validator = int_valid()
        self.title = title
        self.line_1 = line_1
        self.line_2 = line_2
        self.setWindowTitle(self.title)

        self.line_add_name = QLineEdit()
        self.line_add_money = QLineEdit()
        self.line_add_money.setValidator(self.validator)

        self.form_layout.addRow(self.line_1, self.line_add_name)
        self.form_layout.addRow(self.line_2, self.line_add_money)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)


class AddGoodDialog(BaseDialog):
    def __init__(self):
        super().__init__()
        self.validator = int_valid()
        self.setWindowTitle('Добавление товара')

        self.line_add_name = QLineEdit()
        self.line_add_batch = QComboBox()
        self.line_add_number = QLineEdit()
        self.line_add_number.setValidator(self.validator)
        self.line_add_price = QLineEdit()
        self.line_add_price.setValidator(self.validator)

        path = data_base.QUERY_PATHES['get_batch_names']
        list_as = self.db.get_data(path)
        for _ in list_as:
            self.line_add_batch.addItem(_)

        self.form_layout.addRow('Наименование:', self.line_add_name)
        self.form_layout.addRow('Партия:', self.line_add_batch)
        self.form_layout.addRow('Количество:', self.line_add_number)
        self.form_layout.addRow('Продажная цена:', self.line_add_price)

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
        self.line_add_batch = QLineEdit()
        self.line_add_number = QLineEdit()
        self.line_add_price = QLineEdit()
        self.line_add_sell = QLineEdit()

        query = data_base.QUERY_PATHES['get_current_good']
        art, desc, batch, num, price, sell = self.db.get_current_data_by_id(query, art)
        self.line_add_id.setText(str(art))
        self.line_add_id.setReadOnly(True)
        self.line_add_name.setText(str(desc))
        self.line_add_batch.setText(str(batch))
        self.line_add_batch.setReadOnly(True)
        self.line_add_number.setText(str(num))
        self.line_add_number.setValidator(self.validator)
        self.line_add_price.setText(str(price))
        self.line_add_price.setValidator(self.validator)
        self.line_add_sell.setText(str(sell))
        self.line_add_sell.setValidator(self.validator)

        self.form_layout.addRow('Артикул:', self.line_add_id)
        self.form_layout.addRow('Наименование:', self.line_add_name)
        self.form_layout.addRow('Партия:', self.line_add_batch)
        self.form_layout.addRow('Количество:', self.line_add_number)
        self.form_layout.addRow('Продажная цена:', self.line_add_price)
        self.form_layout.addRow('Продано:', self.line_add_sell)

        self.main_layout.addLayout(self.form_layout)
        self. main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)


class EditSellBatch(BaseDialog):
    def __init__(self, title, func, oper=None):
        super().__init__()
        self.setWindowTitle(f'Изменение {title}')
        self.validator = int_valid()
        self.line_add_id = QLineEdit()
        self.line_add_name = QLineEdit()
        self.line_add_money = QLineEdit()
        self.operation = oper

        art, desc, money = func
        self.line_add_id.setText(str(art))
        self.line_add_id.setReadOnly(True)
        self.line_add_name.setText(str(desc))
        if self.operation == 1:
            self.line_add_name.setReadOnly(True)
        self.line_add_money.setText(str(money))
        self.line_add_money.setValidator(self.validator)

        self.form_layout.addRow('Артикул:', self.line_add_id)
        self.form_layout.addRow('Наименование:', self.line_add_name)
        self.form_layout.addRow('Количество/Сумма:', self.line_add_money)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)
