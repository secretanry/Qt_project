import ISQLLogger
import MarketException
import mysql.connector
from mysql.connector import errorcode


class DatabaseIsNotExist(MarketException.MarketException):
    pass


class MySqlLogger(ISQLLogger.ISqlLogger):
    def __init__(self, adress, name, login, password):
        self.adress = adress
        self.name = name
        self.login = login
        self.password = password

    def connect(self):
        try:
            self.connection = mysql.connector.connect(user=self.login, password=self.password, host=self.adress,
                                                      database=self.name)
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                raise DatabaseIsNotExist('No database ' + self.name)
        except Exception:
            raise ISQLLogger.SqlException("Can't connect to a database")

    def disconnect(self):
        try:
            self.connection.close()
        except Exception:
            raise ISQLLogger.SqlException("Error disconnecting from a database")

    def create_database(self):
        try:
            connection = mysql.connector.connect(user=self.login, password=self.password, host=self.adress)
            cursor = connection.cursor()
            cursor.execute('create database {};'.format(self.name))
            cursor.execute('use {};'.format(self.name))
            cursor.execute(
                'create table prices(ticker varchar(5) not null, buy_price float, buy_col int, sell_price float, '
                'sell_col int, cur_time datetime(2) not null);')
            connection.close()
        except Exception as err:
            raise ISQLLogger.SqlException(err)

    def is_database_exist(self):
        try:
            connection = mysql.connector.connect(user=self.login, password=self.password, host=self.adress,
                                                 database=self.name)
            connection.close()
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                return False
        except Exception as err:
            raise ISQLLogger.SqlException(err)


def insert_row(self, ticker, buy_price, buy_col, sell_price, sell_col, cur_time):
    try:
        cur_time = '"' + str(cur_time) + '"'
        ticker = '"' + ticker + '"'
        st = "insert into {} values (".format('prices') + ticker + ", " + str(buy_price) + ", " + \
             str(buy_col) + ", " + str(sell_price) + ", " + str(sell_col) + ", " + cur_time + ");"
        self.cursor.execute(st)
        self.connection.commit()
    except Exception as err:
        raise ISQLLogger.SqlException(err)
