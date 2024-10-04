import logging
from typing import Optional

import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

from configs import api_keys
from cache import AsyncCache
from configs.logger import setup_logger
from .prompts import system_prompt
from .formatter import format_gemini_response


setup_logger()
logger = logging.getLogger(__name__)


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
            # TODO: "response_schema": Recipe,
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
    async def generate_text(
        prompt: str,
        format: bool = True,
        max_retries: int = 2
    ):
        # Public facing method that can be used to 
        # interact without having to manage a class
        # instance
        GeminiAPIClient._touch_instance()
        return await GeminiAPIClient._instance._generate_text(
            prompt, format, max_retries)
    

    async def _generate_text(
        self,
        prompt: str,
        format: bool,
        max_retries: int
    ) -> str:
        # Private instance method that actually
        # can interact with the instance properties
        # functions and variables...
        success = False

        while max_retries > 0 and not success:
            # TODO: handle a per-user chat session (?)
            try:
                response = await self.chat_session.send_message_async(prompt)
                response = response.text
                if not format:
                    return response
                
                response = format_gemini_response(response)
                success = True
            
            except GoogleAPIError as e:
                logging.error(f"{e}")
            
            except ValueError as e:
                logging.error(f"{e}")
            
            finally:
                max_retries -= 1
                
        return response if success else "Error (。_。)" 