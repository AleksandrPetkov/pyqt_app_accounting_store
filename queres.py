CREATE_QUERES = {
    'create_table_nomenclature': '''CREATE TABLE IF NOT EXISTS goods (good_id integer primary key, good_n text,
                                buy_price integer, batch_id integer, buy integer, price integer,  
                                sell integer DEFAULT 0, balance integer AS (buy-sell) STORED,
                                pl_income integer AS (buy*price), FOREIGN KEY (batch_id) REFERENCES batch(batch_id))''',
    'create_size_table': '''CREATE TABLE IF NOT EXISTS size (good_id int, good_n text, first int DEFAULT 0,
                            second int DEFAULT 0, third int DEFAULT 0, fourth int DEFAULT 0, fifth int DEFAULT 0,
                            sixth int DEFAULT 0, seventh int DEFAULT 0, eighth int DEFAULT 0,
                            FOREIGN KEY (good_id) REFERENCES goods(good_id) ON DELETE CASCADE)''',
    'create_table_batch': '''CREATE TABLE IF NOT EXISTS batch (batch_id integer primary key, 
                         batch_n text, costs integer DEFAULT 0)''',
    'create_table_oth_costs': '''CREATE TABLE IF NOT EXISTS other_costs (costs_id integer primary key,
                             cost_n text, costs integer DEFAULT 0)''',
    'create_table_income': '''CREATE TABLE IF NOT EXISTS income_table (note_num integer,
                              good_id integer, good_n text, size text, buy_p int, sell_p int, order_value int,
                              discount int, cash int AS (sell_p*order_value-discount), income int AS (cash - buy_p*order_value), date text)''',
    'create_table_places': '''CREATE TABLE IF NOT EXISTS places (place_id text, place_n integer DEFAULT 0)''',
    'create_table_pre_sell': '''CREATE TABLE IF NOT EXISTS pre_sell (note_num integer, good_id int, sell_price int,
                                value int, discount int DEFAULT 0, size int, date text)''',
    'create_table_dellivery_notes': '''CREATE TABLE IF NOT EXISTS notes (note_num integer, place_n text)''',
}

ADD_QUERES = {
    'add_good': '''INSERT INTO goods(good_n, buy_price, batch_id, buy, price) VALUES (?,?,?,?,?)''',
    'add_batch': '''INSERT INTO batch(batch_n) VALUES (?)''',
    'add_pre_sell': '''INSERT INTO pre_sell(note_num, good_id, sell_price, value, discount, size, date)
                        VALUES (?,?,?,?,?,?,?)''',
    'add_deliv_note': '''INSERT INTO notes(note_num, place_n) VALUES (?,?)''',
    'add_sell': '''UPDATE goods SET sell = sell + (?) WHERE good_id = (?)''',
    'add_del_sell': '''UPDATE goods SET sell = sell - (?) WHERE good_id = (?)''',
    'add_oth_cost': '''INSERT INTO other_costs(cost_n, costs) VALUES (?, ?)''',
    'add_batch_cost': '''UPDATE batch SET costs = costs + (?) WHERE batch_id = (?)''',
    'add_income': '''INSERT INTO income_table(note_num, good_id, good_n, size, buy_p, sell_p,
                     order_value, discount, date) VALUES(?,?,?,?,?,?,?,?,?)''',
    'add_place_stat': '''UPDATE places SET place_n = place_n + (?) WHERE place_id = (?)''',
    'add_good_to_size': '''INSERT INTO size(good_id, good_n) VALUES (?,?)''',
    'add_size': '''UPDATE size SET first=first+(?), second=second + (?), third=third+(?), fourth=fourth+(?),
                   fifth=fifth+(?), sixth=sixth+(?), seventh=seventh+(?), eighth=eighth+(?) WHERE good_id=(?)''',
    'add_sell_place': '''INSERT INTO places(place_id) VALUES (?)'''
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
    'update_batch': '''UPDATE batch SET costs = costs - (?) WHERE batch_id = (?)''',
    'update_good': '''UPDATE goods SET good_n = (?), buy_price = (?), buy = (?), price = (?)
                  WHERE good_id=(?)''',
    'update_size': '''UPDATE size SET good_n = (?), first = (?), second = (?), third = (?), fourth = (?),
                      fifth = (?), sixth = (?), seventh = (?), eighth = (?) WHERE good_id=(?)''',

    'update_first_sell': '''UPDATE size SET first = first - (?) WHERE good_id = (?)''',
    'update_second_sell': '''UPDATE size SET second = second - (?) WHERE good_id = (?)''',
    'update_third_sell': '''UPDATE size SET third = third - (?) WHERE good_id = (?)''',
    'update_fourth_sell': '''UPDATE size SET fourth = fourth - (?) WHERE good_id = (?)''',
    'update_fifth_sell': '''UPDATE size SET fifth = fifth - (?) WHERE good_id = (?)''',
    'update_sixth_sell': '''UPDATE size SET sixth = sixth - (?) WHERE good_id = (?)''',
    'update_seventh_sell': '''UPDATE size SET seventh = seventh - (?) WHERE good_id = (?)''',
    'update_eighth_sell': '''UPDATE size SET eighth = eighth - (?) WHERE good_id = (?)''',

    'update_first_dellsell': '''UPDATE size SET first = first + (?) WHERE good_id = (?)''',
    'update_second_dellsell': '''UPDATE size SET second = second + (?) WHERE good_id = (?)''',
    'update_third_dellsell': '''UPDATE size SET third = third + (?) WHERE good_id = (?)''',
    'update_fourth_dellsell': '''UPDATE size SET fourth = fourth + (?) WHERE good_id = (?)''',
    'update_fifth_dellsell': '''UPDATE size SET fifth = fifth + (?) WHERE good_id = (?)''',
    'update_sixth_dellsell': '''UPDATE size SET sixth = sixth + (?) WHERE good_id = (?)''',
    'update_seventh_dellsell': '''UPDATE size SET seventh = seventh + (?) WHERE good_id = (?)''',
    'update_eighth_dellsell': '''UPDATE size SET eighth = eighth + (?) WHERE good_id = (?)'''
}


