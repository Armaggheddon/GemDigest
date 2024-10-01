
TELEGRAM_API_KEY = "TOKEN"

GEMINI_API_KEY = "TOKEN"

# Create the model
generation_config = {
"temperature": 1,
"top_p": 0.95,
"top_k": 64,
"max_output_tokens": 8192,
"response_mime_type": "text/plain",
}