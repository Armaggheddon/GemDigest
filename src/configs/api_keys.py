import os

class _APIKeys(object):
    """ A class to access API keys from environment variables.

    This class provides properties to retrieve the API keys required 
    for accessing the Gemini API and the Telegram bot. The keys are 
    retrieved from the environment variables. If the required 
    environment variable is not set, a RuntimeError is raised.

    Properties:
        GEMINI_API_KEY (str): The API key for the Gemini service.
        TELEGRAM_BOT_TOKEN (str): The API token for the Telegram bot.

    Raises:
        RuntimeError: If the corresponding environment variable is not set.
    """
    @property
    def GEMINI_API_KEY(self) -> str:
        """Retrieves the GEMINI_API_KEY from environment variables.

        Returns:
            str: The value of the GEMINI_API_KEY environment variable.

        Raises:
            RuntimeError: If the GEMINI_API_KEY environment variable is not set.
        """
        if "GEMINI_API_KEY" in os.environ:
            return os.environ["GEMINI_API_KEY"]
        raise RuntimeError("GEMINI_API_KEY environment variable not set")


    @property
    def TELEGRAM_BOT_TOKEN(self) -> str:
        """Retrieves the TELEGRAM_BOT_TOKEN from environment variables.

        Returns:
            str: The value of the TELEGRAM_API_KEY environment variable.

        Raises:
            RuntimeError: If the TELEGRAM_API_KEY environment variable is not set.
        """
        if "TELEGRAM_API_KEY" in os.environ:
            return os.environ["TELEGRAM_API_KEY"]
        raise RuntimeError("TELEGRAM_API_KEY environment variable not set")
    
APIKeys = _APIKeys()