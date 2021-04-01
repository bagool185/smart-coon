import os
import uuid
from decimal import Decimal
from typing import Dict, Optional

from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from azure.cognitiveservices.language.textanalytics.models import LanguageInput
from msrest.authentication import CognitiveServicesCredentials
from pydantic import BaseModel


class LanguageResultItem(BaseModel):
    name: str
    iso6391_name: str
    score: Decimal
    additional_properties: Dict


class TranslationUtil:

    def __init__(self):
        self.text_analytics_client: Optional[TextAnalyticsClient] = None
        self.__init_analytics_client()

    def __init_analytics_client(self):
        try:
            cog_endpoint: str = os.environ.get('cog_endpoint')
            credentials: Optional[CognitiveServicesCredentials] = CognitiveServicesCredentials(os.environ.get('cog_key'))
            self.text_analytics_client = TextAnalyticsClient(endpoint=cog_endpoint, credentials=credentials)

        except ValueError:
            print('Azure subscription key missing, please make sure it\'s added to the system environment path.')

    def detect_language(self, text: str) -> LanguageResultItem or None:
        if self.text_analytics_client is not None:

            language_input = LanguageInput(text=text, id=uuid.uuid4())

            language_analysis = self.text_analytics_client.detect_language(documents=[language_input])

            language_result_item: LanguageResultItem = language_analysis.documents[0].detected_languages[0]

            return language_result_item


if __name__ == '__main__':
    translation_util = TranslationUtil()
    detected_language_thingie = translation_util.detect_language('Idek what this is anymore')

    if detected_language_thingie is not None:
        print(detected_language_thingie.name)
        print(detected_language_thingie.score)
        print(detected_language_thingie.iso6391_name)

