import requests
from collections import Counter
from transformers import pipeline
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')


# 1. Function for getting news via NewsAPI
def get_news(query, api_key, num_articles=5):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&language=en&pageSize={num_articles}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['articles']
    return []


# 2. Analyzing tone with Hugging Face
tone_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", revision="714eb0f")

def analyze_sentiment(text):
    return tone_analyzer(text)[0]


# 3. Define category

category_model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/tweet-topic-21-multi")
category_tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/tweet-topic-21-multi")
labels = ['art', 'business', 'entertainment', 'environment', 'fashion', 'finance', 'food',
          'health', 'law', 'media', 'military', 'music', 'politics', 'religion', 'sci/tech',
          'sports', 'travel', 'weather', 'world news', 'none']

def classify_category(text):
    inputs = category_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = category_model(**inputs)
    predicted_class = torch.argmax(outputs.logits, dim=1).item()
    return labels[predicted_class]


# 4. Summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def split_text(text, max_tokens=512):
    words = text.split()
    return [' '.join(words[i:i+max_tokens]) for i in range(0, len(words), max_tokens)]

def summarize_text(text):
    chunks = split_text(text)
    summaries = [summarizer(chunk, max_length=100, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks]
    return ' '.join(summaries)


# 5. Search for trending words
def extract_trending_words(texts):
    text = ' '.join(texts).lower()
    words = word_tokenize(text)
    words = [word for word in words if word not in stopwords.words('english') and word not in string.punctuation and len(word) > 1]
    word_freq = Counter(words)
    return word_freq.most_common(10)

# 6. The main process of analyzing news
def analyze_news(query, api_key, num_articles=5):
    articles = get_news(query, api_key, num_articles)

    if not articles:
        return []

    news_results = []
    for article in articles:
        title = article.get('title', 'No Title')
        description = article.get('description', '') or ''
        url = article.get('url', '#')

        sentiment = analyze_sentiment(title + " " + description)['label']
        category = classify_category(title + " " + description)
        summary = summarize_text(title + " " + description)

        news_results.append({
            "title": title,
            "url": url,
            "sentiment": sentiment,
            "category": category,
            "summary": summary
        })

    return news_results

