import sys
import unittest
from pathlib import Path

# Add root directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db import init_db
from database.crud import (
    create_script, get_script_by_id, update_script, delete_script, get_all_scripts,
    save_prediction, get_predictions_for_script,
    add_viral_script, search_viral_scripts, delete_viral_script
)
from database.models import Script, Prediction, ViralScript

class TestDatabaseCRUD(unittest.TestCase):
    def setUp(self):
        init_db()

    def test_script_crud_flow(self):
        # 1. CREATE
        new_script = Script(
            id=None,
            title="QA Test Script",
            script_text="₹50 lakh mein 3 BHK ghar...",
            category="Real Estate",
            audience="First-time buyers",
            platform="Instagram",
            duration=30
        )
        script_id = create_script(new_script)
        self.assertIsNotNone(script_id)

        # 2. READ
        fetched = get_script_by_id(script_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["title"], "QA Test Script")
        self.assertEqual(fetched["script_text"], "₹50 lakh mein 3 BHK ghar...")

        # 3. UPDATE
        updated_success = update_script(
            script_id=script_id,
            title="Updated QA Test Script",
            script_text="Updated text ₹50 lakh...",
            category="Real Estate",
            audience="First-time buyers",
            platform="Instagram",
            duration=35
        )
        self.assertTrue(updated_success)

        refetched = get_script_by_id(script_id)
        self.assertEqual(refetched["title"], "Updated QA Test Script")
        self.assertEqual(refetched["duration"], 35)

        # 4. DELETE
        deleted_success = delete_script(script_id)
        self.assertTrue(deleted_success)

        after_delete = get_script_by_id(script_id)
        self.assertIsNone(after_delete)

    def test_prediction_crud(self):
        script_id = create_script(Script(
            id=None,
            title="Prediction Test Script",
            script_text="Testing prediction storage",
            category="Tech",
            audience="General",
            platform="Instagram",
            duration=30
        ))

        pred = Prediction(
            id=None,
            script_id=script_id,
            ml_score=85.5,
            ann_score=88.0,
            final_score=86.75,
            status="High Potential"
        )
        pred_id = save_prediction(pred)
        self.assertIsNotNone(pred_id)

        preds = get_predictions_for_script(script_id)
        self.assertGreaterEqual(len(preds), 1)
        self.assertEqual(preds[0]["final_score"], 86.75)

        # Clean up
        delete_script(script_id)

    def test_viral_script_search_and_delete(self):
        vs = ViralScript(
            id=None,
            category="QA Category",
            topic="QA Viral Topic",
            audience="QA Audience",
            hook="QA Hook Stop Scrolling",
            script_text="QA Full Script Body",
            duration=30,
            engagement_rate=9.9
        )
        v_id = add_viral_script(vs)
        self.assertIsNotNone(v_id)

        results = search_viral_scripts(category="QA Category", topic="QA Viral Topic")
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["topic"], "QA Viral Topic")

        delete_success = delete_viral_script(v_id)
        self.assertTrue(delete_success)

if __name__ == "__main__":
    unittest.main()
