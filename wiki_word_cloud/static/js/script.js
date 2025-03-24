/**
 * Wikipedia Word Cloud Visualizer
 * 
 * This script handles the frontend functionality for the Wikipedia word cloud application,
 * including API calls, data processing, and word cloud visualization using D3.js.
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const searchForm = document.getElementById('search-form');
    const categoryInput = document.getElementById('category-input');
    const topNInput = document.getElementById('top-n-input');
    const useCacheCheckbox = document.getElementById('use-cache');
    const loadingElement = document.getElementById('loading');
    const resultsElement = document.getElementById('results');
    const errorElement = document.getElementById('error');
    const errorMessage = document.getElementById('error-message');
    const resultTitle = document.getElementById('result-title');
    const resultInfo = document.getElementById('result-info');
    const wordCloudElement = document.getElementById('word-cloud');
    const cachedListElement = document.getElementById('cached-list');

    // Load cached categories on page load
    loadCachedCategories();

    // Form submission handler
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const category = categoryInput.value.trim();
        const topN = parseInt(topNInput.value);
        const useCache = useCacheCheckbox.checked;
        
        if (!category) {
            showError('Please enter a Wikipedia category');
            return;
        }
        
        analyzeCategory(category, topN, useCache);
    });

    /**
     * Analyze a Wikipedia category and generate a word cloud
     */
    function analyzeCategory(category, topN, useCache) {
        // Show loading indicator
        showLoading();
        
        console.log(`Analyzing category: ${category}, top ${topN} words, use cache: ${useCache}`);
        
        // Make API request to the Flask backend
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                category: category,
                top_n: topN,
                use_cache: useCache
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || `Server error: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            // Hide loading indicator
            hideLoading();
            
            console.log('Analysis results:', data);
            
            // Check if we have words
            if (!data.words || Object.keys(data.words).length === 0) {
                throw new Error('No words found in this category. Try another category or disable cache.');
            }
            
            // Display results
            displayResults(data);
            
            // Reload cached categories list
            loadCachedCategories();
        })
        .catch(error => {
            console.error('Error during analysis:', error);
            hideLoading();
            showError(error.message);
        });
    }

    /**
     * Display the analysis results and generate word cloud
     */
    function displayResults(data) {
        // Update result information
        resultTitle.textContent = `Category: ${data.category}`;
        resultInfo.textContent = `Found ${Object.keys(data.words).length} words out of ${data.total_words} total unique words (${data.source})`;
        
        // Show results container
        resultsElement.classList.remove('hidden');
        errorElement.classList.add('hidden');
        
        // Generate word cloud
        generateWordCloud(data.words);
    }

    /**
     * Generate a word cloud visualization using D3.js
     */
    function generateWordCloud(words) {
        // Clear previous word cloud
        wordCloudElement.innerHTML = '';
        
        // Convert words object to array format required by d3-cloud
        const wordArray = Object.entries(words).map(([text, value]) => ({ text, value }));
        
        console.log(`Generating word cloud with ${wordArray.length} words`);
        
        if (wordArray.length === 0) {
            wordCloudElement.innerHTML = '<p class="error-message">No words found to display</p>';
            return;
        }
        
        // Get the size of the container
        const width = wordCloudElement.clientWidth;
        const height = 500;
        
        // Find the maximum frequency for scaling
        const maxFreq = Math.max(...wordArray.map(d => d.value));
        
        // Create a color scale
        const color = d3.scaleOrdinal(d3.schemeCategory10);
        
        try {
            // Configure the word cloud layout
            const layout = d3.layout.cloud()
                .size([width, height])
                .words(wordArray)
                .padding(5)
                .rotate(() => ~~(Math.random() * 2) * 90)
                .fontSize(d => Math.sqrt(d.value / maxFreq) * 50 + 10)
                .on('end', draw);
            
            // Start the layout calculation
            layout.start();
            
            // Function to draw the word cloud
            function draw(words) {
                d3.select('#word-cloud')
                    .append('svg')
                    .attr('width', width)
                    .attr('height', height)
                    .append('g')
                    .attr('transform', `translate(${width / 2},${height / 2})`)
                    .selectAll('text')
                    .data(words)
                    .enter()
                    .append('text')
                    .attr('class', 'word-cloud-word')
                    .style('font-size', d => `${d.size}px`)
                    .style('fill', (d, i) => color(i))
                    .attr('text-anchor', 'middle')
                    .attr('transform', d => `translate(${d.x},${d.y}) rotate(${d.rotate})`)
                    .text(d => d.text)
                    .append('title')
                    .text(d => `${d.text}: ${d.value} occurrences`);
            }
        } catch (error) {
            console.error('Error generating word cloud:', error);
            wordCloudElement.innerHTML = `<p class="error-message">Error generating word cloud: ${error.message}</p>`;
        }
    }

    /**
     * Load and display cached categories
     */
    function loadCachedCategories() {
        fetch('/cached-categories')
            .then(response => response.json())
            .then(categories => {
                cachedListElement.innerHTML = '';
                
                if (categories.length === 0) {
                    cachedListElement.innerHTML = '<p>No cached categories found</p>';
                    return;
                }
                
                console.log(`Loaded ${categories.length} cached categories`);
                
                categories.forEach(category => {
                    const element = document.createElement('div');
                    element.className = 'cached-item';
                    element.textContent = category.category;
                    element.title = `Cached on: ${new Date(category.timestamp).toLocaleString()}\nWords: ${category.word_count}`;
                    
                    element.addEventListener('click', () => {
                        categoryInput.value = category.category;
                        analyzeCategory(category.category, parseInt(topNInput.value), true);
                    });
                    
                    cachedListElement.appendChild(element);
                });
            })
            .catch(error => {
                console.error('Error loading cached categories:', error);
                cachedListElement.innerHTML = '<p>Error loading cached categories</p>';
            });
    }

    /**
     * Show loading indicator
     */
    function showLoading() {
        loadingElement.classList.remove('hidden');
        resultsElement.classList.add('hidden');
        errorElement.classList.add('hidden');
    }

    /**
     * Hide loading indicator
     */
    function hideLoading() {
        loadingElement.classList.add('hidden');
    }

    /**
     * Show error message
     */
    function showError(message) {
        errorElement.classList.remove('hidden');
        resultsElement.classList.add('hidden');
        errorMessage.textContent = message;
    }
});
