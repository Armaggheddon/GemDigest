import os

# Load environment variables
def get_gemini_api_key():
    if "GEMINI_API_KEY" in os.environ:
        return os.environ["GEMINI_API_KEY"]
    
    raise RuntimeError("GEMINI_API_KEY environment variable not set")

def get_telegram_bot_token():
    if "TELEGRAM_BOT_TOKEN" in os.environ:
        return os.environ
    
    raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable not set")