from decimal import Decimal
from typing import Dict

from pydantic import BaseModel


class LanguageResultItem(BaseModel):
    name: str
    iso6391_name: str
    score: Decimal
    additional_properties: Dict
