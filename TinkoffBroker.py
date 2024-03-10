import openapi_genclient
from openapi_client import openapi
from MarketException import MarketException
import IBroker


class TinkoffBrokerException(MarketException):
    def __init__(self, error):
        super().__init__(error)


class TinkoffBroker(IBroker.IBroker):
    def __init__(self, token):
        assert(isinstance(token, str))
        self.token = token
        self.ticker_to_figi = {}
        self.ticker_to_increment = {}
        self.tickers = []

    def connect(self):
        try:
            self.client = openapi.sandbox_api_client(self.token)
            self.client.sandbox.sandbox_register_post()
            self.client.sandbox.sandbox_clear_post()
            self.set_balance()
            for i in self.client.market.market_stocks_get().payload.instruments:
                self.ticker_to_figi[i.ticker] = i.figi
                self.ticker_to_increment[i.ticker] = i.min_price_increment
                self.tickers.append(i.ticker)
        except openapi_genclient.exceptions.ApiException as err:
            raise TinkoffBrokerException(err)

    def disconnect(self):
        pass

    def send_buy_order(self, ticker, quantity, price):
        assert isinstance(ticker, str)
        assert self.client
        if ticker not in self.ticker_to_figi:
            raise IBroker.UnknownTickerException(ticker)
        try:
            order_response = self.client.orders.orders_limit_order_post(figi=self.ticker_to_figi[ticker],
                                                                        limit_order_request={"lots": quantity,
                                                                                             "operation": "Buy",
                                                                                             "price": price})
            return order_response.payload.order_id
        except openapi_genclient.exceptions.ApiException as err:
            raise TinkoffBrokerException(err)

    def send_sell_order(self, ticker, quantity, price):
        assert(isinstance(ticker, str))
        assert self.client
        if ticker not in self.ticker_to_figi:
            raise IBroker.UnknownTickerException(ticker)
        try:
            order_response = self.client.orders.orders_limit_order_post(figi=self.ticker_to_figi[ticker],
                                                                        limit_order_request={"lots": quantity,
                                                                                             "operation": "Sell",
                                                                                             "price": price})
            return order_response.payload.order_id
        except openapi_genclient.exceptions.ApiException as err:
            raise TinkoffBrokerException(err)

    def cancel_order(self, id):
        assert self.client
        try:
            self.client.orders.orders_cancel_post(id)
        except openapi_genclient.exceptions.ApiException as err:
            raise TinkoffBrokerException(err)

    def set_balance(self):
        assert self.client
        try:
            balance_set = self.client.sandbox.sandbox_currencies_balance_post({"currency": "USD", "balance": 10000})
        except openapi_genclient.exceptions.ApiException as err:
            raise TinkoffBrokerException(err)

    def print_portfolio(self):
        assert self.client
        try:
            pf = self.client.portfolio.portfolio_get()
            print(pf)
        except openapi_genclient.exceptions.ApiException as err:
            raise TinkoffBrokerException(err)

    def get_last_price(self, ticker):
        assert self.client
        assert(isinstance(ticker, str))
        if ticker not in self.ticker_to_figi:
            raise IBroker.UnknownTickerException(ticker)
        try:
            return self.client.market.market_orderbook_get(self.ticker_to_figi[ticker], 0).payload.last_price
        except openapi_genclient.exceptions.ApiException as err:
            raise TinkoffBrokerException(err)

    def get_buy_price(self, ticker):
        assert self.client
        assert(isinstance(ticker, str))
        if ticker not in self.ticker_to_figi:
            raise IBroker.UnknownTickerException(ticker)
        try:
            orderbook = self.client.market.market_orderbook_get(self.ticker_to_figi[ticker], 1).payload
            if len(orderbook.asks) == 0:
                raise IBroker.NoDataException(ticker)
            return orderbook.asks[0].price
        except openapi_genclient.exceptions.ApiException as err:
            raise TinkoffBrokerException(err)

    def get_sell_price(self, ticker):
        assert self.client
        assert(isinstance(ticker, str))
        if ticker not in self.ticker_to_figi:
            raise IBroker.UnknownTickerException(ticker)
        try:
            return self.client.market.market_orderbook_get(self.ticker_to_figi[ticker], 1).payload.bids[0].price
        except openapi_genclient.exceptions.ApiException as err:
            raise TinkoffBrokerException(err)

    def get_price_step(self, ticker):
        assert self.client
        assert(isinstance(ticker, str))
        if ticker not in self.ticker_to_figi:
            raise IBroker.UnknownTickerException(ticker)
        try:
            return self.ticker_to_increment[ticker]
        except openapi_genclient.exceptions.ApiException as err:
            raise TinkoffBrokerException(err)

    def get_ticker_list(self):
        return self.tickers

    def get_buy_col(self, ticker):
        assert self.client
        assert(isinstance(ticker, str))
        try:
            return len(self.client.market.market_orderbook_get(self.ticker_to_figi[ticker], 1).payload.asks)
        except openapi_genclient.exceptions.ApiException as err:
            raise TinkoffBrokerException(err)

    def get_sell_col(self, ticker):
        assert self.client
        assert(isinstance(ticker, str))
        try:
            return len(self.client.market.market_orderbook_get(self.ticker_to_figi[ticker], 1).payload.bids)
        except openapi_genclient.exceptions.ApiException as err:
            raise TinkoffBrokerException(err)
