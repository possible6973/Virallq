import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.scoring import aggregate_scores, get_performance_status

class TestScoring(unittest.TestCase):
    def test_weighted_average(self):
        score = aggregate_scores(ml_score=80.0, ann_score=60.0, method="weighted_average", ml_weight=0.5)
        self.assertEqual(score, 70.0)

        score_custom_weight = aggregate_scores(ml_score=80.0, ann_score=60.0, method="weighted_average", ml_weight=0.75)
        self.assertEqual(score_custom_weight, 75.0)

    def test_harmonic_mean(self):
        score = aggregate_scores(ml_score=80.0, ann_score=60.0, method="harmonic_mean")
        expected = round(2.0 * 80.0 * 60.0 / (80.0 + 60.0), 2)
        self.assertEqual(score, expected)

    def test_min_max(self):
        self.assertEqual(aggregate_scores(50.0, 80.0, method="min"), 50.0)
        self.assertEqual(aggregate_scores(50.0, 80.0, method="max"), 80.0)

    def test_edge_cases(self):
        # 0 and 0
        self.assertEqual(aggregate_scores(0.0, 0.0, method="harmonic_mean"), 0.0)
        self.assertEqual(aggregate_scores(0.0, 0.0, method="weighted_average"), 0.0)

        # 100 and 100
        self.assertEqual(aggregate_scores(100.0, 100.0), 100.0)

        # None / NaN inputs safely fall back to 0.0
        self.assertEqual(aggregate_scores(None, 80.0), 40.0)
        self.assertEqual(aggregate_scores(float('nan'), 80.0), 40.0)

    def test_performance_status_thresholds(self):
        self.assertEqual(get_performance_status(80.0), "High Potential")
        self.assertEqual(get_performance_status(85.0), "High Potential")
        self.assertEqual(get_performance_status(75.0), "Moderate Potential")
        self.assertEqual(get_performance_status(64.9), "Needs Optimization")

if __name__ == "__main__":
    unittest.main()
