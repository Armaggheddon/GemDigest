import os

import google.generativeai as genai

import settings 


GEMINI_API_KEY = settings.GEMINI_API_KEY
#? FIX THE PROBLEM WITH THE ENV VARIABLE:
#? genai.configure(api_key=os.environ[GEMINI_API_KEY])
genai.configure(api_key=GEMINI_API_KEY)


def generate_text(
        generation_config: dict,
        prompt: str,
        history: list[str] = []
    ) -> str:
    """
    
    """
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=history
    )

    response = chat_session.send_message(settings.gemini_prompt_v1 + prompt)
    return response.text