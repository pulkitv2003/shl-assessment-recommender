import sys
import os

# Add parent directory to path to access backend module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.recommender import get_recommendations

# Test queries and their expected relevant assessment names (from SHL PDF)
test_data = [
    {
        "query": "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.",
        "relevant": [
            "Automata - Fix (New)", "Core Java (Entry Level) (New)", 
            "Java 8 (New)", "Core Java (Advanced Level) (New)", 
            "Agile Software Development"
        ]
    },
    {
        "query": "I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test.",
        "relevant": [
            "Entry level Sales 7.1 (International)", "Entry Level Sales Sift Out 7.1",
            "Entry Level Sales Solution", "Sales Representative Solution",
            "Sales Support Specialist Solution"
        ]
    }
    # You can add more test cases as needed
]

K = 3  # Top K results to consider

def recall_at_k(predicted, relevant):
    relevant_set = set(relevant)
    top_k_set = set(predicted[:K])
    return len(top_k_set & relevant_set) / len(relevant_set)

def map_at_k(predicted, relevant):
    score = 0.0
    hits = 0
    for i, pred in enumerate(predicted[:K]):
        if pred in relevant:
            hits += 1
            score += hits / (i + 1)
    return score / min(len(relevant), K)

def evaluate():
    recall_scores = []
    map_scores = []

    for item in test_data:
        query = item["query"]
        relevant = item["relevant"]

        recommendations = get_recommendations(query, top_k=K)
        predicted_names = [rec["name"] for rec in recommendations]

        recall = recall_at_k(predicted_names, relevant)
        ap = map_at_k(predicted_names, relevant)

        print(f"\nQuery: {query}")
        print(f"Recall@{K}: {recall:.3f}")
        print(f"MAP@{K}: {ap:.3f}")

        recall_scores.append(recall)
        map_scores.append(ap)

    mean_recall = sum(recall_scores) / len(recall_scores)
    mean_map = sum(map_scores) / len(map_scores)

    print("\n=== FINAL SCORES ===")
    print(f"Mean Recall@{K}: {mean_recall:.3f}")
    print(f"Mean MAP@{K}: {mean_map:.3f}")

if __name__ == "__main__":
    evaluate()
