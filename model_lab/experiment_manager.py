"""
TTHG - Immutable Experiment Tracker
Records training experiments, parameter variance, metrics, loss curves, and hardware stats.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List


class ExperimentManager:
    """Tracks training experiments with immutable run IDs (EXP-000001, EXP-000002)."""

    def __init__(self, experiments_dir: Path):
        self.experiments_dir = experiments_dir
        self.experiments_dir.mkdir(parents=True, exist_ok=True)

    def generate_exp_id(self) -> str:
        existing = list(self.experiments_dir.glob("EXP-*.json"))
        next_num = len(existing) + 1
        return f"EXP-{next_num:06d}"

    def create_experiment(
        self,
        base_model: str,
        dataset_version: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        exp_id = self.generate_exp_id()
        exp_record = {
            "exp_id": exp_id,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "base_model": base_model,
            "dataset_version": dataset_version,
            "params": params,
            "status": "QUEUED",
            "epochs_completed": 0,
            "total_epochs": params.get("epochs", 10),
            "loss_history": [],
            "metrics": {
                "f1_score": 0.0,
                "precision": 0.0,
                "recall": 0.0,
                "temporal_iou": 0.0
            },
            "human_evaluation_score": 0.0
        }

        self.save_experiment(exp_record)
        return exp_record

    def save_experiment(self, exp_record: Dict[str, Any]):
        exp_file = self.experiments_dir / f"{exp_record['exp_id']}.json"
        with open(exp_file, "w", encoding="utf-8") as f:
            json.dump(exp_record, f, indent=2)

    def list_experiments(self) -> List[Dict[str, Any]]:
        exps = []
        for file in sorted(self.experiments_dir.glob("EXP-*.json"), reverse=True):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    exps.append(json.load(f))
            except Exception:
                pass
        return exps
