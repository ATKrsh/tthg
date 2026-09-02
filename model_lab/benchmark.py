"""
TTHG - Benchmark Evaluation & Automated Regression Testing Engine
Calculates F1, Precision, Recall, temporal IoU, and handles Production vs Candidate model promotion logic.
"""

from typing import Dict, Any, List


class BenchmarkEvaluator:
    """Evaluates model performance against held-out benchmark datasets."""

    @staticmethod
    def evaluate_model(predictions: List[Dict[str, Any]], ground_truth: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate Precision, Recall, F1, and Temporal IoU metrics."""
        if not predictions or not ground_truth:
            return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0, "temporal_iou": 0.0}

        true_positives = 0
        false_positives = 0
        false_negatives = 0
        iou_sum = 0.0

        for pred in predictions:
            matched = False
            for gt in ground_truth:
                if pred.get("label") == gt.get("label"):
                    true_positives += 1
                    # Temporal IoU calculation
                    p_start, p_end = pred.get("start", 0), pred.get("end", 1)
                    g_start, g_end = gt.get("start", 0), gt.get("end", 1)
                    intersection = max(0, min(p_end, g_end) - max(p_start, g_start))
                    union = max(p_end, g_end) - min(p_start, g_start)
                    if union > 0:
                        iou_sum += (intersection / union)
                    matched = True
                    break
            if not matched:
                false_positives += 1

        false_negatives = max(0, len(ground_truth) - true_positives)

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        avg_iou = iou_sum / len(predictions) if predictions else 0.0

        return {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "temporal_iou": round(avg_iou, 4)
        }

    @classmethod
    def compare_models(cls, prod_metrics: Dict[str, float], cand_metrics: Dict[str, float]) -> Dict[str, Any]:
        """Compare candidate model vs production model and evaluate promotion eligibility."""
        f1_diff = cand_metrics.get("f1_score", 0.0) - prod_metrics.get("f1_score", 0.0)
        iou_diff = cand_metrics.get("temporal_iou", 0.0) - prod_metrics.get("temporal_iou", 0.0)

        is_improved = f1_diff > 0.01 and iou_diff >= -0.02
        return {
            "prod_f1": prod_metrics.get("f1_score", 0.0),
            "cand_f1": cand_metrics.get("f1_score", 0.0),
            "f1_delta": round(f1_diff, 4),
            "is_improved": is_improved,
            "recommendation": "PROMOTE_TO_PRODUCTION" if is_improved else "REJECT_CANDIDATE"
        }
