import google.generativeai as genai

from configs import APIKeys
from cache import AsyncCache
from .prompts import system_prompt
from .formatter import format_gemini_response


class _GeminiAPIClient():
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            system_instruction=system_prompt
        )

        # Session starts empty
        self.chat_session = self.model.start_chat()

    @AsyncCache.lru_cache(max_size=1000)
    async def generate_text(
            self, prompt: str, format: bool = True
    ) -> str:
        # TODO: handle a per-user chat session (?)

        response = await self.chat_session.send_message_async(prompt)
        response = response.text
        
        # print(response)
        
        if format:
            success, _response = format_gemini_response(response)
            if success:
                response = _response

        return response
    

gemini_api_client = _GeminiAPIClient(APIKeys.GEMINI_API_KEY)