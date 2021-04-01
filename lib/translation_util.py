import uuid
from typing import Optional

import requests
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from azure.cognitiveservices.language.textanalytics.models import LanguageInput
from msrest.authentication import CognitiveServicesCredentials

from .environment import Environment
from .language_result_item import LanguageResultItem


class TranslationUtil:

    def __init__(self):
        self.__text_analytics_client: Optional[TextAnalyticsClient] = None

        self.__init_analytics_client()

    def __init_analytics_client(self):
        try:
            credentials: Optional[CognitiveServicesCredentials] = CognitiveServicesCredentials(Environment.COG_KEY)
            self.__text_analytics_client = TextAnalyticsClient(endpoint=Environment.COG_ENDPOINT, credentials=credentials)

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

        translator_api_endpoint = Environment.TRANSLATOR_API_ENDPOINT

        headers = {
            'Ocp-Apim-Subscription-Key': Environment.COG_KEY,
            'Ocp-Apim-Subscription-Region': Environment.COG_REGION,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        request_body = [{
            'text': source_text
        }]

        response = requests.post(translator_api_endpoint, params=query_params, headers=headers, json=request_body)
        response_content = response.json()

        return response_content[0]['translations'][0]['text']

