import os
import uuid
from decimal import Decimal
from typing import Dict, Optional

import requests
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
        self.__text_analytics_client: Optional[TextAnalyticsClient] = None
        self.__cog_endpoint: str = os.environ.get('cog_endpoint')
        self.__cog_key: str = os.environ.get('cog_key')
        self.__cog_region: str = os.environ.get('cog_region')

        self.__init_analytics_client()

    def __init_analytics_client(self):
        try:
            credentials: Optional[CognitiveServicesCredentials] = CognitiveServicesCredentials(self.__cog_key)
            self.__text_analytics_client = TextAnalyticsClient(endpoint=self.__cog_endpoint, credentials=credentials)

        except ValueError:
            print('Azure subscription key missing, please make sure it\'s added to the system environment path.')

    def detect_language(self, source_text: str) -> LanguageResultItem or None:
        if self.__text_analytics_client is not None:

            language_input = LanguageInput(text=source_text, id=uuid.uuid4())

            language_analysis = self.__text_analytics_client.detect_language(documents=[language_input])

            language_result_item: LanguageResultItem = language_analysis.documents[0].detected_languages[0]

            return language_result_item

    def translate_text(self, source_text: str, to_lang: str, from_lang: str):

        query_params = {
            'from': from_lang,
            'to': to_lang
        }

        translator_api_endpoint = os.environ.get('translator_api_endpoint')

        headers = {
            'Ocp-Apim-Subscription-Key': self.__cog_key,
            'Ocp-Apim-Subscription-Region': self.__cog_region,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        request_body = [{
            'text': source_text
        }]

        response = requests.post(translator_api_endpoint, params=query_params, headers=headers, json=request_body)
        response_content = response.json()
        return response_content[0]['translations'][0]['text']


if __name__ == '__main__':
    translation_util = TranslationUtil()
    text = 'Idek what this is anymore'
    detected_language_thingie = translation_util.detect_language(text)

    if detected_language_thingie is not None:
        print(detected_language_thingie.name)
        print(detected_language_thingie.score)
        print(detected_language_thingie.iso6391_name)

        print(translation_util.translate_text(source_text=text, from_lang=detected_language_thingie.iso6391_name, to_lang='fr'))

