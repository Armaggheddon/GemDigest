import logging
from typing import Mapping, Any

from configs.logger import setup_logger
from .json_parser import parse_gemini_json
from .types import GeminiOutputFormatTemplate

setup_logger()
logger = logging.getLogger(__name__)


def format_gemini_response(
    raw_str: str, 
    format: Mapping[str, Any] = GeminiOutputFormatTemplate
)-> str:
    """
    """
    parserd_output = parse_gemini_json(raw_str, format)
    
    title =  _title_builder(parserd_output.title)
    summary =  _summary_builder(parserd_output.summary)
    image =  _title_builder(parserd_output.image_url)

    return f"<b>{title}</b>\n\n{summary}\n<a href='{image}'>&#8205</a>"


def _title_builder(title: str) -> str:
    """
    TODO:
    """
    return title


def _summary_builder(summary: str) -> str:
    """
    TODO:
    """
    
    tokens = summary.split("**")
    for i in range(1, len(tokens), 2):
        tokens[i] = f"<b>{tokens[i]}</b>"
    
    tokens = "".join(tokens)
    tokens = tokens.split("`")
    for i in range(1, len(tokens), 2):
        tokens[i] = f"<code>{tokens[i]}</code>"

    return "".join(tokens)


def _image_builder(image_url: str) -> str:
    """
    TODO:
    """
    return image_url.rstrip("/|\\")