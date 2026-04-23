import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from scrapers.amazon_scraper import scrape_amazon
from scrapers.flipkart_scraper import scrape_flipkart
import concurrent.futures

app = Flask(__name__)
CORS(app)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"error": "Please provide a search query"}), 400

    results = []
    errors = []

    # Run both scrapers in parallel so it's faster
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_amazon   = executor.submit(scrape_amazon, query)
        future_flipkart = executor.submit(scrape_flipkart, query)

        try:
            amazon_results = future_amazon.result(timeout=15)
            results.extend(amazon_results)
        except Exception as e:
            errors.append(f"Amazon: {str(e)}")

        try:
            flipkart_results = future_flipkart.result(timeout=15)
            results.extend(flipkart_results)
        except Exception as e:
            errors.append(f"Flipkart: {str(e)}")

    if not results:
        return jsonify({
            "error": "No results found. Try a different search term.",
            "details": errors
        }), 404

    # Sort all results by price (lowest first)
    results.sort(key=lambda x: x.get("price_raw", float("inf")))

    # Mark the best deal
    if results:
        results[0]["best_deal"] = True

    return jsonify({
        "query": query,
        "total": len(results),
        "results": results,
        "errors": errors  # non-fatal, just info
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
