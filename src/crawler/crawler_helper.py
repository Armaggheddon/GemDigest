import asyncio
import logging
from enum import Enum
from typing import Union, List, Tuple
from dataclasses import dataclass

from crawl4ai import AsyncWebCrawler

from utils import link_utils
from cache import lru_cache_with_age


class ResultAttributes(Enum):
    MARKDOWN = "markdown"
    EXTRACTED_CONTENT = "extracted_content"
    
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


@lru_cache_with_age(max_size=1000)
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
            *[scraper.arun(url=url, word_count_threshold=200) for url in crawl_urls]
        )
        
        _crawl_results = await _crawl_result_futures

        for crawl_result in _crawl_results:
            if crawl_result.error_message:
                logging.info(crawl_result.error_message)
                continue

            scrape_results.append(
                ScrapeResult(
                    content=getattr(crawl_result, result_attribute.value),
                    sub_urls=link_utils.extract_urls(getattr(crawl_result, result_attribute.value)),
                    original_url=crawl_result.url
                )
            )

    return scrape_results

