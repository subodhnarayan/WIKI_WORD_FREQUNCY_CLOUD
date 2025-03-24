# Wikipedia Category Word Frequency Analyzer

This script analyzes the cumulative frequency of non-common words across all pages in a specified Wikipedia category.

## Features

- Fetches all pages in a given Wikipedia category using the MediaWiki API
- Extracts text content from each page
- Removes common words (stopwords) and punctuation
- Counts and displays word frequencies
- Outputs the most frequent non-common words
- Local caching system to avoid reprocessing the same category multiple times
- Cache expiration after 7 days to ensure data freshness

## Requirements

- Python 3.6+
- Required packages: requests, nltk

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python wiki_analyzer.py "Category_Name"
```

Example:
```bash
python wiki_analyzer.py "Large_Language_Models"
```

## Options

- `--top N`: Display the top N most frequent words (default: 100)
- `--no-cache`: Force fresh data retrieval, ignoring any cached results

Examples:
```bash
python wiki_analyzer.py "Large_Language_Models" --top 50
python wiki_analyzer.py "Large_Language_Models" --no-cache
```

## Cache System

The script automatically caches results in a `cache` directory to avoid reprocessing the same category multiple times. Each cache file:

- Is named using an MD5 hash of the category name
- Contains the word frequency data and a timestamp
- Expires after 7 days to ensure data freshness
- Can be bypassed using the `--no-cache` flag
