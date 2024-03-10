class MarketException(Exception):
    def __init__(self, error):
        self.error = error

    def get_error(self):
        return self.error

