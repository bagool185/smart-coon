import wikipedia
import pandas as pd
import os
import yfinance as yf
from lib.utils import *


def print_historical_market_data(stock_symbol: str):

    if validate_stock_symbol(stock_symbol) is False:
        return

    try:
        base_dir = ""
        filename = os.path.join(base_dir, f"{stock_symbol}-market-history.csv")
        historical_market_data: pd.DataFrame = yf.Ticker(stock_symbol.upper()).history()

        with open(filename, 'w') as market_history_file:
            market_history_file.write(historical_market_data.to_csv())
            print(f"Successfully saved the past 5 years market history for {stock_symbol} in {filename}")

    except:
        print("I'm afraid I couldn't process your query. Please make sure the stock symbol is right.")


def print_stock_info(stock_symbol: str):

    if validate_stock_symbol(stock_symbol) is False:
        return

    try:
        print(yf.Ticker(stock_symbol.upper()).info)
    except:
        print("I'm afraid I couldn't process your query. Please make sure the stock symbol is right.")


def get_user_input() -> str or None:
    try:
        return input("> ")
    except (KeyboardInterrupt, EOFError):
        print("Quitting")
        return None


def print_wiki_summary(search_term: str):
    try:
        print(wikipedia.summary(search_term, sentences=3, auto_suggest=False))
    except wikipedia.exceptions.DisambiguationError:
        print("There were too many results for your query. Please be more explicit")
    except Exception:
        print("I'm afraid I couldn't process your query. Please try rephrasing it.")


def post_process_answer(answer: str):

    params = answer[1:].split('$')
    option = int(params[0])

    if option == CommandOption.EXIT:
        print(params[1])
        exit(0)

    elif option == CommandOption.WIKI:
        print_wiki_summary(search_term=params[1])

    elif option == CommandOption.STOCK_DATA:
        print_stock_info(stock_symbol=params[1])

    elif option == CommandOption.STOCK_HISTORY:
        print_historical_market_data(stock_symbol=params[1])

    elif option == CommandOption.RETRY:
        print(" I did not get that, please try rephrasing.")
