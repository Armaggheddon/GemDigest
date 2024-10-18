from typing import List

def sanitize_code(text: str) -> str:
    """
    Sanitize a string of text to be used in a Telegram code block with MarkdownV2.

    Args:
        text (str): The text to sanitize.

    Returns:
        str: The sanitized code.
    """
    # Escape special characters
    escape_chars = ["`", "\\"]

    return _base_sanitize(text, escape_chars)


def sanitize_str(text: str) -> str:
    """
    Sanitize a string of text to be used in a Telegram message with MarkdownV2.

    Args:
        text (str): The text to sanitize.

    Returns:
        str: The sanitized text.
    """
    # Escape special characters
    escape_chars = ["_", "*","[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"]

    return _base_sanitize(text, escape_chars)


def sanitize_float(number: float) -> str:
    """
    Sanitize a float number to be used in a Telegram message with MarkdownV2.

    Args:
        number (float): The number to sanitize.

    Returns:
        str: The sanitized number.
    """
    return sanitize_str(f"{number:.2f}")


def _base_sanitize(text: str, excape_chars: List[str]) -> str:
    """
    Sanitize a string of text by escaping specified characters.

    Args:
        text (str): The text to sanitize.
        escape_chars (List[str]): A list of characters to escape.

    Returns:
        str: The sanitized text.
    """
    sanitized = "".join(
        [f"\\{ch}" if ch in excape_chars else ch for ch in text]
    )

    return sanitized