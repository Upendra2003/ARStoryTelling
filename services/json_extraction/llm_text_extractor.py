"""
Module 4a — Text LLM Extractor
SHRI Project · RISHA Lab · IIT Tirupati
"""

import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GROQ_MODEL   = "llama-3.3-70b-versatile"


def extract_from_text(
    raw_text: str,
    candidate_names: list,
    index_summary: list
) -> dict:

    stories_str    = json.dumps(index_summary, indent=2)
    candidates_str = ", ".join(candidate_names) if candidate_names else "none detected"

    prompt = f"""You are processing a page from Srimad Bhagavatam.

OCR extracted text from the page:
\"\"\"{raw_text}\"\"\"

Character names detected by rule-based NER: {candidates_str}

Known stories in the scaffold library:
{stories_str}

IMPORTANT RULES — read before generating:
1. Only include characters that are actual named persons or beings in the story.
2. Reject any candidate that is a pronoun (Him, He, She, They, It, His, Her).
3. Reject any question word (How, What, Why, When, Where, Who).
4. Reject any common English word that is clearly not a proper name.
5. Reject characters that are only mentioned briefly (like ancestors) and are not present in the scene.
6. For character_id: match EXACTLY to scaffold character_ids provided.
   Known character_ids: bali_chakravarti, vamana, shukracharya, vishnu, garuda, gajendra, huhu.
   If a character is "Bali" match to "bali_chakravarti".
   If not in scaffold use snake_case of their name.
7. Do NOT invent character physical attributes.

Return ONLY valid JSON, no explanation, no markdown:

{{
  "story_id": "<match to one of the story_ids above>",
  "skandha": "<skandha number as string>",
  "characters": [
    {{
      "name": "<exact name as it appears in text>",
      "character_id": "<match to scaffold character_id exactly>",
      "narrative_role": "<protagonist | antagonist | supporting>",
      "posture": "<what the character is physically doing in this scene>",
      "clothing_override": "<only if text explicitly mentions clothing, else null>"
    }}
  ],
  "events": [
    {{
      "id": "event_1",
      "sequence_order": 1,
      "source_text": "<exact sentence this event comes from>",
      "action_type": "<locomotion | reaction | interaction | gesture | transformation>",
      "action": "<core action description>",
      "action_modifier": "<tone or manner of action>",
      "duration": "<continuous | instantaneous | gradual>",
      "participants": [
        {{
          "character": "<character_id>",
          "action": "<what this character specifically does>"
        }}
      ]
    }}
  ]
}}"""

    client   = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role"   : "system",
                "content": "You are a structured data extractor for Hindu scripture text. Return only valid JSON, no explanation, no markdown fences."
            },
            {
                "role"   : "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=1500
    )

    raw_response = response.choices[0].message.content.strip()

    if raw_response.startswith("```"):
        raw_response = raw_response.split("```")[1]
        if raw_response.startswith("json"):
            raw_response = raw_response[4:]
    raw_response = raw_response.strip()

    try:
        result = json.loads(raw_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}\nResponse: {raw_response}")

    return result


if __name__ == "__main__":
    from scaffold_loader import get_index_summary
    from rule_extractor import extract_candidates

    sample_text = """While Bali silently heard his guru, Sukracarya cited more reasons.
    Bali thought about it. I am the grandson of Prahlada.
    How can I withdraw my promise?"""

    candidates = extract_candidates(sample_text)
    index      = get_index_summary()
    result     = extract_from_text(sample_text, candidates, index)
    print(json.dumps(result, indent=2))