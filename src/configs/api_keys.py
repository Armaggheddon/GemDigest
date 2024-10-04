import os

def get_gemini_api_key():
    """Retrieves the GEMINI_API_KEY from environment variables.

    Returns:
        str: The value of the GEMINI_API_KEY environment variable.

    Raises:
        RuntimeError: If the GEMINI_API_KEY environment variable is not set.
    """
    try:
        return os.environ["GEMINI_API_KEY"]
    except RuntimeError as e:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")


def get_telegram_api_key():
    """Retrieves the TELEGRAM_BOT_TOKEN from environment variables.

    Returns:
        str: The value of the TELEGRAM_API_KEY environment variable.

    Raises:
        RuntimeError: If the TELEGRAM_API_KEY environment variable is not set.
    """
    try:
        return os.environ["TELEGRAM_API_KEY"]
    except RuntimeError as e:
        raise RuntimeError("TELEGRAM_API_KEY environment variable not set")
    