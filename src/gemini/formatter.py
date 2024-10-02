from typing import Tuple
import json


def format_gemini_response(raw_str: str) -> Tuple[bool, str]:
    """
    """
    raw_json = json.loads(raw_str)

    try:
        title = _title_builder(raw_json["title"])
        summary = _summary_builder(raw_json["summary"])
        image = _image_builder(raw_json["url"])

    except TypeError as e:
        # Log the error or return a default message
        print(f"Error processing raw_json: {raw_json}, error: {e}")
        return (False, "Error: Invalid data format.")
    
    return (True, f"<b>{title}</b>\n\n{summary}\n<a href='{image}'>&#8205</a>")


def _title_builder(title: str) -> str:
    """
    TODO:
    """
    return title


def _summary_builder(summary: str) -> str:
    """
    TODO:
    """
    return summary


def _image_builder(image_url: str) -> str:
    """
    TODO:
    """
    return image_url.rstrip("/|\\")