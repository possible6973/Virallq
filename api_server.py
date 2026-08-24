import os
import sys
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Ensure root dir in path
sys.path.insert(0, str(Path(__file__).parent))

# Import database & services
from database.db import init_db
from data.seed_data import seed_database
from database.crud import (
    get_all_scripts, get_script_by_id, create_script, update_script, delete_script,
    get_all_predictions, get_predictions_for_script, save_prediction,
    get_all_viral_scripts, search_viral_scripts, add_viral_script, delete_viral_script,
    get_all_reports, save_report
)
from database.models import Script, Prediction, ViralScript, Report
from utils.feature_extraction import extract_script_features
from services.ml_service import predict_ml_score, get_ml_metrics
from services.ann_service import predict_ann_score, get_ann_metrics
from utils.scoring import aggregate_scores, get_performance_status
from services.gemini_service import get_gemini_client, enhance_prompt, analyze_script, improve_script, generate_report
from services.prompt_service import enhance_user_prompt
from services.optimization_service import BatchOptimizationEngine
from services.cnn_service import analyze_thumbnail_frame

# Initialize DB safely on cold start
try:
    init_db()
    seed_database()
except Exception as e:
    print(f"DB Init Warning: {e}")

app = FastAPI(title="ViralIQ API & SaaS Application", version="2.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class AnalyzeScriptRequest(BaseModel):
    title: str = "My Reel Script"
    script_text: str
    category: str = "General"
    audience: str = "General"
    platform: str = "Instagram"
    duration: int = 30
    score_method: str = "weighted_average"
    ml_weight: float = 0.5
    api_key: Optional[str] = None

class EnhancePromptRequest(BaseModel):
    informal_prompt: str
    category: str = "General"
    audience: str = "General"
    platform: str = "Instagram"
    duration: int = 30
    api_key: Optional[str] = None

class GenerateScriptRequest(BaseModel):
    enhanced_prompt: str
    category: str = "General"
    batch_size: int = 5
    target_score: float = 80.0
    max_batches: int = 5
    score_method: str = "weighted_average"
    ml_weight: float = 0.5
    api_key: Optional[str] = None

class ScriptCreateRequest(BaseModel):
    title: str
    script_text: str
    category: str = "General"
    audience: str = "General"
    platform: str = "Instagram"
    duration: int = 30

class ScriptUpdateRequest(BaseModel):
    title: str
    script_text: str
    category: str
    audience: str
    platform: str
    duration: int

class ChatRequest(BaseModel):
    message: str
    api_key: Optional[str] = None

# ================= REST ENDPOINTS =================

@app.get("/api/dashboard")
def get_dashboard_summary():
    scripts = get_all_scripts()
    predictions = get_all_predictions()
    viral_lib = get_all_viral_scripts()
    
    total_scripts = len(scripts)
    total_analyzed = len(predictions)
    
    if predictions:
        avg_score = round(sum(p['final_score'] for p in predictions) / len(predictions), 1)
        best_score = round(max(p['final_score'] for p in predictions), 1)
    else:
        avg_score = 0.0
        best_score = 0.0
        
    optimized_count = sum(1 for p in predictions if p['final_score'] >= 80.0)
    
    return {
        "total_scripts": total_scripts,
        "reels_analyzed": total_analyzed,
        "avg_score": avg_score,
        "best_score": best_score,
        "optimized_count": optimized_count,
        "recent_predictions": predictions[:10],
        "recent_scripts": scripts[:10],
        "viral_count": len(viral_lib)
    }

@app.post("/api/analyze")
def analyze_script_endpoint(req: AnalyzeScriptRequest):
    if not req.script_text.strip():
        raise HTTPException(status_code=400, detail="Script text cannot be empty.")
        
    features = extract_script_features(req.script_text, target_duration=req.duration)
    ml_score, _ = predict_ml_score(req.script_text, target_duration=req.duration)
    ann_score = predict_ann_score(req.script_text, target_duration=req.duration)
    final_score = aggregate_scores(ml_score, ann_score, method=req.score_method, ml_weight=req.ml_weight)
    status = get_performance_status(final_score)
    
    analysis_data = analyze_script(req.script_text, ml_score, ann_score, final_score, api_key=req.api_key)
    
    script_id = create_script(Script(
        id=None,
        title=req.title,
        script_text=req.script_text,
        category=req.category,
        audience=req.audience,
        platform=req.platform,
        duration=req.duration
    ))
    
    save_prediction(Prediction(
        id=None,
        script_id=script_id,
        ml_score=ml_score,
        ann_score=ann_score,
        final_score=final_score,
        status=status
    ))
    
    save_report(Report(
        id=None,
        script_id=script_id,
        analysis=json.dumps(analysis_data),
        recommendations=json.dumps(analysis_data.get("recommendations", []))
    ))
    
    return {
        "script_id": script_id,
        "title": req.title,
        "script_text": req.script_text,
        "ml_score": ml_score,
        "ann_score": ann_score,
        "final_score": final_score,
        "status": status,
        "features": features,
        "analysis_data": analysis_data
    }

@app.post("/api/enhance-prompt")
def enhance_prompt_endpoint(req: EnhancePromptRequest):
    enhanced = enhance_user_prompt(
        informal_text=req.informal_prompt,
        category=req.category,
        audience=req.audience,
        platform=req.platform,
        duration=req.duration,
        api_key=req.api_key
    )
    return {"enhanced_prompt": enhanced}

@app.post("/api/generate")
def generate_candidates_endpoint(req: GenerateScriptRequest):
    engine = BatchOptimizationEngine(
        batch_size=req.batch_size,
        target_score=req.target_score,
        max_batches=req.max_batches,
        score_method=req.score_method,
        ml_weight=req.ml_weight
    )
    
    opt_result = engine.optimize_script_generation(
        enhanced_prompt=req.enhanced_prompt,
        category=req.category,
        api_key=req.api_key
    )
    
    best = opt_result['global_best']
    script_id = create_script(Script(
        id=None,
        title=f"{req.category} Optimized Reel",
        script_text=best['script_text'],
        category=req.category,
        audience="General",
        platform="Instagram",
        duration=30
    ))
    
    save_prediction(Prediction(
        id=None,
        script_id=script_id,
        ml_score=best['ml_score'],
        ann_score=best['ann_score'],
        final_score=best['final_score'],
        status=best['status']
    ))
    
    return {
        "script_id": script_id,
        "optimization_result": opt_result
    }

@app.get("/api/viral-library")
def get_viral_library_endpoint(category: Optional[str] = None, search: Optional[str] = None):
    return search_viral_scripts(category=category, topic=search, limit=50)

@app.post("/api/viral-library")
def add_viral_library_endpoint(item: Dict[str, Any]):
    vs = ViralScript(
        id=None,
        category=item.get("category", "General"),
        topic=item.get("topic", "Untitled"),
        audience=item.get("audience", "General"),
        hook=item.get("hook", item.get("topic", "")),
        script_text=item.get("script_text", ""),
        duration=item.get("duration", 30),
        views=item.get("views", 100000),
        likes=item.get("likes", 8000),
        comments=item.get("comments", 500),
        shares=item.get("shares", 1200),
        engagement_rate=item.get("engagement_rate", 8.5),
        performance_label="High Potential"
    )
    v_id = add_viral_script(vs)
    return {"id": v_id, "status": "success"}

@app.get("/api/scripts")
def get_user_scripts_endpoint():
    return get_all_scripts()

@app.post("/api/scripts")
def create_script_endpoint(req: ScriptCreateRequest):
    s_id = create_script(Script(
        id=None,
        title=req.title,
        script_text=req.script_text,
        category=req.category,
        audience=req.audience,
        platform=req.platform,
        duration=req.duration
    ))
    return {"id": s_id, "status": "created"}

@app.put("/api/scripts/{script_id}")
def update_script_endpoint(script_id: int, req: ScriptUpdateRequest):
    success = update_script(
        script_id=script_id,
        title=req.title,
        script_text=req.script_text,
        category=req.category,
        audience=req.audience,
        platform=req.platform,
        duration=req.duration
    )
    if not success:
        raise HTTPException(status_code=404, detail="Script not found.")
    return {"status": "updated"}

@app.delete("/api/scripts/{script_id}")
def delete_script_endpoint(script_id: int):
    success = delete_script(script_id)
    if not success:
        raise HTTPException(status_code=404, detail="Script not found.")
    return {"status": "deleted"}

@app.post("/api/ai-advisor")
def ai_advisor_endpoint(req: ChatRequest):
    recent_preds = get_all_predictions()[:3]
    ctx_str = ""
    if recent_preds:
        ctx_str = "User's Recent Model Predictions:\n"
        for p in recent_preds:
            ctx_str += f"- Script '{p.get('script_title', 'Untitled')}': ML={p['ml_score']}%, ANN={p['ann_score']}%, Final={p['final_score']}%\n"
            
    try:
        model = get_gemini_client(req.api_key)
        prompt = (
            "You are ViralIQ's AI Content Strategist and Script Advisor.\n"
            "Provide clear, actionable, concise advice for short-form video creators.\n"
            f"{ctx_str}\n\n"
            f"User Question: {req.message}"
        )
        res = model.generate_content(prompt)
        reply = res.text.strip()
    except Exception as e:
        reply = (
            "Based on ViralIQ's quantitative model evaluation:\n"
            "- High curiosity hooks (containing metrics, 'stop' triggers, or questions) boost retention.\n"
            "- Direct engagement CTAs (asking users to comment a specific keyword for DM automation) increase algorithmic velocity."
        )
        
    return {"reply": reply}

@app.get("/api/analytics")
def get_analytics_endpoint():
    ml_metrics = get_ml_metrics()
    ann_metrics = get_ann_metrics()
    predictions = get_all_predictions()
    return {
        "ml_metrics": ml_metrics,
        "ann_metrics": ann_metrics,
        "predictions": predictions
    }

@app.post("/api/reports/generate")
def generate_report_endpoint(data: Dict[str, Any] = Body(...)):
    script_id = data.get("script_id")
    script = get_script_by_id(script_id)
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
        
    preds = get_predictions_for_script(script_id)
    p_data = preds[0] if preds else {"ml_score": 75, "ann_score": 80, "final_score": 77.5}
    
    report_md = generate_report(
        script_title=script['title'],
        script_text=script['script_text'],
        ml_score=p_data['ml_score'],
        ann_score=p_data['ann_score'],
        final_score=p_data['final_score'],
        analysis={"hook_critique": "Good hook", "weaknesses": ["Tighten body pacing"]},
        api_key=data.get("api_key")
    )
    return {"report_markdown": report_md}

@app.post("/api/analyze-reel")
def analyze_reel_endpoint(data: Dict[str, Any] = Body(...)):
    transcript = data.get("transcript", "").strip()
    if not transcript:
        transcript = "Stop scrolling if you want to double your reel views in 30 seconds! Comment 'INFO' for details."
        
    ml_score, features = predict_ml_score(transcript, target_duration=30)
    ann_score = predict_ann_score(transcript, target_duration=30)
    script_score = aggregate_scores(ml_score, ann_score)
    script_status = get_performance_status(script_score)
    
    # Save script & prediction into SQLite database
    script_id = create_script(Script(
        id=None,
        title="Reel Spoken Content Analysis",
        script_text=transcript,
        category="Reel Video",
        audience="General",
        platform="Instagram Reels",
        duration=30
    ))
    
    save_prediction(Prediction(
        id=None,
        script_id=script_id,
        ml_score=ml_score,
        ann_score=ann_score,
        final_score=script_score,
        status=script_status
    ))
    
    cnn_res = analyze_thumbnail_frame("uploaded_reel_frame")
    
    return {
        "script_id": script_id,
        "transcript": transcript,
        "ml_score": ml_score,
        "ann_score": ann_score,
        "script_score": script_score,
        "script_status": script_status,
        "features": features,
        "cnn_res": cnn_res
    }

# Static file serving for React production build
dist_dir = Path(__file__).parent / "frontend" / "dist"
if dist_dir.exists() and (dist_dir / "assets").exists():
    app.mount("/assets", StaticFiles(directory=dist_dir / "assets"), name="assets")

@app.get("/{full_path:path}")
def serve_react_app(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
        
    file_path = dist_dir / full_path
    if full_path and file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
        
    index_file = dist_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "ViralIQ Server Active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
