from crawl4ai import AsyncWebCrawler


# Function to scrape the website asynchronously
async def scrape_website(url: str) -> str:
    """
    """
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=url)
        return result.markdown