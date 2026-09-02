"""
TTHG - Configuration & Settings Manager
Strictly scoped to the tthg workspace folder.
Persists settings, hotkeys, widget geometry, and telemetry preferences to tthg/data/settings.json.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

APP_DIR = Path(__file__).parent.resolve()
DATA_DIR = APP_DIR / "data"
LOGS_DIR = APP_DIR / "logs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = DATA_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "hotkey_toggle": "Ctrl+Alt+T",
    "hotkey_mute": "Ctrl+Alt+M",
    "refresh_interval_ms": 1000,
    "widget_position": [150, 150],
    "widget_opacity": 0.92,
    "always_on_top": True,
    "theme": "cyan_glass",
    "show_cpu": True,
    "show_ram": True,
    "show_disk": True,
}


class ConfigManager:
    def __init__(self, config_path: Path = CONFIG_FILE):
        self.config_path = config_path
        self.settings = DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.settings.update(saved)
            except Exception as e:
                print(f"[TTHG.Config] Error loading settings: {e}")

    def save(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"[TTHG.Config] Error saving settings: {e}")

    def get(self, key: str, default=None):
        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        self.settings[key] = value
        self.save()
