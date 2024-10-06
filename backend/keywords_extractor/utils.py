"""
keywords_extractor.py

This module provides functions for extracting semantic keywords from web articles
based on a search keyword. It uses asynchronous requests to fetch articles and 
Natural Language Processing (NLP) techniques to analyze the content.

Modules:
- asyncio: To handle asynchronous operations.
- aiohttp: For making asynchronous HTTP requests.
- BeautifulSoup: For parsing HTML content.
- nltk: For natural language processing tasks.
- newspaper3k: For extracting article content.
- spacy: For semantic similarity calculations.

"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.util import trigrams
import nltk
from urllib.parse import urlparse, parse_qs
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import operator
from concurrent.futures import ThreadPoolExecutor
import newspaper

# Ensure nltk data is downloaded
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

# Load spaCy's medium English model for semantic similarity
nlp = spacy.load("en_core_web_md")

async def fetch(session, url, timeout=10):
    """
    Asynchronously fetches the HTML content of a given URL.

    Parameters:
        session (aiohttp.ClientSession): The aiohttp session for making requests.
        url (str): The URL to fetch.
        timeout (int): The timeout duration in seconds (default is 10).

    Returns:
        str: The HTML content of the response if successful, None otherwise.
    """
    try:
        async with session.get(url, timeout=timeout) as response:
            return await response.text()
    except asyncio.TimeoutError:
        print(f"Timeout occurred when trying to fetch {url}")
        return None


async def get_top_links(keyword, session, num_results=10):
    """
    Fetches the top search results from Google for a given keyword.

    Parameters:
        keyword (str): The keyword to search for.
        session (aiohttp.ClientSession): The aiohttp session for making requests.
        num_results (int): The number of top search results to return (default is 10).

    Returns:
        list: A list of URLs of the top search results.
    """
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    keyword = keyword.replace(" ", "+")
    url = f"https://www.google.com/search?q={keyword}&hl=en&num={num_results}"

    async with session.get(url, headers=header) as response:
        if response.status != 200:
            return []

        html_content = await response.text()
        soup = BeautifulSoup(html_content, features="lxml")

        links = []
        for g in soup.find_all("div", {"class": "g"}):
            for a in g.find_all("a"):
                href = a.get("href")
                if href and href.startswith("https://") and not href.startswith("https://translate.google.com") \
                    and not href.startswith("https://youtube.com/"):
                    if href.startswith("https://www.google.com/url?"):
                        parsed = urlparse(href)
                        actual_url = parse_qs(parsed.query).get('q', [None])[0]
                        if actual_url and actual_url.startswith("https://"):
                            links.append(actual_url)
                    else:
                        links.append(href)

                    if len(links) == num_results:
                        return links

        return links

def scrape_article(link, lang='english'):
    """
    Scrapes the content of a given article URL.

    Parameters:
        link (str): The URL of the article to scrape.
        lang (str): The language of the stopwords to be used (default is 'english').

    Returns:
        dict: A dictionary containing the article's link, trigrams of the content,
              and the full text of the article, or None if an error occurs.
    """
    article = newspaper.Article(link, keep_article_html=True)
    try:
        article.download()
        article.parse()
        content = article.text

        text = content.lower()
        word_tokens = word_tokenize(text)
        stop_words = set(stopwords.words(lang))
        filtered_text = [word for word in word_tokens if word.isalpha() and word not in stop_words]


        trigram_tokens = list(trigrams(filtered_text))

        return {
            "link": link,
            "trigrams": [' '.join(trigram) for trigram in trigram_tokens],
            "text": content
        }
    except Exception as e:
        # print(f"Error scraping {link}: {str(e)}")
        return None

async def search_and_extract_keywords(keyword, num_results=10, lang='english'):
    """
    Searches for articles related to a keyword and extracts semantic keywords from them.

    Parameters:
        keyword (str): The keyword to search for.
        num_results (int): The number of articles to process (default is 10).
        lang (str): The language of the stopwords to be used (default is 'english').

    Returns:
        list: A list of the top semantic keywords (trigrams) extracted from the articles.
    """
    async with aiohttp.ClientSession() as session:
        links = await get_top_links(keyword, session, num_results)

        with ThreadPoolExecutor() as executor:
            tasks = [asyncio.get_running_loop().run_in_executor(executor, scrape_article, link, lang) for link in links]
            results = await asyncio.gather(*tasks)

        all_trigrams = []
        documents = []

        for result in results:
            if result:
                all_trigrams.extend(result['trigrams'])
                documents.append(result['text'])


        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
        feature_names = tfidf_vectorizer.get_feature_names_out()


        top_trigrams = compute_semantic_similarity(all_trigrams, keyword)

        return top_trigrams


def compute_semantic_similarity(trigrams, keyword):
    """
    Computes the semantic similarity between trigrams and a given keyword.

    Parameters:
        trigrams (list): A list of trigram strings to evaluate.
        keyword (str): The keyword to compare against.

    Returns:
        list: A list of the top 15 trigrams sorted by their semantic similarity to the keyword.
    """
    keyword_doc = nlp(keyword)
    trigram_docs = list(nlp.pipe(trigrams))

    trigram_scores = {trigram: keyword_doc.similarity(trigram_doc)
                      for trigram, trigram_doc in zip(trigrams, trigram_docs)}

    sorted_trigrams = sorted(trigram_scores.items(), key=operator.itemgetter(1), reverse=True)


    return [trigram for trigram, _ in sorted_trigrams[:15]]
