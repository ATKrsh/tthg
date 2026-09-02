"""
TTHG - Filename Weak Metadata Parser & Alias Normalizer
Extracts candidate concepts from video filenames without treating them as ground truth.
Normalizes abbreviations, separators, and aliases to canonical taxonomy terms.
"""

import re
from typing import List, Dict, Set, Any

# Canonical Alias Mapping Dictionary
ALIAS_DICTIONARY: Dict[str, str] = {
    "pov": "POV",
    "pointofview": "POV",
    "point_of_view": "POV",
    "hd": "1080p",
    "fhd": "1080p",
    "4k": "2160p",
    "uhd": "2160p",
    "solo": "SOLO",
    "duo": "TWO_PERSON",
    "group": "GROUP",
    "indoor": "INDOOR",
    "outdoor": "OUTDOOR",
    "bedroom": "BEDROOM",
    "bathroom": "BATHROOM",
    "office": "OFFICE",
    "studio": "STUDIO",
    "amateur": "AMATEUR",
    "professional": "PROFESSIONAL",
    "staged": "STAGED",
}


class FilenameParser:
    """Parses filenames for weak-label candidate concepts and normalizes terms."""

    @staticmethod
    def clean_filename(filename: str) -> str:
        """Strip file extension and sanitize separators."""
        name = re.sub(r"\.[a-zA-Z0-9]+$", "", filename)  # strip extension
        name = re.sub(r"[_\-\.\+]", " ", name)  # replace separators with space
        return name.strip()

    @classmethod
    def parse_candidate_terms(cls, filename: str) -> Dict[str, Any]:
        """Extract candidate taxonomy terms, resolution, and unknown tokens from filename.

        Returns
        -------
        Dict[str, Any]
            Dict containing canonical_tags, candidate_terms, and raw_tokens.
        """
        cleaned = cls.clean_filename(filename)
        raw_tokens = [tok.lower().strip() for tok in cleaned.split() if tok.strip()]

        canonical_tags: Set[str] = set()
        unknown_terms: List[str] = []

        for token in raw_tokens:
            if token in ALIAS_DICTIONARY:
                canonical_tags.add(ALIAS_DICTIONARY[token])
            elif len(token) >= 3 and not token.isdigit():
                unknown_terms.append(token)

        return {
            "cleaned_name": cleaned,
            "raw_tokens": raw_tokens,
            "canonical_tags": sorted(list(canonical_tags)),
            "unknown_candidate_terms": sorted(list(set(unknown_terms)))
        }
