import sqlite3

from queres import CREATE_QUERES, QUERY_PATHES


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('shop.db')
        self.conn.execute('''PRAGMA foreign_keys = ON''')
        self.c = self.conn.cursor()
        self.c.execute(CREATE_QUERES['create_table_batch'])
        self.c.execute(CREATE_QUERES['create_table_oth_costs'])
        self.c.execute(CREATE_QUERES['create_table_nomenclature'])
        self.c.execute(CREATE_QUERES['create_table_dellivery_notes'])
        self.c.execute(CREATE_QUERES['create_table_pre_sell'])
        self.c.execute(CREATE_QUERES['create_table_income'])
        self.c.execute(CREATE_QUERES['create_table_places'])
        self.conn.commit()

    def ins_del_upd_data(self, query, data):
        self.c.execute(query, data)
        self.conn.commit()
        return

    def get_data_list(self, query):
        query_tuple = self.c.execute(query).fetchall()
        res_list = [data[0] for data in query_tuple]
        return res_list

    def get_data_with_param(self, query, data):
        quere_tuple = self.c.execute(query, (data,)).fetchall()
        return quere_tuple

    def get_data_without_param(self, query):
        query_tuple = self.c.execute(query).fetchall()
        return query_tuple

    def get_batch_profit(self):
        batches_list = self.get_data_without_param(QUERY_PATHES['get_total_batch'])
        return batches_list

    def get_total_profit(self):
        result = self.get_data_without_param(QUERY_PATHES['get_total_income'])
        return result

    def get_sum_oth_costs(self):
        result = self.get_data_without_param(QUERY_PATHES['get_tot_oth_costs'])
        return result
