import sqlite3

#from queres import QUERY_PATHES, CREATE_QUERES, ADD_QUERES, UPDATE_QUERES, DELETE_QUERES
from queres import CREATE_QUERES, QUERY_PATHES


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('shop.db')
        # self.conn.execute('''PRAGMA foreign_keys = ON''')
        self.c = self.conn.cursor()
        self.c.execute(CREATE_QUERES['create_table_batch'])
        self.c.execute(CREATE_QUERES['create_table_oth_costs'])
        self.c.execute(CREATE_QUERES['create_table_nomenclature'])
        self.c.execute(CREATE_QUERES['create_table_pre_sell'])
        self.c.execute(CREATE_QUERES['create_table_income'])
        self.c.execute(CREATE_QUERES['create_table_places'])
        self.c.execute(CREATE_QUERES['create_table_dellivery_notes'])
        self.conn.commit()

    def ins_del_upd_data(self, query, data):
        self.c.execute(query, data)
        self.conn.commit()
        return

    # def get_batch_profit(self):
    #     result = []
    #     batches_list = self.get_data(QUERY_PATHES['get_batch_names'])
    #     for batch in batches_list:
    #         income = self.c.execute(QUERY_PATHES['income_by_batch'], (batch,)).fetchall()
    #         costs = self.c.execute(QUERY_PATHES['cost_by_batch'], (batch,)).fetchall()
    #         tuple_profit = (batch, (income[0][0] - costs[0][0]))
    #         result.append(tuple_profit)
    #     return result

    # def get_total_profit(self):
    #     income = self.c.execute(QUERY_PATHES['total_income']).fetchall()
    #     batch_costs = self.c.execute(QUERY_PATHES['total_batch_costs']).fetchall()
    #     oth_cost = self.c.execute(QUERY_PATHES['total_oth_costs']).fetchall()
    #     result = income[0][0] - batch_costs[0][0] - oth_cost[0][0]
    #     return result
    #
    # def get_sum_oth_costs(self):
    #     oth_cost = self.c.execute(QUERY_PATHES['total_oth_costs']).fetchall()
    #     return oth_cost[0][0]

    def get_current_data_by_id(self, query, art):
        result = []
        query_data = self.c.execute(query, (art,)).fetchall()
        for data in query_data:
            for element in data:
                result.append(element)
        return result

    def get_data(self, query):
        query_tuple = self.c.execute(query).fetchall()
        res_list = [data[0] for data in query_tuple]
        return res_list

    def get_id(self, quere, data):
        result = self.c.execute(quere, (data,)).fetchall()
        return result[0][0]

    def get_data_2(self, query):
        query_tuple = self.c.execute(query).fetchall()
        return query_tuple[0][0]

    def get_pre_sell(self, query, data):
        quere_tuple = self.c.execute(query, (data,)).fetchall()
        return quere_tuple

    def get_data_3(self, query):
        query_tuple = self.c.execute(query).fetchall()
        return query_tuple

    def get_batch_profit(self):
        batches_list = self.get_data_3(QUERY_PATHES['get_total_batch'])
        return batches_list

    def get_total_profit(self):
        batches_list = self.get_data_3(QUERY_PATHES['get_total_income'])
        return batches_list

    def get_sum_oth_costs(self):
        batches_list = self.get_data_3(QUERY_PATHES['get_tot_oth_costs'])
        return batches_list