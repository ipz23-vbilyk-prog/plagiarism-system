from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(new_text: str, existing_texts: list[str]):
    if not existing_texts:
        return []

    texts = existing_texts + [new_text]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts).toarray()

    new_vector = vectors[-1]
    old_vectors = vectors[:-1]

    scores = cosine_similarity([new_vector], old_vectors)[0]

    return scores.tolist()


def get_plagiarism_level(score):
    if score < 0.3:
        return "low"
    elif score < 0.7:
        return "medium"
    else:
        return "high"


# 🔥 КЛЮЧОВЕ — “псевдо Turnitin matching”
def find_text_matches(new_text: str, existing_texts: list[str]):
    matches = []

    new_words = set(new_text.lower().split())

    for text in existing_texts:
        if not text:
            continue

        old_words = set(text.lower().split())

        common = list(new_words.intersection(old_words))

        if len(common) > 5:
            matches.append(" ".join(common[:20]))

    return matches