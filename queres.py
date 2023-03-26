CREATE_QUERES = {
    'create_table_nomenclature': '''CREATE TABLE IF NOT EXISTS goods (good_id integer primary key, good_n text,
                                buy_price integer, batch_id integer, buy integer, price integer,  
                                sell integer DEFAULT 0, balance integer AS (buy-sell) STORED,
                                pl_income integer AS (buy*price), FOREIGN KEY (batch_id) REFERENCES batch(batch_id))''',
    'create_table_batch': '''CREATE TABLE IF NOT EXISTS batch (batch_id integer primary key, 
                         batch_n text, costs integer DEFAULT 0)''',
    'create_table_oth_costs': '''CREATE TABLE IF NOT EXISTS other_costs (costs_id integer primary key,
                             cost_n text, costs integer DEFAULT 0)''',
    'create_table_income': '''CREATE TABLE IF NOT EXISTS income_table (income_id integer primary key, note_num integer,
                            good_id integer, income integer DEFAULT 0)''',
    'create_table_places': '''CREATE TABLE IF NOT EXISTS places (place_id text, place_n integer DEFAULT 0)''',
    'create_table_dellivery_notes': '''CREATE TABLE IF NOT EXISTS notes (note_num integer primary key, place_n text)''', #, FOREIGN KEY (note_num) REFERENCES pre_sell(note_num)
    'create_table_pre_sell': '''CREATE TABLE IF NOT EXISTS pre_sell (s_id int primary key, note_num integer, good_id int, sell_price int,
                                value int, discount int DEFAULT 0, FOREIGN KEY (note_num) REFERENCES notes(note_num))''', #, FOREIGN KEY (note_num) REFERENCES notes(note_num)
}

ADD_QUERES = {
    'add_good': '''INSERT INTO goods(good_n, buy_price, batch_id, buy, price) VALUES (?,?,?,?,?)''',
    'add_batch': '''INSERT INTO batch(batch_n) VALUES (?)''',
    'add_pre_sell': '''INSERT INTO pre_sell(note_num, good_id, sell_price, value, discount)
                        VALUES (?,?,?,?,?)''',
    'add_deliv_note': '''INSERT INTO notes(note_num, place_n) VALUES (?,?)''',
    'add_sell': '''UPDATE goods SET sell = sell + (?) WHERE good_id = (?)''',
    'add_oth_cost': '''INSERT INTO other_costs(cost_n, costs) VALUES (?, ?)''',
    'add_batch_cost': '''UPDATE batch SET costs = costs + (?) WHERE batch_id = (?)''',
    'add_income': '''INSERT INTO income_table(note_num, good_id, income) VALUES(?,?,?)''',
    'add_place_stat': '''UPDATE places SET place_n = place_n + (?) WHERE place_id = (?)''',
    # 'add_places_name': '''INSERT INTO places(place_id) VALUES(?)'''
}

DELETE_QUERES = {
    'delete_good': '''DELETE FROM goods WHERE good_id = (?)''',
    'delete_oth_cost': '''DELETE FROM other_costs WHERE costs_id = (?)''',
    'delete_pre_sell': '''DELETE FROM pre_sell WHERE note_num = (?)''',
    'delete_note': '''DELETE FROM notes WHERE note_num = (?)''',
    'delete_oth_sum': '''DELETE FROM other_costs WHERE cost_n = (?)''',
    'delete_batch_sum': '''DELETE FROM batch WHERE batch_n = (?)''',
    'delete_0_balance': '''DELETE FROM goods WHERE balance = (?)'''
}

UPDATE_QUERES = {
    # 'update_sell': '''UPDATE goods SET sell = (?) WHERE good_id = (?)''',
    'update_batch': '''UPDATE batch SET costs = costs - (?) WHERE batch_id = (?)''',
    # 'update_oth_cost': '''UPDATE other_costs SET cost_n = (?), costs = (?) WHERE costs_id = (?)''',
    'update_good': '''UPDATE goods SET good_n = (?), buy_price = (?), buy = (?), price = (?)
                  WHERE good_id=(?)'''
}


