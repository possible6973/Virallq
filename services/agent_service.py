import sys
from pathlib import Path
from typing import Dict, Any, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.prompt_service import enhance_user_prompt
from services.optimization_service import BatchOptimizationEngine
from services.gemini_service import analyze_script, generate_report
from database.crud import create_script, save_prediction, save_report
from database.models import Script, Prediction, Report

class ViralIQAgent:
    """
    AI-504 AI Agent / Workflow Coordinator:
    Orchestrates RAG retrieval, Prompt Engineering, Gemini multi-candidate generation,
    Scikit-Learn ML evaluation, Keras ANN evaluation, rank selection, and automated reporting.
    """
    def __init__(self, batch_size: int = 5, target_score: float = 80.0, max_batches: int = 5):
        self.engine = BatchOptimizationEngine(
            batch_size=batch_size,
            target_score=target_score,
            max_batches=max_batches
        )

    def run_full_pipeline(
        self,
        informal_prompt: str,
        title: str = "Generated Reel",
        category: str = "General",
        audience: str = "General",
        platform: str = "Instagram",
        duration: int = 30,
        api_key: str = None,
        progress_callback: Optional[Any] = None
    ) -> Dict[str, Any]:
        
        # Step 1: Prompt Enhancement
        enhanced_prompt = enhance_user_prompt(
            informal_text=informal_prompt,
            category=category,
            audience=audience,
            platform=platform,
            duration=duration,
            api_key=api_key
        )
        
        # Step 2: Multi-Candidate Batch Optimization Loop
        optimization_result = self.engine.optimize_script_generation(
            enhanced_prompt=enhanced_prompt,
            category=category,
            api_key=api_key,
            progress_callback=progress_callback
        )
        
        best = optimization_result['global_best']
        
        # Step 3: Store Global Best Script in SQLite database
        new_script = Script(
            id=None,
            title=title if title else f"{category} Reel ({duration}s)",
            script_text=best['script_text'],
            category=category,
            audience=audience,
            platform=platform,
            duration=duration
        )
        script_id = create_script(new_script)
        
        # Step 4: Save Prediction Record
        pred = Prediction(
            id=None,
            script_id=script_id,
            ml_score=best['ml_score'],
            ann_score=best['ann_score'],
            final_score=best['final_score'],
            status=best['status']
        )
        save_prediction(pred)
        
        # Step 5: LLM Detailed Qualitative Analysis & Critique
        analysis_data = analyze_script(
            script_text=best['script_text'],
            ml_score=best['ml_score'],
            ann_score=best['ann_score'],
            final_score=best['final_score'],
            api_key=api_key
        )
        
        # Step 6: Generate Executive Report
        report_md = generate_report(
            script_title=new_script.title,
            script_text=best['script_text'],
            ml_score=best['ml_score'],
            ann_score=best['ann_score'],
            final_score=best['final_score'],
            analysis=analysis_data,
            api_key=api_key
        )
        
        report_obj = Report(
            id=None,
            script_id=script_id,
            analysis=json_dumps_safe(analysis_data),
            recommendations=json_dumps_safe(analysis_data.get('recommendations', []))
        )
        save_report(report_obj)
        
        return {
            'script_id': script_id,
            'title': new_script.title,
            'enhanced_prompt': enhanced_prompt,
            'global_best': best,
            'optimization_result': optimization_result,
            'analysis': analysis_data,
            'report_markdown': report_md
        }

def json_dumps_safe(obj):
    import json
    try:
        return json.dumps(obj)
    except Exception:
        return str(obj)
