"""
This module provides functions to format and parse Gemini API responses.

It includes functionality to:
- Format raw Gemini API responses into structured HTML output, including title, 
    summary, and image links.
- Parse and handle markdown-style text and code blocks.
- Build HTML components from the parsed response.

Functions:
    format_gemini_response: Formats the raw Gemini API response into a 
        structured output.
    _title_builder: Formats a title as bold text after removing markdown symbols.
    _summary_builder: Converts markdown text into HTML, handling code blocks.
    _image_builder: Builds an HTML anchor tag linking to an image URL.
    _markup_to_html_parser: Converts markdown-style formatting to HTML.
    split_markdown_code: Splits markdown content into plain text and code blocks.
"""
import re
import itertools
from io import StringIO
from typing import Mapping, Any, List, Tuple

from .json_parser import parse_gemini_json
from .types import GeminiOutputFormatTemplate


def format_gemini_response(
    raw_str: str, 
    format: Mapping[str, Any] = GeminiOutputFormatTemplate
)-> str:
    """Formats the raw Gemini API response into a structured output 
        containing a title, summary, and image.

    Args:
        raw_str (str): The raw JSON response string from the Gemini API.
        format (Mapping[str, Any], optional): The format template for parsing 
            the JSON. Defaults to GeminiOutputFormatTemplate.

    Returns:
        str: A formatted string containing the title, summary, and image in 
            HTML format.
    """
    _parsed_output = parse_gemini_json(raw_str, format)
    
    _title =  _title_builder(_parsed_output.title)
    _summary =  _summary_builder(_parsed_output.summary)
    _image =  _image_builder(_parsed_output.image_url)

    return "%s\n\n%s\n%s" %(_title, _summary, _image)


def _title_builder(title: str) -> str:
    """Formats the given title as bold text after removing specific 
        markdown-style symbols.

    This function strips the title of markdown symbols such as `*`, `__`, 
    `` ` ``, `~~`, and `||`, and returns the title wrapped in HTML bold tags.

    Args:
        title (str): The input title string that may contain 
            markdown-style symbols.

    Returns:
        str: The formatted title string with HTML bold tags, 
            and without markdown symbols.
    """
    escape_tokens = ["*", "__", "`", "~~", "||"]

    for symbol in escape_tokens:
        title = title.replace(symbol, "")

    return f"<b>{title}</b>"


def _summary_builder(summary: str) -> str:
    """Builds an HTML-formatted summary by parsing the provided markdown 
        text and code blocks.

    Args:
        summary (str): The markdown content to be converted into HTML.

    Returns:
        str: The HTML-formatted content where markdown text is converted to 
            HTML and code blocks are embedded in <pre> tags.
    """
    output = StringIO()
    texts, code = split_markdown_code(summary)

    for text, code_text in itertools.zip_longest(texts, code):
        if text:
            text = _markup_to_html_parser(text)
            output.write(text)
        if code_text:
            output.write(f" <pre language='{code_text[0]}'>")
            output.write(f"{code_text[1]}</pre> ")
    
    content = output.getvalue()
    return content


def _image_builder(image_url: str) -> str:
    """Builds an HTML anchor tag linking to an image URL.

    Args:
        image_url (str): The URL of the image to be embedded as a hyperlink.

    Returns:
        str: An HTML anchor tag containing a zero-width space linking 
            to the image URL.
    """
    image_url.rstrip("/|\\")
    return  f"<a href='{image_url}'>&#8205</a>"


def _markup_to_html_parser(text: str) -> str:
    """Converts markdown-style formatting in text to HTML tags.

    Args:
        text (str): The markdown-formatted text (e.g., with bold, italics, 
            strikethrough, etc.).

    Returns:
        str: The HTML-formatted version of the input text.
    """
    # There is also ||text|| for hidden text
    escape_tokens = [
        ("**", "<b>", "</b>"),
        ("`", "<code>", "</code>"),
        ("*", "<i>", "</i>"),
        ("~~", "<s>", "</s>"),
        ("__", "<u>", "</u>")
    ]

    for symbol in escape_tokens:
        text_chunks = text.count(symbol[0])
        
        if text_chunks % 2 != 0:
            break

        for _ in range(text_chunks // 2):
            text = text.replace(symbol[0], symbol[1], 1)
            text = text.replace(symbol[0], symbol[2], 1)

    text = text.replace("<code></code>", "")
    return text


def split_markdown_code(text: str) -> Tuple[List[str], List[tuple[str, str]]]:
    """Splits markdown content into plain text and code blocks.

    Args:
        text (str): The markdown text containing code blocks 
            (formatted with triple backticks).

    Returns:
        Tuple[List[str], List[tuple[str, str]]]: 
            - A list of normal text parts without code.
            - A list of tuples where each contains a programming language and 
                the respective code block.
    """
    # Regex to match multiple markdown-style code blocks
    markdown_code_pattern = re.compile(r'(.*?)```(\w+)\n(.*?)```', re.DOTALL)
    # Find all code_chunks for code blocks
    code_chunks = markdown_code_pattern.findall(text)
    # Capture the text that comes after the last code block
    remainder_text = markdown_code_pattern.sub('', text).strip()

    normal_text, code_text = [], []
    
    for match in code_chunks:
        before_code = match[0].strip()  # Text before the code block
        language = match[1]  # Language of the code block
        code = match[2].strip().replace("\n", " ")  # Code block in one line

        if before_code:
            normal_text.append(before_code)
        code_text.append((language, code))

    if remainder_text:
        normal_text.append(remainder_text)
    
    return normal_text, code_text
