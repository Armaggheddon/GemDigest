import logging
import asyncio
from typing import Optional

import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

from configs import api_keys
from cache import lru_cache_with_age
from .prompts import system_prompt
from .formatter import format_gemini_response
from .types import (
    GeminiTokenCount, 
    GeminiFinishReasonMessages, 
    GeminiResponse,
    GeminiModelInfo
)


class GeminiAPIClient():
    
    _instance: Optional['GeminiAPIClient'] = None
    
    def __init__(self, api_key: str) -> None:

        generation_config = genai.GenerationConfig(
            candidate_count=1,
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="application/json",
        )

        model_name = "gemini-1.5-flash-001"

        self.model_info = GeminiModelInfo(
            model_name=model_name,
            temperature=generation_config.temperature,
            top_p=generation_config.top_p,
            top_k=generation_config.top_k,
            max_output_tokens=generation_config.max_output_tokens
        )

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            system_instruction=system_prompt
        )

        self.token_count = GeminiTokenCount()

    @staticmethod
    def _touch_instance():
        # Creates a new instance if not already
        # exists.
        # Has a "lazy loading" like behavior
        if not GeminiAPIClient._instance:
            GeminiAPIClient._instance = GeminiAPIClient(
                api_keys.get_gemini_api_key())
    
    @staticmethod
    def get_used_tokens() -> GeminiTokenCount:
        # TODO: add dataclass that includes 
        # both input and output tokens
        GeminiAPIClient._touch_instance()
        
        return GeminiAPIClient._instance.token_count
    
    @staticmethod
    def get_model_info():
        GeminiAPIClient._touch_instance()
        return GeminiAPIClient._instance.model_info
    
    @lru_cache_with_age(max_size=1000)
    @staticmethod
    async def generate_text(
        prompt: str,
        format: bool = True,
        max_retries: int = 2
    ) -> GeminiResponse:
        # Public facing method that can be used to 
        # interact without having to manage a class
        # instance
        GeminiAPIClient._touch_instance()
        return await GeminiAPIClient._instance._generate_text_with_retry(
            prompt, format, max_retries)
    

    async def _generate_text_with_retry(
        self, 
        prompt: str, 
        format: bool, 
        max_retries: int = 2
    ) -> GeminiResponse:
        retries = 0
        _last_result: GeminiResponse | None = None
        while retries < max_retries:
            try:
                _last_result = await self._generate_text(prompt, format)
                if _last_result.error_message:
                    raise GoogleAPIError(_last_result.error_message)
                break # exit loop if no error

            except GoogleAPIError as e:
                # Error with the google api
                logging.error(f"GoogleAPIError: {e}")
                await asyncio.sleep(1)
            except ValueError as e:
                # Error parsing the json created by gemini
                logging.error(f"{e}")
            finally:
                retries += 1
        
        return (_last_result if _last_result 
            else GeminiResponse(error_message="Max retries reached"))

    
    async def _generate_text(
        self,
        prompt: str,
        format: bool,
    ) -> GeminiResponse:        

        # Use generate_content instead of 
        # chat_session since we are not
        # interacting with the model in a
        # conversational manner, but rather
        # generating one-time content based
        # on a prompt
        response = await self.model.generate_content_async(prompt)
        _generated_text = response.text

        # token count in gemini api uses caching, therefore
        # the prompt_token_count will remain the same
        # for the same prompt. Similar behavior is seen
        # in candidates_token_count. The only "stable"
        # number is total_token_count. Maybe just use that ?!
        usage_metadata = response.usage_metadata

        # get token counts
        (self
            .token_count
            .last_input_token_count) = usage_metadata.prompt_token_count
        (self
            .token_count
            .last_output_token_count) = usage_metadata.candidates_token_count
        (self
            .token_count
            .total_input_token_count) += usage_metadata.prompt_token_count
        (self
            .token_count
            .total_output_token_count) += usage_metadata.candidates_token_count

        # in our scenario there is only one candidate
        finish_reason = GeminiFinishReasonMessages[
            response.candidates[0].finish_reason.name]
        if finish_reason != GeminiFinishReasonMessages.STOP: 
            return GeminiResponse(
                error_message=finish_reason.value)

        if format:
            _generated_text = format_gemini_response(_generated_text)
        
        return GeminiResponse(text=_generated_text)