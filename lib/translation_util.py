import os
from typing import Optional

from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials


class TranslationUtil:

    def __init__(self):
        self.__init_analytics_client()
        self.text_analytics_client: Optional[TextAnalyticsClient] = None

    def __init_analytics_client(self):
        try:
            cog_endpoint: str = os.environ.get('cog_endpoint')
            credentials: Optional[CognitiveServicesCredentials] = CognitiveServicesCredentials(os.environ.get('cog_key'))
            self.text_analytics_client = TextAnalyticsClient(endpoint=cog_endpoint, credentials=credentials)

        except ValueError:
            print('Azure subscription key missing, please make sure it\'s added to the system environment path.')

    def detect_language(self, text: str):
        if self.text_analytics_client is not None:
            language_analysis = self.text_analytics_client.detect_language(documents=[text])

            return language_analysis


if __name__ == '__main__':
    translation_util = TranslationUtil()
    detected_language_thingie = translation_util.detect_language('Idek what this is anymore')
    print(detected_language_thingie)
