import aiml
import wikipedia
import pandas as pd
import yfinance as yf

from lib.logic_processing import LogicProcessingUtil
from lib.utils import *
from .translation_util import TranslationUtil


class AIMLProcessingUtil:

    def __init__(self, aiml_file: str, knowledge_base_doc: str, translation_util: TranslationUtil):
        self.translation_util = translation_util
        self.aiml_kernel = aiml.Kernel()
        self.aiml_kernel.setTextEncoding(None)
        self.aiml_kernel.bootstrap(learnFiles=aiml_file)
        self.logic_processing_util = LogicProcessingUtil(knowledge_base_doc=knowledge_base_doc)
        self.language = 'en'

    def set_language(self, language: str):
        self.language = language

    def __print(self, message: str):
        if self.language != 'en':
            translated_message = self.translation_util.translate_text(source_text=message, from_lang='en',
                                                                      to_lang=self.language)
            print(translated_message)
        else:
            print(message)

    def __print_historical_market_data(self, stock_symbol: str):
        if validate_stock_symbol(stock_symbol) is False:
            return

        try:
            base_dir = ""
            filename = os.path.join(base_dir, f"{stock_symbol}-market-history.csv")
            historical_market_data: pd.DataFrame = yf.Ticker(stock_symbol.upper()).history()

            with open(filename, 'w') as market_history_file:
                market_history_file.write(historical_market_data.to_csv())
                self.__print(f"Successfully saved the past 5 years market history for {stock_symbol} in {filename}")
        except:
            self.__print("I'm afraid I couldn't process your query. Please make sure the stock symbol is right.")

    def __print_stock_info(self, stock_symbol: str):
        if validate_stock_symbol(stock_symbol) is False:
            return

        try:
            self.__print(yf.Ticker(stock_symbol.upper()).info)
        except:
            self.__print("I'm afraid I couldn't process your query. Please make sure the stock symbol is right.")

    def __print_wiki_summary(self, search_term: str):
        try:
            self.__print(wikipedia.summary(search_term, sentences=3, auto_suggest=False))
        except wikipedia.exceptions.DisambiguationError:
            self.__print("There were too many results for your query. Please be more explicit")
        except Exception:
            self.__print("I'm afraid I couldn't process your query. Please try rephrasing it.")

    def respond(self, user_input: str):
        return self.aiml_kernel.respond(user_input)

    def post_process_answer(self, answer: str):
        params = answer[1:].split('$')
        option = int(params[0])

        if option == CommandOption.EXIT:
            self.__print(params[1])
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
                self.__print(f'I now know that {obj} is {subject}')
            else:
                self.__print('This contradicts what I know.')

        elif option == CommandOption.LOGIC_INPUT_CHECK:
            obj, subject = params[1].split(' is ')
            is_valid_expression = self.logic_processing_util.is_valid_expression(subject, obj)

            if is_valid_expression:
                self.__print('That is correct')
            else:
                self.__print("I don't know")

        elif option == CommandOption.RETRY:
            self.__print("I did not get that, please try rephrasing.")
