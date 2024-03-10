import IDataFetcher
import MarketException
import mysql.connector
from mysql.connector import errorcode


class MySqlFetcher(IDataFetcher.IDataFetcher):
    def __init__(self, adress, name, login, password, callback):
        self.adress = adress
        self.name = name
        self.login = login
        self.password = password
        self.callback = callback

    def connect(self):
        try:
            self.connection = mysql.connector.connect(user=self.login, password=self.password, host=self.adress,
                                                      database=self.name)
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                raise MarketException.MarketException('No database ' + self.name)
        except Exception:
            raise MarketException.MarketException("Can't connect to a database")

    def disconnect(self):
        try:
            self.connection.close()
        except Exception:
            raise MarketException.MarketException("Error disconnecting from a database")

    def start(self, ticker):
        try:
            if self.callback:
                self.cursor.execute("SELECT * FROM prices where ticker = '" + ticker + "'")
                myresult = self.cursor.fetchall()
                for x in myresult:
                    self.callback(x[0], x[1], x[2], x[3], x[4], x[5])
        except Exception as err:
            raise MarketException.MarketException(err)

    def stop(self, ticker):
        pass
