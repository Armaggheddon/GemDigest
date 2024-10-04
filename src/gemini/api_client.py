from typing import Optional

import google.generativeai as genai

from configs import api_keys
from cache import AsyncCache
from .prompts import system_prompt
from .formatter import format_gemini_response


class GeminiAPIClient():
    
    _instance: Optional['GeminiAPIClient'] = None
    
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

    @staticmethod
    def _touch_instance():
        # Creates a new instance if not already
        # exists.
        # Has a "lazy loading" like behavior
        if not GeminiAPIClient._instance:
            GeminiAPIClient._instance = GeminiAPIClient(api_keys.get_gemini_api_key())
    
    
    @AsyncCache.lru_cache(max_size=1000)
    @staticmethod
    async def generate_text(prompt: str, format: bool = True):
        # Public facing method that can be used to 
        # interact without having to manage a class
        # instance
        GeminiAPIClient._touch_instance()
        return await GeminiAPIClient._instance._generate_text(prompt, format)
    

    async def _generate_text(
        self, prompt: str, format: bool = True
    ) -> str:
        # Private instance method that actually
        # can interact with the instance properties
        # functions and variables...
        
        # TODO: handle a per-user chat session (?)
        response = await self.chat_session.send_message_async(prompt)
        response = response.text
        
        # print(response)
        
        if format:
            success, _response = format_gemini_response(response)
            if success:
                response = _response

        return response