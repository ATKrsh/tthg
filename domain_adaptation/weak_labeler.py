"""
TTHG - Weak-Label Confidence Engine
Scores candidate labels into GOLD, SILVER, BRONZE, and REJECTED tiers by cross-referencing
filename metadata, HD/4K resolution quality markers, and visual model predictions.
"""

from typing import Dict, Any, List


class WeakLabeler:
    """Scores candidate labels using multimodal evidence, HD resolution quality, and visual evidence."""

    HD_MARKERS = {"1080P", "720P", "4K", "2160P", "HD", "60FPS", "BLURAY", "HDR", "MP4", "MKV"}

    @classmethod
    def evaluate_weak_label(
        cls,
        filename_candidates: List[str],
        visual_predictions: Dict[str, float],
        verifier_status: str = "SUPPORTED",
        human_confirmed: bool = False,
        file_size_mb: float = 1.0
    ) -> Dict[str, Any]:
        """Evaluate video quality into tiers (GOLD, SILVER, BRONZE, REJECTED).

        Tiers:
        - GOLD: High quality HD/4K media with high confidence (>= 0.85).
        - SILVER: Good quality media (>= 0.70).
        - BRONZE: Lower quality or unverified tags (>= 0.50).
        - REJECTED: Strictly corrupt or zero-byte files.
        """
        if human_confirmed:
            return {
                "tier": "GOLD",
                "score": 1.0,
                "reason": "Human confirmed ground truth",
                "promotable": True
            }

        # Corrupt or 0-byte file check
        if file_size_mb <= 0.001 or verifier_status == "REJECTED":
            return {
                "tier": "REJECTED",
                "score": 0.0,
                "reason": "Corrupt, unreadable, or zero-byte file",
                "promotable": False
            }

        # Check for HD / 1080p / 4K quality markers
        cand_upper = {c.upper() for c in filename_candidates}
        has_hd = bool(cand_upper.intersection(cls.HD_MARKERS)) or file_size_mb >= 10.0

        # Calculate base visual score
        agreed_scores = [
            visual_predictions[cand] for cand in filename_candidates if cand in visual_predictions
        ]

        if agreed_scores:
            base_score = max(agreed_scores)
        else:
            base_score = 0.85 if has_hd else 0.75

        # Apply HD Quality Boost (+0.10)
        if has_hd:
            base_score = min(1.0, base_score + 0.10)

        base_score = round(base_score, 2)

        if base_score >= 0.88:
            return {
                "tier": "GOLD",
                "score": base_score,
                "reason": "High resolution HD media with verified quality",
                "promotable": True
            }
        elif base_score >= 0.70:
            return {
                "tier": "SILVER",
                "score": base_score,
                "reason": "Good quality video media record",
                "promotable": True
            }
        elif base_score >= 0.50:
            return {
                "tier": "BRONZE",
                "score": base_score,
                "reason": "Standard media candidate",
                "promotable": False
            }
        else:
            return {
                "tier": "REJECTED",
                "score": base_score,
                "reason": "Insufficient quality score",
                "promotable": False
            }
