"""This module provides functions to retrieve API keys and user IDs
    from environment variables. Each function retrieves a specific 
    environment variable required for application configuration.

Functions:
    get_gemini_api_key: Retrieves the GEMINI_API_KEY from environment variables.
    get_telegram_api_key: Retrieves the TELEGRAM_API_KEY from environment variables.
    get_admin_user_id: Retrieves the ADMIN_USER_ID from environment variables.
    
# TODO: rename this file to a more appropriate name
"""
import os


def get_gemini_api_key() -> str:
    """Retrieves the GEMINI_API_KEY from environment variables.

    Returns:
        str: The value of the GEMINI_API_KEY environment variable.

    Raises:
        RuntimeError: If the GEMINI_API_KEY environment variable is not set.
    """
    try:
        return os.environ["GEMINI_API_KEY"]
    except KeyError as e:
        raise KeyError("GEMINI_API_KEY environment variable not set")


def get_telegram_api_key() -> str:
    """Retrieves the TELEGRAM_BOT_TOKEN from environment variables.

    Returns:
        str: The value of the TELEGRAM_API_KEY environment variable.

    Raises:
        RuntimeError: If the TELEGRAM_API_KEY environment variable is not set.
    """
    try:
        return os.environ["TELEGRAM_API_KEY"]
    except KeyError as e:
        raise KeyError("TELEGRAM_API_KEY environment variable not set")
    

def get_admin_user_ids() -> list[int]:
    """Retrieves the ADMIN_USER_ID from environment variables.

    Returns:
        int: The value of the ADMIN_USER_ID environment variable.

    Raises:
        RuntimeError: If the ADMIN_USER_ID environment variable is not set.
    """
    try:
        admin_users = os.environ["ADMIN_USER_ID"]
        admin_list = admin_users.split(";")

        return [int(admin.strip()) for admin in admin_list]

    except KeyError as e:
        raise KeyError("ADMIN_USER_ID environment variable not set")