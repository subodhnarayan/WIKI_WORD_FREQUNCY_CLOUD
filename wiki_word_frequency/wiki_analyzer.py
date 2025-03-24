#!/usr/bin/env python3
"""
Wikipedia Category Word Frequency Analyzer

This script takes a Wikipedia category name as input and outputs the cumulative
frequency of non-common words across all pages in that category.
"""

import sys
import requests
import re
import string
import json
import os
import hashlib
from collections import Counter
import argparse
from nltk.corpus import stopwords
import nltk
from datetime import datetime

# Define cache directory
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

def download_nltk_resources():
    """Download required NLTK resources if not already present."""
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading NLTK stopwords...")
        nltk.download('stopwords', quiet=True)

def get_cache_filename(category):
    """
    Generate a cache filename based on the category name.
    
    Args:
        category (str): The Wikipedia category name
        
    Returns:
        str: Cache filename
    """
    # Create a hash of the category name for the filename
    category_hash = hashlib.md5(category.encode('utf-8')).hexdigest()
    return os.path.join(CACHE_DIR, f"{category_hash}.json")

def load_from_cache(category):
    """
    Load cached results for a category if available.
    
    Args:
        category (str): The Wikipedia category name
        
    Returns:
        tuple: (is_cached, word_counts) where word_counts is a Counter object if cached, None otherwise
    """
    cache_file = get_cache_filename(category)
    
    if not os.path.exists(cache_file):
        return False, None
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
            
        # Check if cache is expired (older than 7 days)
        cache_date = datetime.fromisoformat(cache_data.get('timestamp', '2000-01-01'))
        current_date = datetime.now()
        days_diff = (current_date - cache_date).days
        
        if days_diff > 7:
            print(f"Cache for '{category}' is {days_diff} days old. Refreshing...")
            return False, None
            
        print(f"Loading cached results for '{category}' (cached on {cache_data.get('timestamp')})")
        
        # Convert the cached dictionary back to a Counter object
        word_counts = Counter(cache_data.get('word_counts', {}))
        return True, word_counts
    except Exception as e:
        print(f"Error loading cache: {e}")
        return False, None

def save_to_cache(category, word_counts):
    """
    Save results to cache.
    
    Args:
        category (str): The Wikipedia category name
        word_counts (Counter): Word frequency counter
    """
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
        
    cache_file = get_cache_filename(category)
    
    cache_data = {
        'category': category,
        'timestamp': datetime.now().isoformat(),
        'word_counts': dict(word_counts)
    }
    
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)
    
    print(f"Results cached to {cache_file}")

def get_pages_in_category(category):
    """
    Fetch all pages that belong to a specific Wikipedia category.
    
    Args:
        category (str): The Wikipedia category name
        
    Returns:
        list: List of page titles in the category
    """
    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    
    # Remove "Category:" prefix if present
    if category.startswith("Category:"):
        category = category[9:]
    
    # Normalize spaces to underscores for Wikipedia's format
    category = category.replace(" ", "_")
    
    # Try different variations of the category name
    category_variations = [
        category,  # Original
        category.title(),  # Title case
        category.replace("_", " ").title(),  # Title case with spaces
        category.replace("_", " ").title().replace(" ", "_")  # Title case with underscores
    ]
    
    print(f"Trying category variations: {category_variations}")
    
    for cat in category_variations:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{cat}",
            "cmlimit": "500",  # Maximum allowed by API
            "format": "json"
        }
        
        print(f"Trying category: {cat}")
        print(f"API URL: {url}")
        print(f"API params: {params}")
        
        try:
            response = session.get(url=url, params=params, timeout=30)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            data = response.json()
            
            # Debug information
            print(f"API response status code: {response.status_code}")
            
            pages = []
            if "query" in data and "categorymembers" in data["query"]:
                for member in data["query"]["categorymembers"]:
                    # Only include actual pages (namespace 0), not subcategories
                    if member["ns"] == 0:
                        pages.append(member["title"])
                
                if pages:
                    print(f"Found {len(pages)} pages in category '{cat}'")
                    return pages
            else:
                print(f"No pages found for category '{cat}'. API response:")
                print(data)
                
        except Exception as e:
            print(f"Error fetching pages for category '{cat}': {e}")
            continue
    
    print("WARNING: No pages found in any category variation. The category might not exist or might be empty.")
    return []

def get_page_content(page_title):
    """
    Fetch the content of a Wikipedia page.
    
    Args:
        page_title (str): The title of the Wikipedia page
        
    Returns:
        str: The text content of the page
    """
    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    
    params = {
        "action": "query",
        "prop": "extracts",
        "exlimit": "1",
        "explaintext": "1",  # Get plain text content
        "titles": page_title,
        "format": "json"
    }
    
    response = session.get(url=url, params=params)
    data = response.json()
    
    # Extract the page content
    pages = data["query"]["pages"]
    page_id = list(pages.keys())[0]
    
    if "extract" in pages[page_id]:
        return pages[page_id]["extract"]
    return ""

def process_text(text):
    """
    Process text to extract words and remove common words.
    
    Args:
        text (str): The text to process
        
    Returns:
        list: List of processed words
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text)
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Split into words
    words = text.split()
    
    # Remove common words (stopwords)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words and len(word) > 1]
    
    return words

def analyze_category(category, top_n=100, use_cache=True):
    """
    Analyze word frequencies across all pages in a category.
    
    Args:
        category (str): The Wikipedia category name
        top_n (int): Number of top words to display
        use_cache (bool): Whether to use cached results if available
        
    Returns:
        Counter: Word frequency counter
    """
    # Check cache first if enabled
    if use_cache:
        is_cached, cached_results = load_from_cache(category)
        if is_cached and cached_results and len(cached_results) > 0:
            return cached_results
    
    pages = get_pages_in_category(category)
    all_words = []
    
    if not pages:
        print(f"No pages found in category '{category}'. Cannot analyze word frequencies.")
        return Counter()
    
    for i, page in enumerate(pages):
        print(f"Processing page {i+1}/{len(pages)}: {page}")
        content = get_page_content(page)
        words = process_text(content)
        all_words.extend(words)
    
    # Count word frequencies
    word_counts = Counter(all_words)
    
    # Only cache if we actually found words
    if word_counts:
        save_to_cache(category, word_counts)
    else:
        print(f"Warning: No words found in category '{category}'")
    
    return word_counts

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Analyze word frequencies in a Wikipedia category')
    parser.add_argument('category', help='Wikipedia category name')
    parser.add_argument('--top', type=int, default=100, help='Number of top words to display')
    parser.add_argument('--no-cache', action='store_true', help='Disable cache and force fresh data retrieval')
    args = parser.parse_args()
    
    # Download NLTK resources if needed
    download_nltk_resources()
    
    # Analyze the category
    word_counts = analyze_category(args.category, args.top, not args.no_cache)
    
    # Display results
    print("\nTop words by frequency:")
    print("-----------------------")
    for word, count in word_counts.most_common(args.top):
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()
