import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load catalog
catalog_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'shl_catalog.json')
with open(catalog_path, encoding='utf-8') as f:
    catalog = json.load(f)

# Prepare corpus for TF-IDF: one sentence per catalog entry
corpus = []
for item in catalog:
    text = item["name"] + " " + item["type"] + " " + " ".join(item["keywords"])
    corpus.append(text.lower())

# Fit TF-IDF vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

def get_recommendations(query, top_k=10):
    query = query.lower()
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    top_indices = similarities.argsort()[::-1][:top_k]
    results = []

    for idx in top_indices:
        if similarities[idx] == 0:
            continue  # Skip zero matches
        item = catalog[idx]
        results.append({
            "name": item["name"],
            "url": item["url"],
            "remote_support": item["remote_support"],
            "adaptive_support": item["adaptive_support"],
            "duration": item["duration"],
            "type": item["type"],
            "score": round(float(similarities[idx]), 3)
        })

    return results
