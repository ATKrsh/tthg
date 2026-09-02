"""
TTHG - Document Extractor & Quality Scorer
Normalizes HTML/text content into internal Document format and calculates quality and relevance scores.
"""

from typing import Dict, Any


class ContentExtractor:
    """Normalizes extracted content and evaluates source quality & topic relevance."""

    @staticmethod
    def process_and_score(doc_raw: Dict[str, Any], topic: str) -> Dict[str, Any]:
        text = doc_raw.get("extracted_text", "")
        url = doc_raw.get("source_url", "")

        # Calculate quality & relevance score
        length_score = min(1.0, len(text) / 500.0)
        relevance_score = 1.0 if topic.lower() in text.lower() or topic.lower() in url.lower() else 0.7

        overall_quality = round(length_score * relevance_score, 2)

        return {
            "source_url": url,
            "title": doc_raw.get("title", "Untitled Document"),
            "topic": topic,
            "text": text,
            "quality_score": overall_quality,
            "relevance_score": relevance_score,
            "provenance": {
                "source_url": url,
                "timestamp": doc_raw.get("timestamp"),
                "policy": doc_raw.get("policy", "ALLOWED")
            }
        }
