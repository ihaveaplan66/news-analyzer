from flask import Flask, render_template, request, Response, url_for
from main import analyze_news, extract_trending_words
import io
import time
import matplotlib.pyplot as plt
from wordcloud import WordCloud


app = Flask(__name__)
cache = {}
plt.switch_backend("Agg")

def get_cached_data(cache_key):
    cached = cache.get(cache_key)
    if cached and time.time() - cached["timestamp"] < 600:
        print(f"Cache hit for {cache_key}")
        return cached["results"], cached["trending_words"]
    return None, None

@app.route("/", methods=["GET", "POST"])
def index():
    results, trending_words = [], []
    sentiment_chart = None
    query = ""

    if request.method == "POST":
        query = request.form["query"]
        num_articles = int(request.form["num_articles"])
        api_key = "your_newsapi_key_here"

        cache_key = f"{query}_{num_articles}"
        results, trending_words = get_cached_data(cache_key)

        if results is None:
            print(f"No cache for {cache_key}, fetching new data...")
            results = analyze_news(query, api_key, num_articles)
            texts = [article["title"] + " " + article.get("summary", "") for article in results]
            trending_words = extract_trending_words(texts)

            cache[cache_key] = {
                "results": results,
                "trending_words": trending_words,
                "timestamp": time.time()
            }

        if results:
            sentiment_chart = url_for('sentiment_chart_route')

    return render_template("index.html", results=results, sentiment_chart=sentiment_chart, query=query, trending_words=trending_words)

@app.route("/sentiment_chart")
def sentiment_chart_route():
    if not cache:
        return "No sentiment data", 404

    last_query = list(cache.keys())[-1]
    cached = cache.get(last_query)

    if not cached:
        return "No sentiment data", 404

    results = cached["results"]
    sentiments = [article["sentiment"] for article in results]

    sentiment_counts = dict((x, sentiments.count(x)) for x in set(sentiments))

    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())

    color_map = {
        "POSITIVE": "#28a745",
        "NEGATIVE": "#c82333"
    }

    colors = [color_map[label] for label in labels]
    total = sum(values)

    plt.figure(figsize=(3, 3))
    plt.pie(values, autopct=lambda pct: f'{int(pct * total / 100)} ({pct:.1f}%)', startangle=140, colors=colors)
    plt.axis('equal')

    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight", transparent = True)
    plt.close()
    img.seek(0)

    return Response(img.getvalue(), mimetype="image/png")

@app.route("/wordcloud_chart")
def wordcloud_chart():
    if not cache:
        return "No word data", 404

    last_query = list(cache.keys())[-1]
    cached = cache.get(last_query)

    if not cached:
        return "No word data", 404

    results = cached["results"]
    texts = [article["title"] + " " + article.get("summary", "") for article in results]

    text = " ".join(texts)

    plt.figure(figsize=(16, 8), dpi=150)
    wordcloud = WordCloud(width=1600, height=800, colormap="Blues", background_color='#222').generate(text)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight", pad_inches=0, dpi=150)
    plt.close()
    img.seek(0)

    return Response(img.getvalue(), mimetype="image/png")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
