# NewsAnalyzer

[Live Demo](https://huggingface.co/spaces/YOUR_USERNAME/NewsAnalyzer)

NewsAnalyzer is a web application that analyzes news articles using natural language processing (NLP) techniques. It helps users quickly understand the sentiment, key topics, and overall trends in the latest news based on any search query.

## Features

- Search for recent news articles using NewsAPI
- Perform sentiment analysis to determine whether each article is positive or negative
- Automatically categorize articles into topics such as business, technology, politics, and more
- Generate concise summaries for each article
- Extract the most frequently mentioned words and display them in a word cloud
- Visualize sentiment distribution and trending words in clear charts
- Cache recent searches for improved performance

## Technologies

- **Flask** for backend logic and routing
- **Hugging Face Transformers** for NLP tasks:
    - Sentiment analysis: [distilbert-base-uncased-finetuned-sst-2-english](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english)
    - Topic classification: [cardiffnlp/tweet-topic-21-multi](https://huggingface.co/cardiffnlp/tweet-topic-21-multi)
    - Summarization: [facebook/bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn)
- **NLTK** for tokenization and text preprocessing
- **Matplotlib** and **WordCloud** for visualizations
- **NewsAPI** for retrieving real-time news articles

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ihaveaplan66/news-analyzer.git
    cd NewsAnalyzer
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate   # Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set your NewsAPI key in `app.py`:
    ```python
    api_key = "your_newsapi_key_here"
    ```

5. Run the application:
    ```bash
    python app.py
    ```

6. Open the application in your browser:
    ```
    http://localhost:5000
    ```

## License

This project is part of my personal portfolio and is provided under the MIT License.

## Author

Created by Volodymyr Shereperov
