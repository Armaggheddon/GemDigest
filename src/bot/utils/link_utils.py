from typing import List
import re

_links_regex_template = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

links_regex = re.compile(_links_regex_template)

def has_url(text: str) -> bool:
    """
    """
    if links_regex.search(text):
        return True
    else:
        return False
    

def extract_urls(text: str) -> List[str]:
    """
    """
    urls_list = []
    
    urls = links_regex.findall(text)

    for url in urls:
        urls_list.append(url[0])

    return urls_list