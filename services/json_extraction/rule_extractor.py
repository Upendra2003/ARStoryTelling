import string
"""
Module 3 — Rule-Based Extractor
SHRI Project · RISHA Lab · IIT Tirupati
"""

import re
from collections import Counter


HINDU_TITLES = [
    "King", "Queen", "Prince", "Princess", "Emperor", "Empress",
    "Maharaja", "Maharani", "Lord", "God", "Goddess", "Sage",
    "Rishi", "Muni", "Swami", "Brahmana", "Saint", "Devotee",
    "Demon", "Asura", "Daitya", "Danava", "Noble", "Great",
    "Divine", "Holy"
]

INTENTIONAL_VERBS = [
    "said", "spoke", "replied", "asked", "told", "declared", "prayed",
    "went", "came", "arrived", "entered", "left", "returned",
    "took", "gave", "offered", "received", "granted", "refused",
    "fought", "attacked", "defended", "protected", "saved",
    "looked", "saw", "heard", "felt", "thought", "decided",
    "ordered", "commanded", "blessed", "cursed", "worshipped"
]

# Comprehensive stop words — pronouns, question words, common sentence starters
STOP_WORDS = {
    # Pronouns
    "He", "She", "They", "It", "Him", "Her", "His", "Their", "Its",
    "We", "You", "Me", "My", "Our", "Your", "Them",
    # Question words
    "How", "What", "Why", "When", "Where", "Who", "Which",
    # Common sentence starters
    "The", "This", "That", "These", "Those", "Then", "When", "While",
    "Once", "One", "Two", "Three", "Soon", "After", "Before", "Long",
    "Just", "Now", "But", "And", "So", "In", "On", "At", "To", "For",
    "Of", "With", "From", "By", "As", "An", "A", "Today", "All",
    "Although", "Nevertheless", "Everyone", "Please", "There",
    "Therefore", "Even", "Also", "Here", "Both", "Each", "True",
    "False", "Any", "Some", "Being", "Having", "Not", "Take", "Such",
    "Dear", "If", "Although", "However", "Hence", "Thus", "Since",
    "Though", "Yet", "Still", "Indeed", "Perhaps", "Maybe", "Surely",
    # Common words in scripture translations
    "Lord", "King", "Guru", "Dear",
}


def extract_diacritic_names(text: str) -> set:
    """Detect Sanskrit names with diacritical marks."""
    found = set()
    words = text.split()
    for word in words:
        word = word.strip(string.punctuation + " ")
        if not word or len(word) < 4:
            continue
        if not word[0].isupper():
            continue
        if word in STOP_WORDS:
            continue
        has_diacritic = any(ord(c) > 127 for c in word)
        if has_diacritic:
            found.add(word)
    return found


def extract_candidates(raw_text: str) -> list:
    candidates = set()

    # Rule 1: Title-prefix
    candidates.update(_extract_by_title_prefix(raw_text))

    # Rule 2: Verb subject
    candidates.update(_extract_by_verb_subject(raw_text))

    # Rule 3: Repeated proper nouns
    candidates.update(_extract_repeated_proper_nouns(raw_text))

    # Rule 4: Sanskrit diacritic names
    candidates.update(extract_diacritic_names(raw_text))

    return _clean_candidates(candidates, raw_text)


def _extract_by_title_prefix(text: str) -> set:
    found = set()
    for title in HINDU_TITLES:
        pattern = re.compile(
            rf"\b{title}\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\b"
        )
        for match in pattern.findall(text):
            name = " ".join(match.split()[:2])
            found.add(name)
    return found


def _extract_by_verb_subject(text: str) -> set:
    found = set()
    for verb in INTENTIONAL_VERBS:
        pattern = re.compile(
            rf"\b([A-Z][a-zA-Z]{{2,}}(?:\s+[A-Z][a-zA-Z]+)?)\s+{verb}\b"
        )
        for match in pattern.findall(text):
            name = match.strip()
            if len(name) > 2 and name not in STOP_WORDS:
                found.add(name)
    return found


def _extract_repeated_proper_nouns(text: str, min_occurrences: int = 2) -> set:
    all_caps = re.findall(r"\b([A-Z][a-zA-Z]{2,})\b", text)
    counts   = Counter(all_caps)
    found    = set()
    for word, count in counts.items():
        if count >= min_occurrences and word not in STOP_WORDS:
            found.add(word)
    return found


def _clean_candidates(candidates: set, text: str) -> list:
    candidates  = {c.strip() for c in candidates if c.strip()}
    text_lower  = text.lower()
    candidates  = {c for c in candidates if c.lower() in text_lower}

    canonical = {}
    for name in candidates:
        last_word = name.split()[-1]
        if last_word not in canonical:
            canonical[last_word] = name
        else:
            if len(name) > len(canonical[last_word]):
                canonical[last_word] = name

    return sorted(set(canonical.values()))


if __name__ == "__main__":
    sample = """While Bali silently heard his guru, Śukrācārya cited more reasons.
    Bali thought about it. I am the grandson of Prahlāda.
    Him and How should not appear. There is nothing sinful."""
    print("Candidates:", extract_candidates(sample))