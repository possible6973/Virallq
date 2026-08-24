import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.prompt_service import enhance_user_prompt

class TestPromptEnhancement(unittest.TestCase):
    def test_informal_prompt_enhancement(self):
        informal = "real estate 50 lakh na ghar sale"
        enhanced = enhance_user_prompt(
            informal_text=informal,
            category="Real Estate",
            audience="First-time Buyers",
            platform="Instagram",
            duration=30
        )
        self.assertIsNotNone(enhanced)
        self.assertGreater(len(enhanced), 50)
        # Check structured components present
        self.assertTrue(
            "Role" in enhanced or "Task" in enhanced or "Audience" in enhanced or "Platform" in enhanced
        )

    def test_empty_informal_prompt_validation(self):
        empty_res = enhance_user_prompt("")
        self.assertEqual(empty_res, "Please enter a valid script topic or requirement.")

        spaces_res = enhance_user_prompt("   ")
        self.assertEqual(spaces_res, "Please enter a valid script topic or requirement.")

if __name__ == "__main__":
    unittest.main()
