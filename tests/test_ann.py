import sys
import unittest
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.ann_service import predict_ann_score, get_ann_metrics, load_ann_model

class TestANNModel(unittest.TestCase):
    def test_ann_model_loading(self):
        model, scaler, metrics = load_ann_model()
        self.assertIsNotNone(model)
        self.assertIsNotNone(scaler)
        self.assertIsNotNone(metrics)
        self.assertIn("accuracy", metrics)
        self.assertIn("epochs_trained", metrics)

    def test_ann_prediction_inference(self):
        sample_text = "₹50 lakh mein Surat mein premium 3 BHK home. Prime location, modern amenities. Aaj hi visit book karein."
        ann_score = predict_ann_score(sample_text, target_duration=30)
        self.assertIsInstance(ann_score, float)
        self.assertFalse(math.isnan(ann_score))
        self.assertGreaterEqual(ann_score, 0.0)
        self.assertLessEqual(ann_score, 100.0)

    def test_ann_early_stopping_recorded(self):
        metrics = get_ann_metrics()
        self.assertIn("epochs_trained", metrics)
        # Early stopping patience is 10, so max 100 epochs
        self.assertLessEqual(metrics["epochs_trained"], 100)

if __name__ == "__main__":
    unittest.main()
