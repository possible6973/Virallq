import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.feature_extraction import extract_script_features

class TestInputValidation(unittest.TestCase):
    def test_empty_script_feature_extraction(self):
        feats = extract_script_features("")
        self.assertEqual(feats['word_count'], 0.0)
        self.assertEqual(feats['estimated_duration'], 0.0)

    def test_extremely_long_script_feature_extraction(self):
        long_script = "Stop scrolling! " + ("This is a luxury property. " * 500) + "Comment HOME below!"
        feats = extract_script_features(long_script, target_duration=30)
        self.assertGreater(feats['word_count'], 1000)
        self.assertGreater(feats['estimated_duration'], 300)

    def test_special_character_script(self):
        script_with_symbols = "Stop scrolling!! ₹50 Lakhs @Surat City #Home 100% 0% brokerage? DM now!!!"
        feats = extract_script_features(script_with_symbols, target_duration=30)
        self.assertGreater(feats['number_count'], 0.0)
        self.assertGreater(feats['question_count'], 0.0)

if __name__ == "__main__":
    unittest.main()
