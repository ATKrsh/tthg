"""
TTHG - Versioned Prompt Library Manager
Stores structured prompts for observation, activity recognition, tagging, verification, and domain analysis.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class PromptManager:
    """Manages versioned prompts under tthg/prompts/."""

    def __init__(self, prompts_dir: Path):
        self.prompts_dir = prompts_dir
        self.prompts_dir.mkdir(parents=True, exist_ok=True)
        self.init_default_prompts()

    def init_default_prompts(self):
        defaults = {
            "observation_v1": {
                "prompt_id": "obs_001",
                "version": "1.0",
                "purpose": "Visual observation extraction",
                "text": "Extract factual visual observations including people, environment, objects, and viewpoint."
            },
            "activity_v1": {
                "prompt_id": "act_001",
                "version": "1.0",
                "purpose": "Activity recognition",
                "text": "Identify distinct physical activities and timestamp intervals factually."
            },
            "tagging_v1": {
                "prompt_id": "tag_001",
                "version": "1.0",
                "purpose": "Controlled taxonomy tagging",
                "text": "Assign controlled taxonomy tags with confidence scores based strictly on visual evidence."
            }
        }

        for name, p_data in defaults.items():
            p_file = self.prompts_dir / f"{name}.json"
            if not p_file.exists():
                with open(p_file, "w", encoding="utf-8") as f:
                    json.dump(p_data, f, indent=2)

    def list_prompts(self) -> List[Dict[str, Any]]:
        prompts = []
        for file in sorted(self.prompts_dir.glob("*.json")):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    prompts.append(json.load(f))
            except Exception:
                pass
        return prompts
