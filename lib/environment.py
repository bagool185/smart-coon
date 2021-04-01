import os


class Environment:
    COG_ENDPOINT: str = os.environ.get('cog_endpoint')
    COG_KEY: str = os.environ.get('cog_key')
    COG_REGION: str = os.environ.get('cog_region')
    TRANSLATOR_API_ENDPOINT: str = os.environ.get('translator_api_endpoint')
