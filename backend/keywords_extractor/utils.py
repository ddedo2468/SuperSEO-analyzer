"""
This script performs web scraping and text analysis to extract
the most common trigrams (three-word sequences) from the body text of web pages.

The main functionalities include:
1. Performing asynchronous HTTP requests to fetch the HTML content of web pages.
2. Parsing HTML content using BeautifulSoup to extract body text.
3. Tokenizing and filtering text to remove stopwords and non-alphabetical characters.
4. Extracting the most common trigrams from the filtered text.
5. Performing Google searches to get the top search result links for a given keyword.
6. Combining the above functionalities to perform a search for a keyword,
fetch the top result pages, and extract the most common trigrams from the content.

Dependencies:
- asyncio for asynchronous programming.
- aiohttp for asynchronous HTTP requests.
- BeautifulSoup (bs4) for parsing HTML content.
- nltk for natural language processing, specifically tokenization and trigram extraction.

The script consists of the following main functions:
1. fetch(session, url, timeout=10): Fetches the content of a URL.
2. get_soup(session, url): Fetches and parses HTML content from a URL.
3. get_keywords(soup): Extracts the most common trigrams from the body text of the HTML content.
4. get_top_links(keyword, session): Fetches the top search result links from Google for a given keyword.
5. search_and_extract_keywords(keyword): Combines the previous functions to perform a search for a keyword,
fetch the top result pages, and extract the most common trigrams from the content.
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk import trigrams
import nltk
from datetime import datetime, timedelta

# Ensure nltk data is downloaded
nltk.download("punkt")


async def fetch(session, url, timeout=10):
    """
    Fetch the content of a given URL using aiohttp.

    Args:
        session (aiohttp.ClientSession): The aiohttp session object.
        url (str): The URL to fetch content from.
        timeout (int): The timeout period in seconds.

    Returns:
        str: The HTML content of the URL, or None if a timeout occurs.
    """
    try:
        async with session.get(url, timeout=timeout) as response:
            return await response.text()
    except asyncio.TimeoutError:
        print(f"Timeout occurred when trying to fetch {url}")
        return None


async def get_soup(session, url):
    """
    Fetch the HTML content and parse it using BeautifulSoup.

    Args:
        session (aiohttp.ClientSession): The aiohttp session object.
        url (str): The URL to fetch content from.

    Returns:
        BeautifulSoup: The BeautifulSoup object containing
        the parsed HTML content, or None if fetching fails.
    """
    html_content = await fetch(session, url)
    if html_content:
        return BeautifulSoup(html_content, "html.parser")
    return None


def get_keywords(soup):
    """
    Extract the most common trigrams (three-word sequences) from the body text of the HTML content.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML content.

    Returns:
        dict: A dictionary of the most common trigrams.
    """
    if soup is None:
        return {}

    try:
        body = soup.find("body")
        if body:
            body_text = body.get_text().lower()
        else:
            body_text = soup.get_text().lower()
    except AttributeError:
        body_text = ""

    words = [word for word in word_tokenize(body_text) if word.isalpha()]

    with open("english", "r") as file:
        stopwords = set(line.strip() for line in file)

    filtered_words = [word for word in words if word not in stopwords]
    new_trigrams = list(trigrams(filtered_words))
    tri_freq = nltk.FreqDist(new_trigrams).most_common(3)

    most_common_trigram_strings = [" ".join(trigram) for trigram, freq in tri_freq]
    keywords_dict = {
        str(i + 1): keyword for i, keyword in enumerate(most_common_trigram_strings)
    }

    return keywords_dict


async def get_top_links(keyword, session):
    """
    Fetch the top search result links from Google for a given keyword.

    Args:
        keyword (str): The search keyword.
        session (aiohttp.ClientSession): The aiohttp session object.

    Returns:
        list: A list of URLs of the top search results.
    """
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    keyword = keyword.replace(" ", "+")
    url = f"https://www.google.com/search?q={keyword}"

    async with session.get(url, headers=header) as response:
        if response.status != 200:
            return []

        html_content = await response.text()
        soup = BeautifulSoup(html_content, features="lxml")
        links = [
            a["href"]
            for g in soup.find_all("div", {"class": "g"})
            for a in g.find_all("a")
            if a
        ]
        return links


async def search_and_extract_keywords(keyword):
    """
    Perform a Google search for a given keyword, extract the content from the top search results,
    and extract the most common trigrams from the body text.

    Args:
        keyword (str): The search keyword.

    Returns:
        list: A list of unique keywords extracted from the top search result pages.
    """
    async with aiohttp.ClientSession() as session:
        links = await get_top_links(keyword, session)
        tasks = [get_soup(session, link) for link in links]
        soups = await asyncio.gather(*tasks)

        all_keywords = []
        for soup in soups:
            if soup:  # Only process if soup is not None
                keywords = get_keywords(soup)
                all_keywords.extend(keywords.values())

        unique_keywords = list(set(all_keywords))
        return unique_keywords