QUERY_PATHES = {
    'get_pre_sell': '''SELECT good_id, sell_price, value, discount, size, date FROM pre_sell WHERE note_num = (?)''',
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
    'get_good_name': '''SELECT good_n FROM goods''',
    'get_last_good_id': '''SELECT good_id FROM goods ORDER BY good_id DESC LIMIT 1''',
    'get_batch_id': '''SELECT batch_id FROM batch''',
    'get_batch_id_by_name': '''SELECT batch_id FROM batch WHERE batch_n=(?)''',
    'get_oth_costs_id': '''SELECT costs_id FROM other_costs''',
    'get_batch_names': '''SELECT batch_n FROM batch''',
    'get_current_oth_costs': '''SELECT costs_id, cost_n, costs FROM other_costs WHERE costs_id=(?)''',
    'get_current_batch': '''SELECT batch_id, batch_n, costs FROM batch WHERE batch_id=(?)''',
    'get_current_sell': '''SELECT good_id, good_n, sell FROM goods WHERE good_id=(?)''',
    'get_current_good': '''SELECT goods.good_id, goods.good_n, goods.buy_price, batch.batch_n, goods.buy, goods.price
                        FROM goods JOIN batch WHERE goods.batch_id=batch.batch_id AND good_id=(?)''',
    'get_current_good_edit': '''SELECT goods.good_id, goods.good_n, goods.buy_price, batch.batch_n, goods.buy, goods.price, goods.balance
                    FROM goods JOIN batch WHERE goods.batch_id=batch.batch_id AND good_id=(?)''',
    'get_buy_price': '''SELECT batch_id FROM goods ORDER BY good_id DESC LIMIT 1''',
    'get_place_names': '''SELECT place_id FROM places''',
    'get_place_names_note': '''SELECT place_n FROM notes WHERE note_num = (?)''',
    'get_note_num': '''SELECT note_num FROM notes''',
    'get_good_bp_bn': '''SELECT buy_price, batch_id, buy FROM goods WHERE good_id = (?)''',
    'get_good_n_buy_p': '''SELECT good_n, buy_price FROM goods WHERE good_id = (?)''',
    'get_places': '''SELECT * FROM places''',
    'get_total_batch': '''SELECT batch_n, costs FROM batch
                         UNION SELECT 'Сумма закупки товара' AS batch_n, SUM(costs) AS costs FROM batch ORDER BY costs''',
    'get_tot_oth_costs': '''SELECT 'Всего прочих затрат' AS cost_n, SUM(costs) AS costs FROM other_costs''',
    'get_total_income': '''SELECT 'Всего доход' AS good_id, SUM(sell_p * order_value - discount)
                           AS income FROM income_table''',
    'get_size_info': '''SELECT good_id, value, size FROM pre_sell WHERE note_num = (?)''',
    'get_size_by_good': '''SELECT * FROM size WHERE good_id = (?)''',
    'get_income_by_date': '''SELECT note_num, good_id, good_n, size, buy_p, sell_p, order_value, discount, cash, 
                             income, date FROM income_table WHERE date BETWEEN (?) and (?)
                             UNION SELECT 'Сумма закупки товара' AS note_num, '' AS good_id, '' AS good_n,
                             '' AS size, '' AS buy_p, '' AS sell_p, '' AS order_value, '' AS discount, SUM(cash) AS cash,
                             SUM(income) AS income, '' AS date FROM income_table WHERE date BETWEEN (?) and (?) ORDER BY note_num''',

    'get_first': '''SELECT first FROM size WHERE good_id = (?)''',
    'get_second': '''SELECT second FROM size WHERE good_id = (?)''',
    'get_third': '''SELECT third FROM size WHERE good_id = (?)''',
    'get_fourth': '''SELECT fourth FROM size WHERE good_id = (?)''',
    'get_fifth': '''SELECT fifth FROM size WHERE good_id = (?)''',
    'get_sixth': '''SELECT sixth FROM size WHERE good_id = (?)''',
    'get_seventh': '''SELECT seventh FROM size WHERE good_id = (?)''',
    'get_eighth': '''SELECT  eighth FROM size WHERE good_id = (?)''',

    'get_good_balance': '''SELECT buy, balance FROM goods WHERE good_id=(?)'''
}
