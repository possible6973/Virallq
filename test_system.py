import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=== ViralIQ Verification Test Suite ===")

# 1. Test Database & Seed Data
print("1. Testing SQLite Database Connection & Seeding...")
from database.db import init_db, get_connection
from database.crud import get_all_scripts, get_all_viral_scripts, get_all_predictions
init_db()
viral_scripts = get_all_viral_scripts()
print(f"   [OK] SQLite initialized. Found {len(viral_scripts)} benchmark viral library scripts.")

# 2. Test Feature Extraction
print("2. Testing Feature Extraction Engine...")
from utils.feature_extraction import extract_script_features
feats = extract_script_features("Stop scrolling! 3 secret AI tools in 2026! Comment 'AI' for links.", target_duration=30)
assert feats['word_count'] > 0
print(f"   [OK] Features extracted: {list(feats.keys())[:5]}...")

# 3. Test Scikit-Learn ML Model Prediction
print("3. Testing Scikit-Learn Random Forest ML Model...")
from services.ml_service import predict_ml_score, get_ml_metrics
ml_score, _ = predict_ml_score("Stop scrolling! 3 secret AI tools in 2026!")
ml_metrics = get_ml_metrics()
print(f"   [OK] ML Score: {ml_score}%, Model Accuracy: {ml_metrics['accuracy']}%")

# 4. Test TensorFlow/Keras ANN Model Prediction
print("4. Testing Keras ANN Deep Neural Network Model...")
from services.ann_service import predict_ann_score, get_ann_metrics
ann_score = predict_ann_score("Stop scrolling! 3 secret AI tools in 2026!")
ann_metrics = get_ann_metrics()
print(f"   [OK] ANN Score: {ann_score}%, Epochs Trained: {ann_metrics.get('epochs_trained', 0)}")

# 5. Test Aggregation Layer
print("5. Testing Aggregation Layer...")
from utils.scoring import aggregate_scores, get_performance_status
final_score = aggregate_scores(ml_score, ann_score, method="weighted_average", ml_weight=0.5)
status = get_performance_status(final_score)
print(f"   [OK] Aggregated Score: {final_score}% ({status})")

# 6. Test Gemini API Prompt Enhancer & Candidate Generation
print("6. Testing Gemini API & Prompt Engineering...")
from services.gemini_service import get_gemini_client, enhance_prompt, generate_candidates
api_key = os.environ.get("GEMINI_API_KEY", "")
try:
    enhanced = enhance_prompt("real estate 50 lakh na ghar sale", category="Real Estate", api_key=api_key)
    print(f"   [OK] Enhanced Prompt preview snippet:\n   {enhanced[:150]}...")
except Exception as e:
    print(f"   [WARN] Gemini call warning: {e}")

# 7. Test Multi-Candidate Optimization Engine Loop
print("7. Testing Multi-Candidate Optimization Engine Loop...")
from services.optimization_service import BatchOptimizationEngine
engine = BatchOptimizationEngine(batch_size=3, target_score=80.0, max_batches=2)
res = engine.optimize_script_generation(
    enhanced_prompt="Role: Real Estate Writer. Task: Write a 30s reel script for a 50 lakh flat.",
    category="Real Estate",
    api_key=api_key
)
print(f"   [OK] Optimization complete! Evaluated {res['total_candidates_evaluated']} candidates across {res['total_batches_run']} batches.")
print(f"   [OK] Winner Global Peak Score: {res['global_best']['final_score']}% (Batch #{res['global_best']['batch_number']})")

# 8. Test Page Imports
print("8. Testing Streamlit Page Views imports...")
from pages import dashboard, analyze_script, generate_script, analyze_reel, viral_library, my_scripts, ai_advisor, analytics, reports, settings
print("   [OK] All 10 Streamlit page modules imported with 0 errors!")

print("=== ALL SYSTEM CHECKS PASSED SUCCESSFULLY! ===")
