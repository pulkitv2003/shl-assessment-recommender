from flask import Flask, request, jsonify
from backend.recommender import get_recommendations

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"}), 200

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    query = data.get("query", "")
    print("Received query:", query)  # Debug log
    recommendations = get_recommendations(query)
    print("Top Recommendation:", recommendations[0] if recommendations else "None")
    return jsonify({"recommendations": recommendations}), 200

if __name__ == "__main__":
    app.run(debug=True)
