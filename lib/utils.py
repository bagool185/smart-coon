from enum import IntEnum


def validate_stock_symbol(stock_symbol: str) -> bool:

    if stock_symbol is None or stock_symbol == '':
        print("I need the symbol in order to fetch the historical market data")
        return False

    return True


class CommandOption(IntEnum):

    EXIT = 0
    WIKI = 1
    STOCK_DATA = 2
    STOCK_HISTORY = 3
    RETRY = 99
