import sys
import os
from pathlib import Path

# Force UTF-8 encoding for Windows stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))

from database.db import init_db
from database.crud import get_script_by_id, update_script, delete_script
from services.agent_service import ViralIQAgent

print("=== Starting Step-by-Step QA End-to-End Scenario Test ===")

# User Requirement
user_input = "real estate 50 lakh na ghar sale"
print(f"Input User Requirement: '{user_input}'")

# Step 1-8: Initialize AI Agent & Run full pipeline
print("\nRunning Agent Workflow (Prompt Enhancer -> Gemini Candidates -> ML -> ANN -> Ranking -> SQLite)...")
agent = ViralIQAgent(batch_size=3, target_score=80.0, max_batches=2)

result = agent.run_full_pipeline(
    informal_prompt=user_input,
    title="E2E Test Real Estate Reel",
    category="Real Estate",
    audience="First-time Buyers",
    platform="Instagram",
    duration=30
)

script_id = result['script_id']
best = result['global_best']

print(f"-> Script Created in SQLite DB with ID: #{script_id}")
print(f"-> Enhanced Prompt Generated: {result['enhanced_prompt'][:100]}...")
print(f"-> Total Candidates Evaluated: {result['optimization_result']['total_candidates_evaluated']}")
print(f"-> Total Batches Executed: {result['optimization_result']['total_batches_run']}")
print(f"-> Winning Global Peak Candidate Score: {best['final_score']}% (ML: {best['ml_score']}%, ANN: {best['ann_score']}%)")

# Safe print script text
try:
    print(f"-> Winning Script Text:\n{best['script_text']}\n")
except Exception:
    print(f"-> Winning Script Text:\n{best['script_text'].encode('utf-8', errors='ignore').decode()}\n")

# Step 9: Verify Record in SQLite
fetched = get_script_by_id(script_id)
assert fetched is not None, "Failed to fetch script from DB"
assert fetched['title'] == "E2E Test Real Estate Reel"
print("-> Step 9 PASS: Script record verified in SQLite database!")

# Step 10: Edit Record (Update CRUD)
updated = update_script(
    script_id=script_id,
    title="E2E Test Real Estate Reel (EDITS SAVED)",
    script_text=best['script_text'] + "\nUpdated bonus line.",
    category="Real Estate",
    audience="First-time Buyers",
    platform="Instagram",
    duration=30
)
assert updated is True, "Failed to update script record"
refetched = get_script_by_id(script_id)
assert "EDITS SAVED" in refetched['title']
print("-> Step 10 PASS: Script update verified in SQLite database!")

# Step 11: Delete Record (Delete CRUD)
deleted = delete_script(script_id)
assert deleted is True, "Failed to delete script record"
post_delete = get_script_by_id(script_id)
assert post_delete is None, "Script record still exists after deletion"
print("-> Step 11 PASS: Script deletion verified in SQLite database!")

print("\n=== END-TO-END QA SCENARIO PASSED WITH 100% SUCCESS ===")
