"""
Module 2 — Scaffold Loader
SHRI Project · RISHA Lab · IIT Tirupati
"""

import json
import os

SCAFFOLD_DIR = os.path.join(os.path.dirname(__file__), "scaffolds")

# Alias map — common name variants → canonical character_id
CHARACTER_ALIASES = {
    "bali"           : "bali_chakravarti",
    "mahabali"       : "bali_chakravarti",
    "sukracharya"    : "shukracharya",
    "shukra"         : "shukracharya",
    "sukra"          : "shukracharya",
    "trivikrama"     : "vamana",
    "urukrama"       : "vamana",
    "hari"           : "vishnu",
    "narayana"       : "vishnu",
    "the_lord"       : "vishnu",
    "prahlada"       : "prahlada",
    "prahlāda"       : "prahlada",
}


def resolve_character_id(character_id: str) -> str:
    """Resolve character_id aliases to canonical scaffold filename."""
    key = character_id.lower().replace(" ", "_")
    return CHARACTER_ALIASES.get(key, key)


def load_index() -> dict:
    index_path = os.path.join(SCAFFOLD_DIR, "index.json")
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_story(story_id: str) -> dict:
    story_path = os.path.join(SCAFFOLD_DIR, "stories", f"{story_id}.json")
    if not os.path.exists(story_path):
        raise FileNotFoundError(f"Story scaffold not found: {story_id}")
    with open(story_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_character(character_id: str) -> dict:
    """Load character scaffold, resolving aliases automatically."""
    resolved  = resolve_character_id(character_id)
    char_path = os.path.join(SCAFFOLD_DIR, "characters", f"{resolved}.json")
    if not os.path.exists(char_path):
        return None
    with open(char_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_for_story(story_id: str) -> dict:
    story      = load_story(story_id)
    characters = {}
    for char_id in story.get("characters", []):
        char_data = load_character(char_id)
        if char_data:
            characters[char_id] = char_data
    return {"story": story, "characters": characters}


def get_index_summary() -> list:
    index   = load_index()
    summary = []
    for s in index.get("stories", []):
        summary.append({
            "story_id"  : s["story_id"],
            "story_name": s["story_name"],
            "skandha"   : s["skandha"],
            "key_terms" : s["key_terms"]
        })
    return summary


if __name__ == "__main__":
    # Test alias resolution
    print("bali →", resolve_character_id("bali"))
    print("Sukracarya →", resolve_character_id("sukracharya"))
    print("Trivikrama →", resolve_character_id("trivikrama"))

    summary = get_index_summary()
    print("\nKnown stories:")
    for s in summary:
        print(f"  {s['story_id']}")