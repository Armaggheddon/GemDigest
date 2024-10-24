import os


def _get_website_blacklist():
    """
    Loads the website blacklist from a specified file. 

    The blacklist file is expected to be located at '/gem_digest_bot/website_blacklist.txt'. 
    Each line in the file should contain a domain name or URL. Lines starting 
    with '#' are considered comments and are ignored. Empty lines are 
    also skipped.

    Returns:
        list: A list of blacklisted websites (if the file exists), or an 
            empty list otherwise.
    """
    _website_blacklist_path = "/gem_digest_bot/extra_configs/website_blacklist.txt"
    blacklisted_websites = []

    if not os.path.isfile(_website_blacklist_path):
        return []
    
    with open(_website_blacklist_path, "r") as f:
        
        for line in f:
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            
            blacklisted_websites.append(line)
        
    print(f"Blacklisted websites: {blacklisted_websites}")
    return blacklisted_websites


blacklisted_websites = _get_website_blacklist()