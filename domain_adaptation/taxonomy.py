"""
TTHG - Local Taxonomy & Domain Ontology Manager
Manages structured taxonomy terms, relationships, and candidate term discovery.
"""

from typing import List, Dict, Set, Any


class TaxonomyManager:
    """Manages domain terms, relationships, and candidate term suggestions."""

    def __init__(self):
        self.domain_terms: Set[str] = {
            "POV", "SOLO", "TWO_PERSON", "GROUP",
            "INDOOR", "OUTDOOR", "BEDROOM", "BATHROOM", "OFFICE", "STUDIO",
            "AMATEUR", "PROFESSIONAL", "STAGED", "1080p", "2160p"
        }
        self.candidate_terms: Dict[str, int] = {}
        self.relationships: List[Dict[str, str]] = [
            {"term": "BEDROOM", "relation": "belongs_to", "target": "INDOOR"},
            {"term": "BATHROOM", "relation": "belongs_to", "target": "INDOOR"},
            {"term": "OFFICE", "relation": "belongs_to", "target": "INDOOR"},
            {"term": "SOLO", "relation": "incompatible_with", "target": "TWO_PERSON"},
        ]

    def register_unknown_term(self, term: str):
        """Track recurring candidate terms across analyzed files."""
        clean = term.strip().lower()
        if clean and clean.upper() not in self.domain_terms:
            self.candidate_terms[clean] = self.candidate_terms.get(clean, 0) + 1

    def list_candidate_terms(self, min_occurrences: int = 2) -> List[Dict[str, Any]]:
        """Return candidate terms meeting occurrence thresholds for user review."""
        candidates = []
        for term, count in self.candidate_terms.items():
            if count >= min_occurrences:
                candidates.append({"term": term, "occurrences": count})
        return sorted(candidates, key=lambda x: x["occurrences"], reverse=True)

    def accept_candidate_term(self, term: str) -> bool:
        """Promote a candidate term to the formal domain taxonomy."""
        upper = term.strip().upper()
        self.domain_terms.add(upper)
        if term.lower() in self.candidate_terms:
            del self.candidate_terms[term.lower()]
        return True
