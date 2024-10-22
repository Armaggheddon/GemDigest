
def _get_website_blacklist():

    _website_blacklist_path = "/gem_digest_bot/website_blacklist.txt.yml
    blacklisted_websites = []

    with open(_website_blacklist_path, "r") as f:
        
        for line in f:
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            
            blacklisted_websites.append(line)
        
    print(f"Blacklisted websites: {blacklisted_websites}")
    return blacklisted_websites


blacklisted_websites = _get_website_blacklist()