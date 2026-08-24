import sys
import unittest
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.ml_service import predict_ml_score, get_ml_metrics, load_ml_model
from utils.feature_extraction import extract_script_features, FEATURE_NAMES

class TestMLModel(unittest.TestCase):
    def test_model_loading(self):
        model, scaler, metrics = load_ml_model()
        self.assertIsNotNone(model)
        self.assertIsNotNone(scaler)
        self.assertIsNotNone(metrics)
        self.assertIn("accuracy", metrics)

    def test_feature_vector_dimension(self):
        sample_text = "₹50 lakh mein Surat mein premium 3 BHK home. Prime location, modern amenities. Aaj hi visit book karein."
        feats = extract_script_features(sample_text, target_duration=30)
        self.assertEqual(len(feats), len(FEATURE_NAMES))
        for name in FEATURE_NAMES:
            self.assertIn(name, feats)

    def test_prediction_output(self):
        sample_text = "₹50 lakh mein Surat mein premium 3 BHK home. Prime location, modern amenities aur easy connectivity ke saath. Aaj hi visit book karein."
        score, feats = predict_ml_score(sample_text, target_duration=30)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 100.0)

    def test_prediction_stability(self):
        sample_text = "Stop scrolling! Here are 3 secret AI tools in 2026!"
        score1, _ = predict_ml_score(sample_text, target_duration=30)
        score2, _ = predict_ml_score(sample_text, target_duration=30)
        self.assertEqual(score1, score2)

if __name__ == "__main__":
    unittest.main()
