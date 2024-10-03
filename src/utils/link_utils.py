from typing import List
import re

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