"""
SEO Analyzer Module
 
This module provides functions to analyze the SEO aspects of a web page.
It includes functions to fetch and parse HTML content, analyze the head and body sections,
check heading tag order, extract keywords, and analyze specific SEO metrics.
 
Functions:
- get_soup(url): Fetches and parses HTML content from a given URL.
- analyze_head(soup): Analyzes the head section of HTML for SEO metrics.
- analyze_h_tags_order(soup): Analyzes the order of heading tags (h1 to h6) in HTML body.
- get_keywords(soup): Extracts top keywords (bigrams) from HTML body text.
- analyze_body(soup): Analyzes the body section of HTML for SEO metrics.
- analyze_url(url): Analyzes a given URL comprehensively for SEO metrics.
 
Dependencies:
- requests: For making HTTP requests to fetch web pages.
- BeautifulSoup (from bs4): For parsing HTML content.
- nltk: For natural language processing tasks such as tokenization and frequency analysis.
 
Note: Requires an 'english' file in the working directory containing stopwords for keyword extraction.
"""
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk import bigrams


def get_soup(url):
    """Get BeautifulSoup object from URL."""
    res = requests.get(url)
    return BeautifulSoup(res.content, "html.parser")


def analyze_head(soup):
    """Analyze HTML head section."""
    results = {}
    title_tag = soup.find("title")
    results["title_exist"] = 1 if title_tag else 0
    results["title_length"] = len(title_tag.get_text()) if title_tag else 0

    description_tag = soup.find("meta", attrs={"name": "description"})
    results["description_exist"] = 1 if description_tag else 0

    return results


def analyze_h_tags_order(soup):
    """Analyze h tags order"""
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    previous_level = 0
    for heading in headings:
        current_level = int(heading.name[1])

        if current_level > previous_level + 1:
            return 0

        previous_level = current_level

    return 1


def get_keywords(soup):
    """returns keywords in pairs"""
    body_text = soup.find("body").get_text().lower()
    words = [word for word in word_tokenize(body_text) if word.isalpha()]

    with open("english", "r") as file:
        stopwords = set(line.strip() for line in file)

    filtered_words = [word for word in words if word not in stopwords]
    new_bigrams = list(bigrams(filtered_words))
    bi_freq = nltk.FreqDist(new_bigrams).most_common(10)

    most_common_bigram_strings = [" ".join(bigram) for bigram, freq in bi_freq]
    keywords_dict = {
        str(i + 1): keyword for i, keyword in enumerate(most_common_bigram_strings)
    }

    return keywords_dict


def analyze_body(soup):
    """Analyze HTML body section."""
    results = {}

    results["h1_exist"] = 1 if soup.find("h1") else 0

    results["h_tags_order"] = analyze_h_tags_order(soup)

    results["h1_count"] = len(soup.find_all("h1"))

    results["img_alt"] = 1 if soup.find("img", alt="") else 0

    results["key_words"] = get_keywords(soup)

    return results


def analyze_url(url):
    """Analyze URL for SEO."""
    soup = get_soup(url)
    head_results = analyze_head(soup)
    body_results = analyze_body(soup)

    results = {**head_results, **body_results}
    results["url"] = url

    return results
