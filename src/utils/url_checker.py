import re


regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

def contains_url(text: str) -> bool:
    """
    """
    # Ho fatto un esame sulle regex ma sicuro chatgpt le fa meglio di me
    url_pattern = re.compile(regex)
    
    if url_pattern.search(text):
        return True
    else:
        return False


def extract_urls(text: str) -> list[str]:
    """
    """
    urls_list = []
    
    url_pattern = re.compile(regex)
    urls = url_pattern.findall(text)

    for url in urls:
        urls_list.append(url[0])

    return urls_list
