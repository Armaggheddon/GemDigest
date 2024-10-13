"""This module provides functionality for scraping URLs using an asynchronous 
    web crawler. It includes methods for crawling multiple URLs in parallel 
    and returning the scraped content and extracted sub-URLs. Results can be 
    cached for improved performance.

Classes:
    ResultAttributes: Enum for specifying the type of result attributes 
        to extract.
    ScrapeResult: Data class to hold the scraped content, sub-URLs, and 
        original URL.

Functions:
    crawl_urls: Asynchronously crawls the provided URLs and returns a list 
        of scrape results.
    _crawl_urls: Helper function that performs the actual crawling of the 
        URLs with caching.
"""
import asyncio
import logging
from enum import Enum
from typing import Union, List, Tuple
from dataclasses import dataclass

from crawl4ai import AsyncWebCrawler

from utils import link_utils
from cache import lru_cache_with_age


class ResultAttributes(Enum):
    """Enumeration for the types of attributes that can be extracted from the 
        crawl results.
    """
    MARKDOWN = "markdown"
    EXTRACTED_CONTENT = "extracted_content"
    
@dataclass
class ScrapeResult():
    """Data class to store the results of a web scraping operation.

    Attributes:
        content (str): The content extracted from the web page.
        sub_urls (List[str]): A list of sub-URLs found within the content.
        original_url (str): The original URL that was crawled.
    """
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
    """Asynchronously crawls the specified URLs and returns the scraping 
        results.

    This function serves as a wrapper around the _crawl_urls function to 
        facilitate the caching of crawl results. It accepts both single and 
        multiple URLs.

    Args:
        urls (Union[str, List[str]]): A single URL as a string or a list of 
            URLs to crawl.
        result_attribute (ResultAttributes, optional): The type of result 
            attribute to extract. Defaults to ResultAttributes.MARKDOWN.
        verbose (bool, optional): Whether to log detailed output. 
            Defaults to True.

    Returns:
        List[ScrapeResult]: A list of ScrapeResult instances containing 
            the scraped content and extracted sub-URLs.
    """
    if isinstance(urls, str):
        urls = [urls]

    # check that all the urls have the http/https prefix
    # TODO: could be that https version of website does not exist,
    # a retry logic should be considered to retry with http version
    urls = [link_utils.add_https_prefix(url) for url in urls]

    return await _crawl_urls(tuple(urls), result_attribute, verbose)


@lru_cache_with_age(max_size=1000)
async def _crawl_urls(
    urls: Tuple[str], 
    result_attribute: ResultAttributes = ResultAttributes.MARKDOWN, 
    verbose=True
    ) -> List[ScrapeResult]:
    """Crawls the specified URLs asynchronously and returns the scraping results.

    This function performs the actual crawling of the URLs, caching 
        results to improve performance on subsequent calls.

    Args:
        urls (Tuple[str]): A tuple of URLs to crawl.
        result_attribute (ResultAttributes, optional): The type of result 
            attribute to extract. Defaults to ResultAttributes.MARKDOWN.
        verbose (bool, optional): Whether to log detailed output. 
            Defaults to True.

    Returns:
        List[ScrapeResult]: A list of ScrapeResult instances containing the 
            scraped content and extracted sub-URLs.
    """
    crawl_urls = urls
    scrape_results = []

    async with AsyncWebCrawler(verbose=verbose) as scraper:
        # Crawl all the urls in parallel
        _crawl_result_futures = asyncio.gather(
            *[scraper.arun(
                url=url, 
                word_count_threshold=200
                ) for url in crawl_urls]
        )
        
        _crawl_results = await _crawl_result_futures

        for crawl_result in _crawl_results:
            if crawl_result.error_message:
                logging.info(crawl_result.error_message)
                continue

            scrape_results.append(
                ScrapeResult(
                    content=getattr(crawl_result, result_attribute.value),
                    sub_urls=link_utils.extract_urls(
                        getattr(crawl_result, result_attribute.value)),
                    original_url=crawl_result.url
                )
            )

    return scrape_results

