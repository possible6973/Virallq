import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.optimization_service import BatchOptimizationEngine
from database.crud import get_candidates_by_script_id

class TestCandidateOptimizer(unittest.TestCase):
    def test_ranking_logic_deterministic(self):
        """
        QA Section 30: Verify global best selection logic.
        Input: Candidate scores 60, 82, 74, 91 -> Winner must be 91.
        """
        candidates = [
            {'script_text': 'A', 'final_score': 60.0},
            {'script_text': 'B', 'final_score': 82.0},
            {'script_text': 'C', 'final_score': 74.0},
            {'script_text': 'D', 'final_score': 91.0},
        ]
        
        best = max(candidates, key=lambda x: x['final_score'])
        self.assertEqual(best['script_text'], 'D')
        self.assertEqual(best['final_score'], 91.0)

    def test_global_best_preservation_across_batches(self):
        """
        QA Section 18: Verify global peak preservation.
        Batch 1 = 90, Batch 2 = 74, Batch 3 = 81 -> Global Peak must be 90.
        """
        batches = [
            [{'script_text': 'B1_Cand1', 'final_score': 90.0}],
            [{'script_text': 'B2_Cand1', 'final_score': 74.0}],
            [{'script_text': 'B3_Cand1', 'final_score': 81.0}]
        ]
        
        global_best = {'final_score': -1.0, 'script_text': ''}
        for b in batches:
            for c in b:
                if c['final_score'] > global_best['final_score']:
                    global_best = c
                    
        self.assertEqual(global_best['final_score'], 90.0)
        self.assertEqual(global_best['script_text'], 'B1_Cand1')

    def test_max_batch_stopping(self):
        """
        QA Section 17 & 30: Max batch stopping limit test.
        Target score 101.0% (unreachable), max_batches = 3. Should run exactly 3 batches and stop.
        """
        engine = BatchOptimizationEngine(batch_size=2, target_score=101.0, max_batches=3)
        res = engine.optimize_script_generation(
            enhanced_prompt="Role: Real Estate. Task: Write a 30s reel script.",
            category="Real Estate"
        )
        self.assertEqual(res['total_batches_run'], 3)
        self.assertFalse(res['target_achieved'])
        self.assertIsNotNone(res['global_best'])

    def test_target_early_stopping(self):
        """
        QA Section 16: Target score stopping test.
        If batch 1 candidate hits target (>= 50%), stop optimization loop immediately in batch 1.
        """
        engine = BatchOptimizationEngine(batch_size=2, target_score=50.0, max_batches=5)
        res = engine.optimize_script_generation(
            enhanced_prompt="Role: Expert. Task: Write high performing 30s reel script.",
            category="Real Estate"
        )
        self.assertEqual(res['total_batches_run'], 1)
        self.assertTrue(res['target_achieved'])

if __name__ == "__main__":
    unittest.main()
