from threading import Timer
import datetime
import IDataFetcher
import MarketException
import IBroker


class DataFetcherException(MarketException.MarketException):
    def __init__(self, error):
        super().__init__(error)


class BrokerDataFetcher(IDataFetcher.IDataFetcher):
    def __init__(self, broker, delay, callback):
        self.tickers = []
        self.broker = broker
        self.delay = delay
        self.callback = callback
        self.timer_enabled = False

    def timer_restart(self):
        if self.timer_enabled:
            self.timer = Timer(self.delay, self.on_timer)
            self.timer.start()

    def start(self, ticker):
        try:
            if len(self.tickers) == 0:
                self.timer_enabled = True
                self.timer_restart()
            assert ticker not in self.tickers
            if ticker not in self.tickers:
                self.tickers.append(ticker)
        except Exception:
            raise DataFetcherException('Cant start logging for ticker ' + ticker)

    def stop(self, ticker):
        try:
            assert ticker in self.tickers
            if ticker in self.tickers:
                self.tickers.remove(ticker)
            if len(self.tickers) == 0:
                self.timer_enabled = False
                self.timer.cancel()
        except Exception:
            raise DataFetcherException('Cant stop logging for ticker ' + ticker)

    def on_timer(self):
        for ticker in self.tickers:
            try:
                now = datetime.datetime.now()
                buy_price = self.broker.get_buy_price(ticker)
                buy_col = self.broker.get_buy_col(ticker)
                sell_price = self.broker.get_sell_price(ticker)
                sell_col = self.broker.get_sell_col(ticker)
                self.callback(ticker, buy_price, buy_col, sell_price, sell_col, now)
            except IBroker.NoDataException:
                pass
            except Exception:
                pass

        try:
            self.timer_restart()
        except Exception:
            raise DataFetcherException('Cant restart a timer')
