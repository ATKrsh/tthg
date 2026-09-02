"""
TTHG - Comprehensive Automated Unit Test Suite
Tests Domain Adaptation, Filename Intelligence, Weak-Label Scoring, Model Lab, and Domain Research.
"""

import sys
import unittest
from pathlib import Path

# Ensure tthg directory is in sys.path
TTHG_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(TTHG_DIR))

from config import ConfigManager
from core.system_info import SystemInfoCollector
from domain_adaptation.filename_parser import FilenameParser
from domain_adaptation.weak_labeler import WeakLabeler
from domain_adaptation.taxonomy import TaxonomyManager
from model_lab.experiment_manager import ExperimentManager
from model_lab.benchmark import BenchmarkEvaluator
from domain_intelligence.crawler import DomainCrawler, SourcePolicyEngine
from domain_intelligence.extractor import ContentExtractor
from domain_intelligence.knowledge_base import LocalKnowledgeBase


class TestTTHGConfigAndTelemetry(unittest.TestCase):
    def setUp(self):
        self.test_config_path = TTHG_DIR / "data" / "test_settings.json"
        if self.test_config_path.exists():
            self.test_config_path.unlink()
        self.cm = ConfigManager(config_path=self.test_config_path)

    def tearDown(self):
        if self.test_config_path.exists():
            try:
                self.test_config_path.unlink()
            except Exception:
                pass

    def test_telemetry_metrics(self):
        metrics = SystemInfoCollector.get_metrics()
        self.assertIn("cpu_pct", metrics)
        self.assertIn("ram_pct", metrics)


class TestDomainAdaptationEngine(unittest.TestCase):
    def test_filename_parsing(self):
        res = FilenameParser.parse_candidate_terms("Solo_POV_Bedroom_1080p.mp4")
        self.assertIn("POV", res["canonical_tags"])
        self.assertIn("SOLO", res["canonical_tags"])
        self.assertIn("BEDROOM", res["canonical_tags"])

    def test_weak_label_gold_tier(self):
        eval_res = WeakLabeler.evaluate_weak_label(
            filename_candidates=["POV"],
            visual_predictions={"POV": 0.94},
            verifier_status="SUPPORTED"
        )
        self.assertEqual(eval_res["tier"], "GOLD")
        self.assertTrue(eval_res["promotable"])

    def test_weak_label_rejected_tier(self):
        eval_res = WeakLabeler.evaluate_weak_label(
            filename_candidates=["POV"],
            visual_predictions={"POV": 0.31},
            verifier_status="REJECTED"
        )
        self.assertEqual(eval_res["tier"], "REJECTED")
        self.assertFalse(eval_res["promotable"])

    def test_taxonomy_manager(self):
        tm = TaxonomyManager()
        tm.register_unknown_term("customconcept")
        cands = tm.list_candidate_terms(min_occurrences=1)
        self.assertEqual(len(cands), 1)
        self.assertEqual(cands[0]["term"], "customconcept")


class TestModelLabAndBenchmark(unittest.TestCase):
    def test_benchmark_evaluator(self):
        preds = [{"label": "POV", "start": 0, "end": 10}]
        gt = [{"label": "POV", "start": 0, "end": 10}]
        res = BenchmarkEvaluator.evaluate_model(preds, gt)
        self.assertEqual(res["f1_score"], 1.0)
        self.assertEqual(res["temporal_iou"], 1.0)

    def test_model_promotion_comparison(self):
        prod = {"f1_score": 0.85, "temporal_iou": 0.80}
        cand = {"f1_score": 0.92, "temporal_iou": 0.88}
        comp = BenchmarkEvaluator.compare_models(prod, cand)
        self.assertTrue(comp["is_improved"])
        self.assertEqual(comp["recommendation"], "PROMOTE_TO_PRODUCTION")


class TestDomainIntelligenceEngine(unittest.TestCase):
    def test_source_policy_engine(self):
        self.assertEqual(SourcePolicyEngine.evaluate_url_policy("https://en.wikipedia.org/wiki/Tech"), "ALLOWED")
        self.assertEqual(SourcePolicyEngine.evaluate_url_policy("https://malicious.com/test"), "BLOCKED")

    def test_knowledge_base_ingestion_and_query(self):
        kb = LocalKnowledgeBase()
        doc = ContentExtractor.process_and_score({
            "source_url": "https://example.org/auto",
            "title": "Automotive Engineering",
            "extracted_text": "Electric vehicle powertrain overview.",
            "timestamp": "2026-08-12 12:00:00"
        }, topic="automotive")
        kb.ingest_document(doc)

        q_res = kb.query_knowledge_base("electric")
        self.assertEqual(len(q_res), 1)
        self.assertEqual(q_res[0]["title"], "Automotive Engineering")


if __name__ == "__main__":
    unittest.main()
