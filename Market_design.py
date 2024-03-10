import sys
import TinkoffBroker
import IBroker
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
import MySqlLogger
import ISQLLogger
import BrokerDataFetcher
import mysql.connector


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class MarketDesign(QMainWindow):
    def __init__(self):
        super().__init__()
        self.list_of_tickers = []
        uic.loadUi('C:\\Users\\secre\\PycharmProjects\\pyQT_project\\Market_design.ui', self)
        self.pixmap = QPixmap('C:\\Users\\secre\\PycharmProjects\\pyQT_project\\orig.jpg')
        self.label_11.setPixmap(self.pixmap)
        self.token = 't.EeFiYgDPE06eom3C2Y1Lsi3M3PROj4vdbncuvzfXtxiuqNDwsmD3sUCaf7O76jB8-6-7YK4HNFQLyDHM_8rTNg'
        self.broker = TinkoffBroker.TinkoffBroker(self.token)
        self.fetcher = BrokerDataFetcher.BrokerDataFetcher(self.broker, 1, self.add_to_database)
        self.lineEdit.textChanged.connect(self.filter)
        self.pushButton.clicked.connect(self.on_connect)
        self.listWidget.itemClicked.connect(self.get_params_by_ticker)
        self.pushButton_2.clicked.connect(self.connect_to_database)
        self.pushButton_3.clicked.connect(self.start)
        self.pushButton_4.clicked.connect(self.stop)

    def filter(self):
        beg_of_ticker = self.lineEdit.text()
        list_of_tickers = self.broker.get_ticker_list()
        self.listWidget.clear()
        for i in list_of_tickers:
            if i[:len(beg_of_ticker)] == beg_of_ticker:
                self.listWidget.addItem(i)

    def on_connect(self):
        self.pushButton.setEnabled(False)
        self.lineEdit.setEnabled(True)
        self.broker.connect()
        self.listWidget.clear()
        self.listWidget.addItems(self.broker.get_ticker_list())

    def get_params_by_ticker(self):
        try:
            ticker = self.listWidget.selectedItems()[0].text()
            self.label_3.setText('Последняя цена: ' + str(self.broker.get_last_price(ticker)))
            self.label_4.setText('Цена покупки: ' + str(self.broker.get_buy_price(ticker)))
            self.label_5.setText('Цена продажи: ' + str(self.broker.get_sell_price(ticker)))
            self.label_6.setText('Шаг цены: ' + str(self.broker.get_price_step(ticker)))
        except IBroker.NoDataException:
            self.label_3.setText('Последняя цена: нет информации')
            self.label_4.setText('Цена покупки: нет информации')
            self.label_5.setText('Цена продажи: нет информации')
            self.label_6.setText('Шаг цены: нет информации')

    def connect_to_database(self):
        try:
            self.pushButton_3.setEnabled(True)
            self.pushButton_2.setEnabled(False)
            self.sql = MySqlLogger.MySqlLogger(self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(),
                                               self.lineEdit_5.text())
            if not self.sql.is_database_exist():
                self.sql.create_database()
            self.sql.connect()
        except Exception:
            self.label_13.setText('Cant connect to database')

    def add_to_database(self, ticker, buy_price, buy_col, sell_price, sell_col, cur_time):
        try:
            self.sql.insert_row(ticker, buy_price, buy_col, sell_price, sell_col, cur_time)
        except AttributeError:
            self.fetcher.stop()
        except ISQLLogger.SqlException:
            pass
        except Exception as err:
            print(err, ticker)

    def start(self):
        try:
            ticker = self.listWidget.selectedItems()[0].text()
            self.pushButton_4.setEnabled(True)
            if ticker not in self.list_of_tickers:
                self.list_of_tickers.append(ticker)
                self.fetcher.start(ticker)
                self.listWidget_2.addItem(ticker)
        except IndexError:
            pass

    def stop(self):
        try:
            ticker = self.listWidget_2.selectedItems()[0]
            if ticker.text() in self.list_of_tickers:
                self.list_of_tickers.remove(ticker.text())
                self.fetcher.stop(ticker.text())
                self.listWidget_2.takeItem(self.listWidget_2.row(ticker))
        except IndexError:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
try:
    ex = MarketDesign()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
except Exception as err:
    print(err)
