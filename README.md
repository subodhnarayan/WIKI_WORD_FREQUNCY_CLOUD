# Wikipedia Word Cloud Visualizer

A powerful web application that analyzes Wikipedia categories and generates interactive word clouds to visualize word frequencies. Built with Python, Flask, and D3.js.

## 🌟 Features

- **Interactive Word Clouds**: Visualize word frequencies from any Wikipedia category
- **Real-time Analysis**: Process Wikipedia pages on-the-fly
- **Smart Caching**: Store and retrieve previously analyzed categories
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Natural Language Processing**: Uses NLTK for intelligent word processing
- **User-Friendly Interface**: Simple and intuitive web interface
- **Error Handling**: Graceful error handling and user feedback
- **Performance Optimized**: Efficient data processing and caching

## 🛠️ Tech Stack

### Backend
- Python 3.x
- Flask (Web Framework)
- NLTK (Natural Language Processing)
- Wikipedia API
- JSON for data storage

### Frontend
- HTML5
- CSS3
- JavaScript
- D3.js (Data Visualization)
- D3 Cloud Layout

## 📋 Prerequisites

- Python 3.x
- pip (Python package manager)
- Modern web browser with JavaScript enabled

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wikipedia-word-cloud.git
cd wikipedia-word-cloud
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Start the Flask application:
```bash
cd wiki_word_cloud
python app.py
```

4. Open your web browser and navigate to:
```
http://localhost:5000
```

## 💡 Usage

1. Enter a Wikipedia category name (e.g., "Artificial Intelligence", "Machine Learning")
2. Set the number of words to display (default: 100)
3. Choose whether to use cached data if available
4. Click "Analyze" to generate the word cloud
5. Hover over words to see their frequencies
6. Click on cached categories to quickly load previous analyses

## 🔧 Project Structure

```
wikipedia-word-cloud/
├── wiki_word_cloud/           # Web application
│   ├── app.py                # Flask application
│   ├── static/               # Static files
│   │   ├── css/             # Stylesheets
│   │   └── js/              # JavaScript files
│   └── templates/           # HTML templates
├── wiki_word_frequency/      # Core functionality
│   ├── wiki_analyzer.py     # Main analysis script
│   └── cache/              # Cached results
└── requirements.txt         # Python dependencies
```

## 🔍 How It Works

1. **Category Analysis**:
   - Fetches all pages from the specified Wikipedia category
   - Extracts text content from each page
   - Processes text using NLTK for word frequency analysis

2. **Word Processing**:
   - Removes common words (stopwords)
   - Handles special characters and formatting
   - Calculates word frequencies

3. **Visualization**:
   - Generates interactive word clouds using D3.js
   - Word size represents frequency
   - Color-coded for better visualization
   - Hover effects for detailed information

4. **Caching System**:
   - Stores analyzed categories for faster retrieval
   - Cache expires after 7 days
   - Can be disabled for fresh analysis

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Wikipedia API for providing access to article data
- D3.js community for the word cloud layout
- NLTK for natural language processing capabilities
- DeepLearning.AI for the learning resources

## 📞 Support

If you encounter any issues or have questions, please open an issue in the GitHub repository.

## 🔄 Updates

- Version 1.0.0: Initial release
- Added responsive design
- Implemented caching system
- Enhanced error handling
- Improved word cloud visualization

---
