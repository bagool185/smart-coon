from nltk.sem import Expression
from nltk.inference import ResolutionProverCommand
import pandas


class LogicProcessingUtil:

    def __init__(self, knowledge_base_doc: str):
        self.knowledge_base_doc = knowledge_base_doc
        self.knowledge_base = []
        self.__initialise_knowledge_base()

    def __initialise_knowledge_base(self):
        try:
            data = pandas.read_csv(self.knowledge_base_doc, header=None)
            [self.knowledge_base.append(self.__read_expression(row)) for row in data[0]]
        except pandas.errors.EmptyDataError:
            print('Missing knowledge base file')

    @staticmethod
    def __read_expression(expression: str) -> Expression:
        return Expression.fromstring(expression)

    def add_expression_to_knowledge_base(self, subject: str, obj: str) -> bool:

        expression = self.__read_expression(f'{subject}({obj})')
        self.knowledge_base.append(expression)

        return True

    def is_valid_expression(self, subject: str, obj: str) -> bool:
        expression = self.__read_expression(f'{subject}({obj})')

        answer = ResolutionProverCommand(expression, self.knowledge_base).prove()
        return answer
