#!/usr/bin/env python3
"""
Wikipedia Category Word Cloud Visualizer

This Flask application uses the wiki_analyzer.py script to generate
word clouds from Wikipedia categories.
"""

from flask import Flask, render_template, request, jsonify
import sys
import os
import json
from collections import Counter

# Add the wiki_analyzer.py directory to the Python path
wiki_analyzer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'wiki_word_frequency')
sys.path.append(wiki_analyzer_path)

# Import functions from wiki_analyzer.py
try:
    from wiki_analyzer import analyze_category, download_nltk_resources, load_from_cache, get_cache_filename
    print(f"Successfully imported wiki_analyzer from {wiki_analyzer_path}")
except ImportError as e:
    print(f"Error importing wiki_analyzer: {e}")
    print(f"Current sys.path: {sys.path}")
    raise

# Initialize Flask app
app = Flask(__name__)

# Download NLTK resources on startup
download_nltk_resources()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze a Wikipedia category and return word frequencies."""
    data = request.get_json()
    category = data.get('category', '')
    top_n = int(data.get('top_n', 100))
    use_cache = data.get('use_cache', True)
    
    if not category:
        return jsonify({'error': 'Category name is required'}), 400
    
    try:
        # Print debug information
        print(f"Analyzing category: {category}")
        print(f"Top N: {top_n}")
        print(f"Use cache: {use_cache}")
        
        # Check if we have cached results
        is_cached = False
        if use_cache:
            is_cached, cached_results = load_from_cache(category)
            print(f"Cache status for {category}: {'Found' if is_cached else 'Not found'}")
        
        if is_cached and cached_results and len(cached_results) > 0:
            word_counts = cached_results
            source = "cache"
            print(f"Loaded {len(word_counts)} words from cache")
        else:
            # Analyze the category
            word_counts = analyze_category(category, top_n, use_cache)
            source = "fresh analysis"
            print(f"Analyzed {len(word_counts)} words from {category}")
        
        # Get the top N words
        top_words = dict(word_counts.most_common(top_n))
        
        if not top_words:
            return jsonify({'error': 'No words found in the category. Try another category.'}), 404
        
        return jsonify({
            'category': category,
            'words': top_words,
            'source': source,
            'total_words': len(word_counts)
        })
    except Exception as e:
        print(f"Error analyzing category: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/cached-categories')
def cached_categories():
    """Return a list of cached categories."""
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'wiki_word_frequency', 'cache')
    
    if not os.path.exists(cache_dir):
        return jsonify([])
    
    cached = []
    for filename in os.listdir(cache_dir):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(cache_dir, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    word_count = len(data.get('word_counts', {}))
                    if word_count > 0:  # Only include categories with words
                        cached.append({
                            'category': data.get('category', 'Unknown'),
                            'timestamp': data.get('timestamp', 'Unknown'),
                            'word_count': word_count
                        })
            except Exception as e:
                print(f"Error reading cache file {filename}: {e}")
                continue
    
    return jsonify(cached)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
