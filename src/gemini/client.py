from typing import List
import functools

import google.generativeai as genai

from configs import api_keys, generation_config, gemini_system_prompt
from .formatter import format_gemini_response
from cache import AsyncCache

class _GeminiClient():
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.generation_config = generation_config

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            system_instruction=gemini_system_prompt
        )

        # Session starts empty
        self.chat_session = self.model.start_chat()

    @AsyncCache.lru_cache(max_size=1000)
    async def generate_text(
            self, prompt: str, format: bool = True
    ) -> str:
        # TODO: handle a per-user chat session

        response = await self.chat_session.send_message_async(prompt)
        response = response.text
        
        # print(response)
        
        if format:
            success, _response = format_gemini_response(response)
            if success:
                response = _response

        return response
    

gemini_api = _GeminiClient(api_keys.GEMINI_API_KEY)