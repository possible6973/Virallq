import sys
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.gemini_service import generate_candidates
from services.ml_service import predict_ml_score
from services.ann_service import predict_ann_score
from utils.scoring import aggregate_scores, get_performance_status
from database.crud import save_candidate, search_viral_scripts
from database.models import GeneratedCandidate

class BatchOptimizationEngine:
    def __init__(
        self,
        batch_size: int = 5,
        target_score: float = 80.0,
        max_batches: int = 5,
        score_method: str = "weighted_average",
        ml_weight: float = 0.5
    ):
        self.batch_size = batch_size
        self.target_score = target_score
        self.max_batches = max_batches
        self.score_method = score_method
        self.ml_weight = ml_weight

    def optimize_script_generation(
        self,
        enhanced_prompt: str,
        category: str = "General",
        original_script_id: Optional[int] = None,
        api_key: str = None,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        """
        Iterative Multi-Candidate Script Optimization Loop:
        1. Retrieves relevant viral library examples as context.
        2. Generates a batch of N candidates via Gemini API.
        3. Evaluates every candidate using ML + ANN models.
        4. Tracks and preserves the global highest-scoring candidate.
        5. If target score (>=80%) reached, stops early.
        6. Otherwise repeats up to max_batches and returns global best.
        """
        # Retrieve contextual viral script patterns
        examples = search_viral_scripts(category=category, limit=3)
        
        global_best = {
            'script_text': "",
            'final_score': -1.0,
            'ml_score': 0.0,
            'ann_score': 0.0,
            'batch_number': 0,
            'candidate_number': 0,
            'status': "Needs Optimization"
        }
        
        batch_history = []
        all_candidates_evaluated = []
        target_achieved = False
        
        for batch_num in range(1, self.max_batches + 1):
            # Generate N candidate scripts for current batch
            # Adjust prompt for subsequent batches if target not reached
            current_prompt = enhanced_prompt
            if batch_num > 1:
                current_prompt += (
                    f"\n\n[Optimization Feedback for Batch {batch_num}]: "
                    f"Previous best score was {global_best['final_score']}%. "
                    f"Generate punchier hooks, higher curiosity triggers, and stronger direct CTAs to push the performance score above {self.target_score}%!"
                )
                
            raw_candidates = generate_candidates(
                enhanced_prompt=current_prompt,
                num_candidates=self.batch_size,
                examples=examples,
                api_key=api_key
            )
            
            batch_candidates = []
            batch_best_score = -1.0
            batch_best_candidate = None
            
            for c_idx, script_text in enumerate(raw_candidates, 1):
                # 1. Feature extraction & ML score
                ml_score, features = predict_ml_score(script_text)
                
                # 2. ANN score
                ann_score = predict_ann_score(script_text)
                
                # 3. Score aggregation
                final_score = aggregate_scores(
                    ml_score=ml_score,
                    ann_score=ann_score,
                    method=self.score_method,
                    ml_weight=self.ml_weight
                )
                
                status = get_performance_status(final_score)
                
                cand_info = {
                    'batch_number': batch_num,
                    'candidate_number': c_idx,
                    'script_text': script_text,
                    'ml_score': ml_score,
                    'ann_score': ann_score,
                    'final_score': final_score,
                    'status': status,
                    'features': features,
                    'is_global_best': False
                }
                
                batch_candidates.append(cand_info)
                all_candidates_evaluated.append(cand_info)
                
                # Track batch best
                if final_score > batch_best_score:
                    batch_best_score = final_score
                    batch_best_candidate = cand_info
                    
                # Track global best across all batches
                if final_score > global_best['final_score']:
                    global_best = {
                        'script_text': script_text,
                        'final_score': final_score,
                        'ml_score': ml_score,
                        'ann_score': ann_score,
                        'batch_number': batch_num,
                        'candidate_number': c_idx,
                        'status': status,
                        'features': features
                    }
                    
                # Save candidate to SQLite database
                db_cand = GeneratedCandidate(
                    id=None,
                    original_script_id=original_script_id,
                    batch_number=batch_num,
                    candidate_number=c_idx,
                    script_text=script_text,
                    ml_score=ml_score,
                    ann_score=ann_score,
                    final_score=final_score,
                    is_best=(final_score == global_best['final_score'])
                )
                save_candidate(db_cand)

            # Record batch summary
            batch_summary = {
                'batch_number': batch_num,
                'num_candidates': len(batch_candidates),
                'best_score': batch_best_score,
                'avg_score': round(sum(c['final_score'] for c in batch_candidates) / max(1, len(batch_candidates)), 2),
                'candidates': batch_candidates
            }
            batch_history.append(batch_summary)
            
            if progress_callback:
                progress_callback({
                    'current_batch': batch_num,
                    'max_batches': self.max_batches,
                    'batch_best': batch_best_score,
                    'global_best': global_best['final_score'],
                    'batch_summary': batch_summary
                })
                
            # Check target score stopping condition (>= 80%)
            if global_best['final_score'] >= self.target_score:
                target_achieved = True
                break
                
        return {
            'global_best': global_best,
            'target_achieved': target_achieved,
            'total_batches_run': len(batch_history),
            'total_candidates_evaluated': len(all_candidates_evaluated),
            'batch_history': batch_history,
            'all_candidates': all_candidates_evaluated
        }
