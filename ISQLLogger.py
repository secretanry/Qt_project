class SqlException(Exception):
    pass

class ISqlLogger:
    def __init__(self, adress, name, login, password):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def insert_row(self, ticker, buy_price, buy_col, sell_price, sell_col, cur_time):
        pass

    def is_database_exist(self):
        pass

    def create_database(self):
        pass

