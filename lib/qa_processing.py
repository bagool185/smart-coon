from typing import List
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class QAProcessingUtil:

    def __init__(self, data_file: str):
        self.questions_source = data_file
        self.questions_limit = 10
        self.__parse_questions()

    def __parse_questions(self):
        self.qa_data_frame: pd.DataFrame = pd.read_csv(self.questions_source, header=None, delimiter='~')[:self.questions_limit].head()

        self.questions: List[str] = list(self.qa_data_frame.iloc[:, 0])

    def get_closest_matching_answer(self, text_to_compare: str) -> str or None:
        count_vectoriser = CountVectorizer(stop_words='english')

        index = 0

        for question in self.questions:
            corpus = [text_to_compare, question]

            matrix = count_vectoriser.fit_transform(corpus)

            data_frame = pd.DataFrame(matrix.todense(), columns=count_vectoriser.get_feature_names(), index=corpus)

            similarity = cosine_similarity(data_frame, data_frame)

            if np.all((similarity >= 0.5)):
                return self.qa_data_frame.iloc[index, 1]

            index += 1

        return None
