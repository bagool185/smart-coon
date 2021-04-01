import aiml
import wikipedia
import pandas as pd
import yfinance as yf

from lib.logic_processing import LogicProcessingUtil
from lib.utils import *


class AIMLProcessingUtil:

    def __init__(self, aiml_file: str, knowledge_base_doc: str):
        self.aiml_kernel = aiml.Kernel()
        self.aiml_kernel.setTextEncoding(None)
        self.aiml_kernel.bootstrap(learnFiles=aiml_file)
        self.logic_processing_util = LogicProcessingUtil(knowledge_base_doc=knowledge_base_doc)

    @staticmethod
    def __print_historical_market_data(stock_symbol: str):
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

    @staticmethod
    def __print_stock_info(stock_symbol: str):
        if validate_stock_symbol(stock_symbol) is False:
            return

        try:
            print(yf.Ticker(stock_symbol.upper()).info)
        except:
            print("I'm afraid I couldn't process your query. Please make sure the stock symbol is right.")

    @staticmethod
    def __print_wiki_summary(search_term: str):
        try:
            print(wikipedia.summary(search_term, sentences=3, auto_suggest=False))
        except wikipedia.exceptions.DisambiguationError:
            print("There were too many results for your query. Please be more explicit")
        except Exception:
            print("I'm afraid I couldn't process your query. Please try rephrasing it.")

    def respond(self, input: str):
        return self.aiml_kernel.respond(input)

    def post_process_answer(self, answer: str):
        params = answer[1:].split('$')
        option = int(params[0])

        if option == CommandOption.EXIT:
            print(params[1])
            exit(0)

        elif option == CommandOption.WIKI:
            self.__print_wiki_summary(search_term=params[1])

        elif option == CommandOption.STOCK_DATA:
            self.__print_stock_info(stock_symbol=params[1])

        elif option == CommandOption.STOCK_HISTORY:
            self.__print_historical_market_data(stock_symbol=params[1])

        elif option == CommandOption.LOGIC_INPUT_ADD:
            obj, subject = params[1].split(' is ')
            is_valid_expression = self.logic_processing_util.add_expression_to_knowledge_base(subject, obj)

            if is_valid_expression:
                print(f'I now know that {obj} is {subject}')
            else:
                print('This contradicts what I know.')

        elif option == CommandOption.LOGIC_INPUT_CHECK:
            obj, subject = params[1].split(' is ')
            is_valid_expression = self.logic_processing_util.is_valid_expression(subject, obj)

            if is_valid_expression:
                print('That is correct')
            else:
                print("I don't know")

        elif option == CommandOption.RETRY:
            print(" I did not get that, please try rephrasing.")
