import sqlite3

QUERY_PATHES = {
    'create_table_nomenclature': '''CREATE TABLE IF NOT EXISTS nomenclature (id integer primary key, description text,
                                    batch_n text, buy integer, price integer, sell integer DEFAULT 0,
                                    balance integer AS (buy-sell), pl_income integer AS (buy*price))''',
    'create_table_batch': '''CREATE TABLE IF NOT EXISTS batch (id integer primary key, 
                             batch_n text, costs integer DEFAULT 0)''',
    'create_table_oth_costs': '''CREATE TABLE IF NOT EXISTS other_costs (id integer primary key,
                                 description text, costs integer DEFAULT 0)''',

    'nomenclature': '''SELECT id, description, batch_n FROM nomenclature''',
    'general_balance': '''SELECT id, description, batch_n, buy, price, sell, balance FROM nomenclature
                       UNION
                       SELECT 'Итого' AS id, '' AS description, '' AS batch_n, SUM(buy) AS buy, '' AS price,
                              SUM(sell) AS sell, SUM(balance) AS balance FROM nomenclature ORDER BY id''',
    'other_costs': '''SELECT * FROM other_costs
                      UNION
                      SELECT 'Итого' AS id, '' AS description,SUM(costs) AS costs FROM other_costs ORDER BY id''',
    'batches': '''SELECT * FROM batch
                  UNION
                  SELECT 'Итого' AS id, '' AS batch_n,SUM(costs) AS costs FROM batch ORDER BY id''',
    'batch_balance': '''SELECT id, description, batch_n, buy, price, sell, balance FROM nomenclature WHERE batch_n=(?)
                        UNION
                        SELECT 'Итого' AS id, '' AS description, batch_n, SUM(buy) AS buy, '' AS price, SUM(sell) 
                        AS sell, SUM(balance) AS balance FROM nomenclature WHERE batch_n=(?) ORDER BY id ''',
    'plan_fin_res': '''SELECT id, description, batch_n, buy, price, pl_income FROM nomenclature WHERE batch_n=(?)
                       UNION
                       SELECT 'Плановая прибыль' AS id, '' AS description, nomenclature.batch_n, '' AS buy, '' AS price,
                       (SUM(nomenclature.pl_income) - batch.costs) AS pl_income 
                       FROM nomenclature, batch WHERE  nomenclature.batch_n=(?) AND batch.batch_n=(?)  ORDER BY id ''',

    'delete_good': '''DELETE FROM nomenclature WHERE id = (?)''',
    'delete_oth_cost': '''DELETE FROM other_costs WHERE id = (?)''',
    'delete_sell': '''UPDATE nomenclature SET sell = (?) WHERE id = (?)''',

    'update_sell': '''UPDATE nomenclature SET sell = (?) WHERE id = (?)''',
    'update_batch': '''UPDATE batch SET costs = (?) WHERE id = (?)''',
    'update_oth_cost': '''UPDATE other_costs SET description = (?), costs = (?) WHERE id = (?)''',
    'update_good': '''UPDATE nomenclature SET description = (?), buy = (?), price = (?), sell = (?)
                      WHERE id=(?)''',

    'get_good_id': '''SELECT id FROM nomenclature''',
    'get_batch_id': '''SELECT id FROM batch''',
    'get_oth_costs_id': '''SELECT id FROM other_costs''',
    'get_batch_names': '''SELECT batch_n FROM batch''',
    'get_current_oth_costs': '''SELECT id, description, costs FROM other_costs WHERE id=(?)''',
    'get_current_batch': '''SELECT id, batch_n, costs FROM batch WHERE id=(?)''',
    'get_current_sell': '''SELECT id, description, sell FROM nomenclature WHERE id=(?)''',
    'get_current_good': '''SELECT id, description, batch_n, buy, price, sell FROM nomenclature WHERE id=(?)''',

    'add_good': '''INSERT INTO nomenclature(description, batch_n, buy, price) VALUES (?, ?, ?, ?)''',
    'add_batch': '''INSERT INTO batch(batch_n, costs) VALUES (?, ?)''',
    'add_sell': '''UPDATE nomenclature SET sell = sell + (?) WHERE id = (?)''',
    'add_oth_cost': '''INSERT INTO other_costs(description, costs) VALUES (?, ?)''',

    'total_income': '''SELECT sum(price * sell) FROM nomenclature''',
    'income_by_batch': '''SELECT sum(price * sell) FROM nomenclature WHERE batch_n=(?)''',
    'cost_by_batch': '''SELECT sum(costs) FROM batch WHERE batch_n=(?)''',
    'total_batch_costs': '''SELECT sum(costs) FROM batch''',
    'total_oth_costs': '''SELECT sum(costs) FROM other_costs ''',

}


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('shop.db')
        self.c = self.conn.cursor()
        self.c.execute(QUERY_PATHES['create_table_batch'])
        self.c.execute(QUERY_PATHES['create_table_oth_costs'])
        self.c.execute(QUERY_PATHES['create_table_nomenclature'])
        self.conn.commit()

    def insert_data(self, query, data):
        self.c.execute(query, data)
        self.conn.commit()
        return

    def get_batch_profit(self):
        result = []
        batches_list = self.get_data(QUERY_PATHES['get_batch_names'])
        for batch in batches_list:
            income = self.c.execute(QUERY_PATHES['income_by_batch'], (batch,)).fetchall()
            costs = self.c.execute(QUERY_PATHES['cost_by_batch'], (batch,)).fetchall()
            tuple_profit = (batch, (income[0][0] - costs[0][0]))
            result.append(tuple_profit)
        return result

    def get_total_profit(self):
        income = self.c.execute(QUERY_PATHES['total_income']).fetchall()
        batch_costs = self.c.execute(QUERY_PATHES['total_batch_costs']).fetchall()
        oth_cost = self.c.execute(QUERY_PATHES['total_oth_costs']).fetchall()
        result = income[0][0] - batch_costs[0][0] - oth_cost[0][0]
        return result

    def get_sum_oth_costs(self):
        oth_cost = self.c.execute(QUERY_PATHES['total_oth_costs']).fetchall()
        return oth_cost[0][0]

    def get_current_data_by_id(self, query, art):
        result = []
        query_data = self.c.execute(query, (art,)).fetchall()
        for data in query_data:
            for element in data:
                result.append(element)
        return result

    def get_data(self, query):
        id_tuples = self.c.execute(query).fetchall()
        id_list = [batch[0] for batch in id_tuples]
        return id_list

    def delete_update_data(self, query, values):
        self.c.execute(query, values)
        self.conn.commit()
        return
