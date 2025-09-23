import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Text preprocessing
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return " ".join(text.split())

# Recommendation logic
def get_recommendations(qualification, skills, languages, df):
    # Combine fields with weighted importance: Qualification (3x), Skills (2x), Languages (1x)
    df["combined_features"] = (
        df["Required Qualifications"].apply(preprocess_text).str.repeat(3) + " " +
        df["Required Skills"].apply(preprocess_text).str.repeat(2) + " " +
        df["Programming Languages"].apply(preprocess_text)
    )

    # User profile input
    user_input = f"{qualification} {' '.join(skills)} {' '.join(languages)}"
    user_input_processed = preprocess_text(user_input)

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", max_features=500)
    tfidf_matrix = vectorizer.fit_transform(df["combined_features"])
    user_vector = vectorizer.transform([user_input_processed])

    # Cosine similarity scoring
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    df["similarity_score"] = similarities

    # Select top 3 distinct job roles, each with top matches
    top_matches = df.sort_values(by="similarity_score", ascending=False)
    recommendations = []
    seen_roles = set()

    for _, row in top_matches.iterrows():
        if len(seen_roles) >= 3:
            break
        role = row["Job Title"]
        if role not in seen_roles:
            role_group = top_matches[top_matches["Job Title"] == role].head(1)
            recommendations.append(role_group)
            seen_roles.add(role)

    result_df = pd.concat(recommendations).drop(columns=["combined_features", "similarity_score"])
    return result_df.reset_index(drop=True)
