from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    created_at: Optional[str] = None

@dataclass
class Script:
    id: Optional[int]
    title: str
    script_text: str
    category: str = "General"
    audience: str = "General"
    platform: str = "Instagram"
    duration: int = 30
    user_id: int = 1
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class Prediction:
    id: Optional[int]
    script_id: int
    ml_score: float
    ann_score: float
    final_score: float
    status: str = "Analyzed"
    created_at: Optional[str] = None

@dataclass
class ViralScript:
    id: Optional[int]
    category: str
    topic: str
    hook: str
    script_text: str
    audience: str = "General"
    duration: int = 30
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    engagement_rate: float = 0.0
    performance_label: str = "Viral"

@dataclass
class GeneratedCandidate:
    id: Optional[int]
    batch_number: int
    candidate_number: int
    script_text: str
    ml_score: float
    ann_score: float
    final_score: float
    original_script_id: Optional[int] = None
    is_best: bool = False
    created_at: Optional[str] = None

@dataclass
class Report:
    id: Optional[int]
    script_id: int
    analysis: str
    recommendations: str
    created_at: Optional[str] = None
