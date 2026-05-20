import re


def clean_fragment(text: str) -> str:
    """Очищення шумного тексту"""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,:;()%\-–]', '', text)
    return text.strip()


def get_context(full_text: str, fragment: str, window: int = 120):
    """Витягує контекст до і після фрагмента"""
    idx = full_text.find(fragment)

    if idx == -1:
        return "", ""

    start = max(0, idx - window)
    end = min(len(full_text), idx + len(fragment) + window)

    context = full_text[start:end]

    before = full_text[start:idx]
    after = full_text[idx + len(fragment):end]

    return before.strip(), after.strip()


def build_match(full_text: str, fragment: str, source: str, similarity: float):
    """Формує нормальний результат співпадіння"""

    fragment_clean = clean_fragment(fragment)
    before, after = get_context(full_text, fragment_clean)

    return {
        "similarity": round(similarity * 100, 2),
        "fragment": fragment_clean,
        "source": source,
        "context_before": before,
        "context_after": after
    }