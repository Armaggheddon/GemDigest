"""This module defines the data structures and enums for handling responses, 
    token counts, and output formats for the Gemini model.

Classes:
    GeminiFinishReasonMessages: Enum representing possible reasons the model 
        finishes token generation.
    GeminiResponse: Data class for encapsulating response text and error messages.
    GeminiTokenCount: Data class for tracking token usage in input and output.
    GeminiOutputFormat: Data class representing the structure of a formatted 
        output, including title, summary, and image URL.
    GeminiOutputFormatTemplate: TypedDict template for structured output, 
        similar to GeminiOutputFormat.

Usage:
    These classes and enums are used to define the expected structure for 
        various aspects of the Gemini model's interactions,
    such as recording token counts, returning formatted responses, and 
        capturing error or finish reasons.
"""
from enum import Enum
from typing import TypedDict, Optional
from dataclasses import dataclass, field


class GeminiFinishReasonMessages(Enum):
    """Enum to represent the different reasons why the Gemini model may stop generating tokens.

    Attributes:
        FINISH_REASON_UNSPECIFIED: Default value, indicating an unspecified 
            or unused stop reason.
        STOP: Natural stop point in the text generation or a stop sequence 
            was encountered.
        MAX_TOKENS: Model reached the maximum token limit specified in the 
            request.
        SAFETY: Generation was flagged for safety reasons.
        RECITATION: The content was flagged for potential recitation reasons.
        LANGUAGE: Content flagged for unsupported language use.
        OTHER: Unknown or unspecified reason for stopping token generation.
        BLOCKLIST: Stopped due to encountering forbidden terms.
        PROHIBITED_CONTENT: Stopped due to potentially prohibited content.
        SPII: Stopped due to potential exposure of Sensitive Personally 
            Identifiable Information (SPII).
        MALFORMED_FUNCTION_CALL: Stopped due to an invalid function call 
            generated by the model.
    """
    FINISH_REASON_UNSPECIFIED="Default value. This value is unused."
    STOP="Natural stop point of the model or provided stop sequence."
    MAX_TOKENS="The maximum number of tokens as specified in the request was reached."
    SAFETY="The response candidate content was flagged for safety reasons."
    RECITATION="The response candidate content was flagged for recitation reasons."
    LANGUAGE="The response candidate content was flagged for using an unsupported language."
    OTHER="Unknown reason."
    BLOCKLIST="Token generation stopped because the content contains forbidden terms."
    PROHIBITED_CONTENT="Token generation stopped for potentially containing prohibited content."
    SPII="Token generation stopped because the content potentially contains Sensitive Personally Identifiable Information (SPII)."
    MALFORMED_FUNCTION_CALL="The function call generated by the model is invalid."


@dataclass
class GeminiResponse:
    """Data class to represent a response from the Gemini model.

    Attributes:
        text (Optional[str]): The text generated by the model, if available.
        error_message (Optional[str]): Any error message encountered during 
            generation.
    """
    text: Optional[str] = field(default=None)
    error_message: Optional[str] = field(default=None)


@dataclass
class GeminiModelInfo:
    """Represents the information about the Gemini model configuration used."""
    model_name: str
    temperature: float
    top_p: float
    top_k: int
    max_output_tokens: int


@dataclass
class GeminiTokenCount:
    """Data class to track token usage by the Gemini model.

    Attributes:
        last_input_token_count (int): Token count for the last input, 
            initialized to 0.
        last_output_token_count (int): Token count for the last output, 
            initialized to 0.
        total_input_token_count (int): Total token count for all inputs, 
            initialized to 0.
        total_output_token_count (int): Total token count for all outputs, 
            initialized to 0.
    """
    last_input_token_count: int = field(init=False, default=0)
    last_output_token_count: int = field(init=False, default=0)
    total_input_token_count: int = field(init=False, default=0)
    total_output_token_count: int = field(init=False, default=0)


@dataclass
class GeminiOutputFormat:
    """Data class to represent a formatted output for the Gemini model.

    Attributes:
        title (str): The title of the output.
        summary (str): A brief summary of the content.
        image_url (str): The URL of the representative image.
    """
    title: str
    summary: str
    image_url: str


class GeminiOutputFormatTemplate(TypedDict):
    """TypedDict to define the expected structure of the Gemini model's output.

    Attributes:
        title (str): The title of the output.
        summary (str): A brief summary of the content.
        image_url (str): The URL of the representative image.
    """
    title: str
    summary: str
    image_url: str