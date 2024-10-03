import os

class _APIKeys(object):
    @property
    def GEMINI_API_KEY(self) -> str:
        if "GEMINI_API_KEY" in os.environ:
            return os.environ["GEMINI_API_KEY"]
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    
    @property
    def TELEGRAM_BOT_TOKEN(self) -> str:
        if "TELEGRAM_API_KEY" in os.environ:
            return os.environ["TELEGRAM_API_KEY"]
        raise RuntimeError("TELEGRAM_API_KEY environment variable not set")
    
APIKeys = _APIKeys()