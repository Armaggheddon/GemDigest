import asyncio
from enum import Enum
from typing import Union, List, Tuple
from dataclasses import dataclass, Field

from crawl4ai import AsyncWebCrawler

from cache import AsyncCache
from utils import extract_urls

class ResultAttributes(Enum):
    MARKDOWN = "markdown"
    
@dataclass
class ScrapeResult():
    content: str
    sub_urls: List[str]
    original_url: str
    

# This function is a wrapper around the _crawl_urls function
# that allows for the caching of the results of the crawl
async def crawl_urls(
    urls: Union[str, List[str]], 
    result_attribute: ResultAttributes = ResultAttributes.MARKDOWN, 
    verbose=True
    ) -> List[ScrapeResult]:
    """
    
    """
    if isinstance(urls, str):
        urls = [urls]

    return await _crawl_urls(tuple(urls), result_attribute, verbose)

@AsyncCache.lru_cache(max_size=1000)
async def _crawl_urls(
    urls: Tuple[str], 
    result_attribute: ResultAttributes = ResultAttributes.MARKDOWN, 
    verbose=True
    ) -> List[ScrapeResult]:

    crawl_urls = urls
    scrape_results = []

    async with AsyncWebCrawler(verbose=verbose) as scraper:
        
        # Crawl all the urls in parallel
        _crawl_result_futures = asyncio.gather(
            *[scraper.arun(url=url) for url in crawl_urls]
        )
        _crawl_results = await _crawl_result_futures

        scrape_results.extend(
            [
                ScrapeResult(
                    content=getattr(result, result_attribute.value),
                    sub_urls=extract_urls(getattr(result, result_attribute.value)),
                    original_url=url
                )
                for result, url in zip(_crawl_results, crawl_urls)
            ]
        )

    return scrape_results

