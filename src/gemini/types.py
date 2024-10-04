from typing import TypedDict
from dataclasses import dataclass
from pydantic import BaseModel, Field


@dataclass
class GeminiOutputFormat:
    title: str
    summary: str
    image_url: str


class GeminiOutputFormatTemplate(TypedDict):
    title: str
    summary: str
    image_url: str