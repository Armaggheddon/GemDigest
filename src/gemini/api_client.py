"""This module defines the GeminiAPIClient class, responsible for interacting 
with the Gemini model to generate text responses based on prompts. The client 
uses the Google Gemini API for text generation and handles retries and token 
counting. It provides static methods for retrieving model information 
and token usage, as well as generating text with optional formatting.

GeminiAPIClient:
    This class implements a singleton design pattern to ensure that only one 
        instance of the client is used across the application. The client is 
        used to configure the model and manage text generation requests.

Static Methods:
    - get_used_tokens: Retrieves the total input and output tokens used by 
        the model.
    - get_model_info: Returns the model's configuration details such as name, 
        temperature, top-p, top-k, and max tokens.
    - generate_text: Generates a response based on a given prompt and supports 
        retries on failures.

Instance Methods:
    - _generate_text_with_retry: Handles retries for text generation in 
        case of API errors.
    - _generate_text: Generates text asynchronously using the Gemini model 
        and handles token counting.

Error Handling:
    - Handles GoogleAPIError for issues during API calls.
    - Logs ValueErrors for issues like parsing JSON responses.
    - Implements retries with an exponential backoff in case of failures.

Caching:
    - The generate_text method is cached to avoid redundant requests for 
        identical prompts within a specified time window.
"""
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
    """A client for interacting with the Google Gemini API to generate text 
    based on prompts. The client is a singleton that ensures only one instance 
    is used across the application.

    Attributes:
        model_info (GeminiModelInfo): Contains details about the current 
            model configuration.
        token_count (GeminiTokenCount): Keeps track of input and output tokens 
            for the API usage.
        model (GenerativeModel): The instance of the generative model used to 
            generate text.

    Methods:
        get_used_tokens: Returns the token counts used by the model.
        get_model_info: Returns the model information.
        generate_text: Generates a response based on a given prompt.
    """
    _instance: Optional['GeminiAPIClient'] = None
    

    def __init__(self, api_key: str) -> None:
        """Initializes the GeminiAPIClient with the given API key and 
            configures the model.

        Args:
            api_key (str): The API key for authenticating requests to 
                the Gemini API.
        """
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
        """Ensures that the GeminiAPIClient singleton instance is initialized 
            (lazy loading).
        """
        # Creates a new instance if not already
        # exists.
        # Has a "lazy loading" like behavior
        if not GeminiAPIClient._instance:
            GeminiAPIClient._instance = GeminiAPIClient(
                api_keys.get_gemini_api_key())
    

    @staticmethod
    def get_used_tokens() -> GeminiTokenCount:
        """Returns the total input and output token counts for the API usage.

        Returns:
            GeminiTokenCount: A dataclass that includes both input and output 
                token counts.
        """
        # TODO: add dataclass that includes 
        # both input and output tokens
        GeminiAPIClient._touch_instance()
        
        return GeminiAPIClient._instance.token_count
    

    @staticmethod
    def get_model_info():
        """Returns the configuration details of the current model.

        Returns:
            GeminiModelInfo: A dataclass containing the model's name, 
                temperature, top-p, top-k, and max tokens.
        """
        GeminiAPIClient._touch_instance()
        return GeminiAPIClient._instance.model_info
    

    @lru_cache_with_age(max_size=1000)
    @staticmethod
    async def generate_text(
        prompt: str,
        format: bool = True,
        max_retries: int = 2
    ) -> GeminiResponse:
        """
        Generates a response based on the provided prompt.

        Args:
            prompt (str): The input text prompt for generating a response.
            format (bool, optional): Whether to format the response using 
                the formatter. Defaults to True.
            max_retries (int, optional): The maximum number of retry attempts 
                in case of failures. Defaults to 2.

        Returns:
            GeminiResponse: The generated text or an error message in case 
                of failure.
        """
        # Public facing method that can be used to 
        # interact without having to manage a class
        # instance
        GeminiAPIClient._touch_instance()
        return await GeminiAPIClient._instance._attempt_generate_text(
            prompt, format, max_retries)
    

    async def _attempt_generate_text(
        self, 
        prompt: str, 
        format: bool, 
        max_retries: int = 2
    ) -> GeminiResponse:
        """Attempts to generate text, retrying if the API call fails, up 
            to a maximum number of retries.

        Args:
            prompt (str): The input text prompt.
            format (bool): Whether to format the generated response.
            max_retries (int, optional): The maximum number of retry attempts. 
                Defaults to 2.

        Returns:
            GeminiResponse: The generated text or an error message if retries 
                are exhausted.
        """
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
        """Generates text asynchronously using the Gemini model, updates 
            token counts, and optionally formats the response.

        Args:
            prompt (str): The input text prompt.
            format (bool): Whether to format the generated response.

        Returns:
            GeminiResponse: The generated text or an error message.
        """
        # Use generate_content instead of 
        # chat_session since we are not
        # interacting with the model in a
        # conversational manner, but rather
        # generating one-time content based
        # on a prompt
        response = await self.model.generate_content_async(prompt)

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

        # right now apis only return one candidate
        finish_reason = GeminiFinishReasonMessages[
            response.candidates[0].finish_reason.name]
        
        if (
            finish_reason != GeminiFinishReasonMessages.STOP 
            or finish_reason != GeminiFinishReasonMessages.MAX_TOKENS): 
            return GeminiResponse(
                error_message=finish_reason.value)

        _generated_text = response.text
        if format:
            _generated_text = format_gemini_response(_generated_text)
        
        return GeminiResponse(text=_generated_text)