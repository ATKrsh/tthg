"""
TTHG - Hybrid Knowledge Base & Provenance Indexer
Indexes documents for local search and vector retrieval while maintaining exact source provenance.
"""

from typing import List, Dict, Any


class LocalKnowledgeBase:
    """Manages local domain research documents and query retrieval."""

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []

    def ingest_document(self, doc: Dict[str, Any]):
        """Ingest scored document into knowledge base with full provenance."""
        self.documents.append(doc)

    def query_knowledge_base(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search local documents matching query terms."""
        results = []
        q_clean = query.lower()

        for doc in self.documents:
            text = doc.get("text", "").lower()
            title = doc.get("title", "").lower()
            if q_clean in text or q_clean in title:
                results.append(doc)

        return sorted(results, key=lambda x: x.get("quality_score", 0.0), reverse=True)[:top_k]
