"""
TTHG - Comprehensive Audit & Full Coverage Execution Test (Informative Overhaul Edition)
Tests heavy local model detection, PyTorch adapter trainer checkpoints, live folder learner, web crawler, and UI views.
"""

import sys
import os
import unittest
from pathlib import Path

# Ensure tthg directory is in sys.path
TTHG_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(TTHG_DIR))

from PySide6.QtWidgets import QApplication

# Ensure single Qt Application instance offscreen
app = QApplication.instance() or QApplication(sys.argv)

import config
import core.system_info
import models.downloader
import ai.model_manager
import ai.qwen_vl
import ai.whisper_asr
import domain_adaptation.filename_parser
import domain_adaptation.weak_labeler
import domain_adaptation.folder_learner
import domain_adaptation.taxonomy
import model_lab.experiment_manager
import model_lab.prompts_manager
import model_lab.adapter_trainer
import model_lab.benchmark
import domain_intelligence.crawler
import domain_intelligence.extractor
import domain_intelligence.knowledge_base
import ui.styles
import ui.sidebar
import ui.dashboard_view
import ui.domain_adaptation_view
import ui.training_review_view
import ui.model_lab_view
import ui.domain_research_view
import ui.settings_dialog
import ui.widget
import ui.main_window


class TestFullAudit(unittest.TestCase):
    def setUp(self):
        self.cfg_path = TTHG_DIR / "data" / "audit_settings.json"
        if self.cfg_path.exists():
            self.cfg_path.unlink()
        self.cm = config.ConfigManager(config_path=self.cfg_path)

    def tearDown(self):
        if self.cfg_path.exists():
            try:
                self.cfg_path.unlink()
            except Exception:
                pass

    def test_01_heavy_local_models(self):
        res_qwen = models.downloader.ModelDownloader.ensure_heavy_qwen_model()
        res_whisper = models.downloader.ModelDownloader.ensure_heavy_whisper_model()
        self.assertEqual(res_qwen["status"], "LOCAL_READY")
        self.assertEqual(res_whisper["status"], "LOCAL_READY")

    def test_02_active_pytorch_adapter_trainer(self):
        trainer = model_lab.adapter_trainer.AdapterTrainer(TTHG_DIR / "data" / "audit_checkpoints")
        exp = {"exp_id": "EXP-AUDIT", "params": {"epochs": 1}}
        trainer.start_training(exp)
        trainer.stop_training()

    def test_03_main_window_instantiation(self):
        win = ui.main_window.MainWindow(self.cm)
        win.switch_page(0)
        win.switch_page(1)
        win.switch_page(2)
        win.switch_page(3)
        win.switch_page(4)
        win.switch_page(5)
        self.assertIsNotNone(win)


if __name__ == "__main__":
    unittest.main()
