"""This module provides functions for detecting, extracting, and verifying 
    URLs in text.

The module includes regular expressions to detect URLs in a string, 
    and functions to:
- Check if a string contains a URL.
- Extract all URLs from a given text.
- Verify if a URL belongs to YouTube.

Functions:
    - has_url: Checks if a given string contains a URL.
    - extract_urls: Extracts and returns a list of URLs from a given string.
    - is_youtube: Checks if a given URL is a YouTube link.

Imports:
    - List (from typing): For type hinting list return types.
    - re: For using regular expressions to find URLs.
    - urlparse (from urllib.parse): To parse and check URL components.
"""
from typing import List
import re
from urllib.parse import urlparse


_links_regex_template = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

links_regex = re.compile(_links_regex_template)


def has_url(text: str) -> bool:
    """Checks whether the given text contains a URL.

    This function uses a regular expression to search for URLs in the input text. 
    It returns `True` if a URL is found, and `False` otherwise.

    Args:
        text (str): The input text to search for URLs.

    Returns:
        bool: `True` if the text contains a URL, `False` otherwise.

    Example:
        has_url("Check out this link: https://example.com")  # Returns: True
    """
    if links_regex.search(text):
        return True
    return False
    

def extract_urls(text: str) -> List[str]:
    """
    Extracts all URLs from the given text.

    This function searches for and extracts all URLs in the input text using a 
    regular expression. The URLs are returned as a list of strings.

    Args:
        text (str): The input text to extract URLs from.

    Returns:
        List[str]: A list of URLs found in the input text. If no URLs are found, 
        an empty list is returned.

    Example:
        extract_urls("Visit https://example.com and http://test.com")  
        # Returns: ["https://example.com", "http://test.com"]
    
    #: WARNING: check the url[0] why is used here
    """
    urls = links_regex.findall(text)
    urls_list = [url[0] for url in urls]
    return urls_list


def is_youtube(link: str) -> bool:
    """
    Check if the given link is a YouTube URL.

    This function checks if the given link is a YouTube URL by comparing the 
    domain name to "youtube.com" and "youtu.be". It returns `True` if the link 
    is a YouTube URL, and `False` otherwise.

    Args:
        link (str): The link to check.

    Returns:
        bool: `True` if the link is a YouTube URL, `False` otherwise.

    Example:
        is_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Returns: True
    """

    host = urlparse(link).hostname
    return host == "www.youtube.com"


def add_https_prefix(url: str) -> str:
    """
    Add the HTTP prefix to a URL if it does not have one.
    """

    # just needs to check first 8 characters
    if not url.startswith(("http://", "https://"), start=0, end=8):
        return "https://" + url

    return url
