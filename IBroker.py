from MarketException import MarketException


class UnknownTickerException(MarketException):
    def __init__(self, ticker_name):
        super().__init__('Unknown ticker: ' + ticker_name)


class NoDataException(MarketException):
    def __init__(self, ticker_name):
        super().__init__('No data for ticker: ' + ticker_name)


class IBroker:
    def __init__(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def get_last_price(self, ticker):
        pass

    def get_buy_price(self, ticker):
        pass

    def get_sell_price(self, ticker):
        pass

    def get_price_step(self, ticker):
        pass

    def send_buy_order(self, ticker, quantity, price):
        pass

    def send_sell_order(self, ticker, quantity, price):
        pass

    def cancel_order(self, id):
        pass

    def get_ticker_list(self):
        pass

    def get_buy_col(self, ticker):
        pass

    def get_sell_col(self, ticker):
        pass