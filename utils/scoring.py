import numpy as np
import math

def safe_float(val, default=0.0) -> float:
    if val is None:
        return default
    try:
        f = float(val)
        if math.isnan(f) or math.isinf(f):
            return default
        return f
    except (ValueError, TypeError):
        return default

def aggregate_scores(ml_score: float, ann_score: float, method: str = "weighted_average", ml_weight: float = 0.5) -> float:
    """
    Combines raw ML score and raw ANN score into a final Performance Score [0 - 100].
    
    Methods:
    - weighted_average: ml_weight * ml_score + (1 - ml_weight) * ann_score
    - harmonic_mean: 2 * (ml * ann) / (ml + ann) [penalizes severe model disagreement]
    - min: Conservative evaluation
    - max: Optimistic evaluation
    """
    ml = max(0.0, min(100.0, safe_float(ml_score)))
    ann = max(0.0, min(100.0, safe_float(ann_score)))
    w = max(0.0, min(1.0, safe_float(ml_weight, 0.5)))
    
    if method == "weighted_average":
        final = (w * ml) + ((1.0 - w) * ann)
    elif method == "harmonic_mean":
        if ml + ann == 0:
            final = 0.0
        else:
            final = (2.0 * ml * ann) / (ml + ann)
    elif method == "min":
        final = min(ml, ann)
    elif method == "max":
        final = max(ml, ann)
    else:
        final = (ml + ann) / 2.0
        
    return round(float(final), 2)

def get_performance_status(score: float) -> str:
    """
    Evaluates score against optimization target threshold (default 80%).
    Note: 80% is an optimization target, NOT a scientific guarantee of virality.
    """
    s = safe_float(score)
    if s >= 80.0:
        return "High Potential"
    elif s >= 65.0:
        return "Moderate Potential"
    else:
        return "Needs Optimization"
