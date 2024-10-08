import logging
import asyncio
from typing import Optional

import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

from configs import api_keys
from cache import AsyncCache
from .prompts import system_prompt
from .formatter import format_gemini_response
from .types import GeminiTokenCount, GeminiFinishReasonMessages



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
        model_name = "gemini-1.5-flash-001"

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config,
            system_instruction=system_prompt
        )

        self.last_input_token_count = 0
        self.last_output_token_count = 0
        self.total_input_token_count = 0
        self.total_output_token_count = 0

    @staticmethod
    def _touch_instance():
        # Creates a new instance if not already
        # exists.
        # Has a "lazy loading" like behavior
        if not GeminiAPIClient._instance:
            GeminiAPIClient._instance = GeminiAPIClient(api_keys.get_gemini_api_key())
    
    @staticmethod
    def get_used_tokens() -> GeminiTokenCount:
        # TODO: add dataclass that includes 
        # both input and output tokens
        GeminiAPIClient._touch_instance()
        
        return GeminiTokenCount(
            last_input_token_count=GeminiAPIClient._instance.last_input_token_count,
            last_output_token_count=GeminiAPIClient._instance.last_output_token_count,
            total_input_token_count=GeminiAPIClient._instance.total_input_token_count,
            total_output_token_count=GeminiAPIClient._instance.total_output_token_count
        )
    
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

        generated_text = ""

        while max_retries > 0 and not success:
            # TODO: handle a per-user chat session (?)
            try:
                # Use generate_content instead of 
                # chat_session since we are not
                # interacting with the model in a
                # conversational manner, but rather
                # generating one-time content based
                # on a prompt
                response = await self.model.generate_content_async(prompt)
                # print(response)
                _generated_text = response.text

                # token count in gemini api uses caching, therefore
                # the prompt_token_count will remain the same
                # for the same prompt. Similar behavior is seen
                # in candidates_token_count. The only "stable"
                # number is total_token_count. Maybe just use that ?!
                usage_metadata = response.usage_metadata

                # get token counts
                self.last_input_token_count = usage_metadata.prompt_token_count
                self.last_output_token_count = usage_metadata.candidates_token_count
                self.total_input_token_count += usage_metadata.prompt_token_count
                self.total_output_token_count += usage_metadata.candidates_token_count

                # in our scenario there is only one candidate
                if finish_reason := response.candidates[0].finish_reason:
                    generated_text = GeminiFinishReasonMessages.value_from_name(finish_reason.name)

                if not format:
                    return _generated_text
                
                generated_text = format_gemini_response(_generated_text)
                success = True
            
            except GoogleAPIError as e:
                logging.error(f"{e}")
            
            except ValueError as e:
                logging.error(f"{e}")
            
            finally:
                await asyncio.sleep(0.5)
                max_retries -= 1
                
        return generated_text if success else "Error (。_。)" 