# Wikipedia Word Cloud Visualizer

A web application that visualizes word frequencies from Wikipedia categories as an interactive word cloud.

## Features

- Search for any Wikipedia category to analyze word frequencies
- Generate beautiful, interactive word clouds with D3.js
- Utilizes local caching system to avoid redundant API calls
- Option to use cached data or perform fresh analysis
- View list of previously cached categories

## Requirements

- Python 3.x
- Flask
- NLTK
- D3.js (loaded via CDN)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```
pip3 install -r requirements.txt
```

## Usage

1. Start the Flask server:

```
python3 app.py
```

2. Open your web browser and navigate to:

```
http://localhost:5000
```

3. Enter a Wikipedia category name (e.g., "Machine learning", "Artificial intelligence", "Planets")
4. Specify the number of top words to display
5. Choose whether to use cached data (if available)
6. Click "Analyze" to generate the word cloud

## How It Works

This application leverages the existing `wiki_analyzer.py` script to:

1. Fetch pages in a Wikipedia category using the MediaWiki API
2. Extract and process text content from each page
3. Remove common words (stopwords) and count word frequencies
4. Cache results locally to improve performance
5. Visualize the results as an interactive word cloud

## Technologies Used

- Backend: Flask, Python
- Frontend: HTML, CSS, JavaScript
- Visualization: D3.js, D3-Cloud
- Data Source: Wikipedia API via the wiki_analyzer.py script
