class CandleHelpers():
    @staticmethod
    def is_green(data):
        return data['close'] > data['open']

    def is_red(data):
        return data['open'] > data['close']

    def is_indecision(data):
        if abs(data['high'] - data['low']) / 2 >= abs(data['close'] - data['open']):
            return True
        return False