QUERY_PATHES = {
    'get_pre_sell': '''SELECT good_id, sell_price, value, discount FROM pre_sell WHERE note_num = (?)''',
    'pre_sell': '''SELECT pre_sell.note_num, pre_sell.good_id, pre_sell.value, pre_sell.discount, notes.place_n
                FROM pre_sell, notes WHERE pre_sell.note_num = notes.note_num''',
    'general_balance': '''SELECT goods.good_id, goods.good_n, goods.buy_price, batch.batch_n, goods.buy,
                       goods.price, goods.sell, goods.balance FROM goods JOIN batch WHERE goods.batch_id=batch.batch_id
                       UNION
                       SELECT 'Итого' AS good_id, '' AS good_n, '' AS buy_price, '' AS batch_n, SUM(buy) AS buy, '' AS price,
                              SUM(sell) AS sell, SUM(balance) AS balance FROM goods ORDER BY good_id''',
    'other_costs': '''SELECT 'Итого' AS costs_id, '' AS cost_n,SUM(costs) AS costs FROM other_costs ORDER BY costs_id''',
    'batches': '''SELECT * FROM batch
                  UNION
                  SELECT 'Итого' AS batch_id, '' AS batch_n,SUM(costs) AS costs FROM batch ORDER BY batch_id''',
    'batch_balance': '''SELECT goods.good_id, goods.good_n, goods.buy_price, batch.batch_n, goods.buy,
                        goods.price, goods.sell, goods.balance, goods.pl_income FROM goods 
                        JOIN batch WHERE goods.batch_id=batch.batch_id AND goods.batch_id=(?)
                        UNION
                        SELECT 'Итого' AS good_id, '' AS good_n, '' AS buy_price, '' AS batch_id, SUM(buy) AS buy, ''
                        AS price, SUM(sell) AS sell, SUM(balance) AS balance, SUM(pl_income) AS pl_income
                        FROM goods WHERE batch_id=(?) ORDER BY good_id ''',
    'plan_fin_res': '''SELECT good_id, good_n, buy, price, pl_income FROM goods WHERE batch_id=(?)
                       UNION
                       SELECT 'Плановая прибыль' AS good_id, '' AS good_n, '' AS buy, '' AS price,
                       (SUM(goods.pl_income) - batch.costs) AS pl_income 
                       FROM goods, batch WHERE  goods.batch_id=(?) AND batch.batch_id=(?)  ORDER BY good_id''',

    'get_good_id': '''SELECT good_id FROM goods''',
    'get_batch_id': '''SELECT batch_id FROM batch''',
    'get_batch_id_by_name': '''SELECT batch_id FROM batch WHERE batch_n=(?)''',
    'get_oth_costs_id': '''SELECT costs_id FROM other_costs''',
    'get_batch_names': '''SELECT batch_n FROM batch''',
    # 'get_pre_sell_id': '''SELECT note_num FROM pre_sell''',
    'get_current_oth_costs': '''SELECT costs_id, cost_n, costs FROM other_costs WHERE costs_id=(?)''',
    'get_current_batch': '''SELECT batch_id, batch_n, costs FROM batch WHERE batch_id=(?)''',
    'get_current_sell': '''SELECT good_id, good_n, sell FROM goods WHERE good_id=(?)''',
    'get_current_good': '''SELECT goods.good_id, goods.good_n, goods.buy_price, batch.batch_n, goods.buy, goods.price
                        FROM goods JOIN batch WHERE goods.batch_id=batch.batch_id AND good_id=(?)''',
    'get_buy_price': '''SELECT batch_id FROM goods ORDER BY good_id DESC LIMIT 1''',
    'get_place_names': '''SELECT place_id FROM places''',
    'get_place_names_note': '''SELECT place_n FROM notes WHERE note_num = (?)''',
    'get_note_num': '''SELECT note_num FROM notes''',
    'get_good_bp_bn': '''SELECT buy_price, batch_id, buy FROM goods WHERE good_id = (?)''',


    # 'total_income': '''SELECT sum(price * sell) FROM goods''',
    # 'income_by_batch': '''SELECT sum(price * sell) FROM goods WHERE batch_id=(?)''',
    # 'cost_by_batch': '''SELECT sum(costs) FROM batch WHERE batch_n=(?)''',
    # 'total_batch_costs': '''SELECT sum(costs) FROM batch''',
    # 'total_oth_costs': '''SELECT sum(costs) FROM other_costs ''',

    'get_total_batch': '''SELECT batch_n, costs FROM batch
                         UNION SELECT 'Сумма закупки товара' AS batch_n, SUM(costs) AS costs FROM batch ORDER BY costs''',
    'get_tot_oth_costs': '''SELECT 'Всего прочих затрат' AS cost_n, SUM(costs) AS costs FROM other_costs''',
    'get_total_income': '''SELECT 'Всего доход' AS good_id, SUM(income) AS income FROM income_table'''
}
