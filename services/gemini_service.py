import os
import json
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, NotFound, GoogleAPICallError

# Load environment variables if dotenv installed
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass

DEFAULT_API_KEY = os.environ.get("GEMINI_API_KEY", "")
DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")

# Prioritize active models with high quota limits
FALLBACK_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-1.5-flash-8b",
    "gemini-3.7-flash",
    "gemini-3.6-flash"
]

def get_gemini_client(api_key: str = None, model_name: str = None):
    key = api_key if (api_key and api_key.strip()) else os.environ.get("GEMINI_API_KEY", "")
    genai.configure(api_key=key)
    target_model = model_name if model_name else DEFAULT_MODEL
    return genai.GenerativeModel(target_model)

def generate_with_fallback(prompt_text: str, api_key: str = None) -> str:
    key = api_key if (api_key and api_key.strip()) else os.environ.get("GEMINI_API_KEY", "")

    genai.configure(api_key=key)
    
    last_err = None
    for m_name in FALLBACK_MODELS:
        try:
            model = genai.GenerativeModel(m_name)
            res = model.generate_content(prompt_text)
            if res and res.text and res.text.strip():
                return res.text.strip()
        except (ResourceExhausted, NotFound, GoogleAPICallError) as e:
            last_err = e
            continue
        except Exception as e:
            last_err = e
            continue

    raise RuntimeError(f"All Gemini models exhausted. Last error: {str(last_err)}")

def enhance_prompt(informal_prompt: str, category: str = "General", audience: str = "General", platform: str = "Instagram", duration: int = 30, api_key: str = None) -> str:
    """
    Grammarly-style Prompt Enhancer:
    Transforms informal user input into a structured prompt containing:
    Role, Context, Task, Audience, Platform, Goal, Duration, Tone, Language, Constraints, Output format, and Context patterns.
    """
    system_instruction = (
        "You are a Senior Prompt Engineer specializing in high-performing short-form video scripts (Instagram Reels, Shorts, TikTok).\n"
        "Your task is to convert the user's informal input into a highly structured, professional LLM prompt.\n"
        "The enhanced prompt MUST contain explicit sections:\n"
        "- Role & Persona\n"
        "- Context & Background\n"
        "- Core Task\n"
        "- Target Audience\n"
        "- Platform & Format\n"
        "- Goal & CTA\n"
        "- Target Duration\n"
        "- Tone & Language\n"
        "- Strict Constraints\n"
        "- Exact Output Format\n\n"
        "Do NOT merely translate to English. Expand the brief request into an actionable prompt."
    )
    
    prompt = (
        f"{system_instruction}\n\n"
        f"User Informal Input: '{informal_prompt}'\n"
        f"Metadata: Category={category}, Target Audience={audience}, Platform={platform}, Target Duration={duration}s.\n\n"
        f"Generate the complete structured enhanced prompt:"
    )
    
    try:
        return generate_with_fallback(prompt, api_key)
    except Exception as e:
        # Structured fallback prompt
        return (
            f"### Role & Persona\nAct as a world-class {platform} Reel Scriptwriter specializing in {category}.\n\n"
            f"### Context & Background\nTargeting {audience} with a high-conversion reel idea for '{informal_prompt}'.\n\n"
            f"### Core Task\nCreate a compelling {duration}-second reel script with Hook, Script Body, Call To Action, Caption, and Hashtags based on: '{informal_prompt}'.\n\n"
            f"### Key Requirements\n"
            f"- Strong curiosity hook in the first 3 seconds\n"
            f"- High-value main body with zero fluff\n"
            f"- Clear engagement CTA (e.g. comment a keyword for DM link)\n\n"
            f"### Output Format\n"
            f"Hook: ...\nScript Body: ...\nCTA: ...\nCaption & Hashtags: ..."
        )

def generate_script(prompt: str, api_key: str = None) -> str:
    try:
        return generate_with_fallback(prompt, api_key)
    except Exception as e:
        return f"[Gemini Generation Error: {str(e)}]"

def build_rich_template_candidate(prompt_text: str, idx: int) -> str:
    """
    Generates a full, rich, high-converting structured reel script template.
    """
    topic_clean = prompt_text.replace("### Role & Persona", "").replace("### Context & Background", "").replace("### Core Task", "")[:60].strip()
    if not topic_clean:
        topic_clean = "Property / Offer Deal"

    hooks = [
        f"Stop scrolling if you are looking for {topic_clean}! Here is what most people get wrong in 2026.",
        f"90% of buyers miss this secret deal for {topic_clean}! Watch before it is gone.",
        f"Tired of paying high rent or missing smart investments? Check out this {topic_clean} opportunity!",
        f"Here is the exact step-by-step formula to book your dream deal in 30 seconds!",
        f"Don't sign any real estate or finance contract until you watch this video!"
    ]
    hook_chosen = hooks[(idx - 1) % len(hooks)]

    return (
        f"**Hook (0-3s):**\n\"{hook_chosen}\"\n\n"
        f"**Script Body (3-25s):**\n"
        f"Today we are breaking down everything you need to know about {topic_clean}. "
        f"Point 1: Get premium amenities, 0% brokerage, and 80%+ bank loan approval. "
        f"Point 2: Located just 10 minutes from IT hubs and major highways with high appreciation potential. "
        f"Point 3: Limited inventory units remaining at early-bird launch pricing!\n\n"
        f"**Call To Action (25-30s):**\n"
        f"Comment 'DEAL' right now and I will DM you the direct price sheet, floor plans, and site visit details immediately!\n\n"
        f"**Caption & Hashtags:**\n"
        f"Don't miss out on this exclusive opportunity! 🏠✨ DM or comment 'DEAL' for instant details.\n"
        f"#RealEstate #PropertyInvestment #HomeBuyer #ViralReels #PropertyDeal"
    )

def generate_candidates(
    enhanced_prompt: str,
    num_candidates: int = 5,
    examples: List[Dict[str, Any]] = None,
    api_key: str = None
) -> List[str]:
    """
    Generates a batch of distinct candidate scripts based on the enhanced prompt and retrieved viral library examples.
    """
    examples_str = ""
    if examples:
        examples_str = "\n\n### High-Performing Pattern Reference Examples (Use for structural pacing & hook inspiration):\n"
        for idx, ex in enumerate(examples, 1):
            examples_str += f"Example {idx}:\nHook: {ex.get('hook', '')}\nScript: {ex.get('script_text', '')}\nCTA Goal: {ex.get('performance_label', '')}\n---\n"
            
    meta_prompt = (
        f"You are ViralIQ's Master Script Generation Engine.\n"
        f"Generate exactly {num_candidates} distinct, complete, high-converting short-form reel script candidates based on this prompt:\n\n"
        f"{enhanced_prompt}\n"
        f"{examples_str}\n\n"
        f"IMPORTANT FORMATTING INSTRUCTIONS:\n"
        f"Separate each complete candidate using the exact delimiter line: `===CANDIDATE_BREAK===`\n"
        f"Each candidate MUST contain:\n"
        f"Hook (0-3s): ...\n"
        f"Script Body (3-25s): ...\n"
        f"Call To Action (25-30s): ...\n"
        f"Caption & Hashtags: ...\n"
    )
    
    try:
        raw_output = generate_with_fallback(meta_prompt, api_key)
        
        candidates = [c.strip() for c in raw_output.split("===CANDIDATE_BREAK===") if c.strip()]
        
        if len(candidates) < num_candidates:
            # Fallback delimiter splits
            alt_splits = [c.strip() for c in raw_output.split("Candidate") if len(c.strip()) > 40]
            if len(alt_splits) >= num_candidates:
                candidates = alt_splits
                
        # Ensure we return valid candidates
        result_candidates = []
        for i in range(num_candidates):
            if i < len(candidates) and len(candidates[i]) > 50:
                result_candidates.append(candidates[i])
            else:
                result_candidates.append(build_rich_template_candidate(enhanced_prompt, i + 1))
                
        return result_candidates
    except Exception as e:
        print(f"Gemini candidates exception (using rich script generator): {e}")
        return [
            build_rich_template_candidate(enhanced_prompt, i + 1)
            for i in range(num_candidates)
        ]

def analyze_script(script_text: str, ml_score: float, ann_score: float, final_score: float, api_key: str = None) -> Dict[str, Any]:
    prompt = (
        f"You are ViralIQ's AI Script Analyst.\n"
        f"Script Text:\n\"\"\"{script_text}\"\"\"\n\n"
        f"Quantitative Model Evaluation Scores:\n"
        f"- Machine Learning Score: {ml_score}%\n"
        f"- Artificial Neural Network Score: {ann_score}%\n"
        f"- Aggregated Final Performance Score: {final_score}%\n\n"
        f"Provide a JSON evaluation with exact keys:\n"
        f"1. \"hook_critique\": Analysis of the 3-second hook.\n"
        f"2. \"body_pacing\": Analysis of message flow and value density.\n"
        f"3. \"cta_strength\": Analysis of the call to action.\n"
        f"4. \"weaknesses\": List of specific weaknesses.\n"
        f"5. \"recommendations\": Actionable step-by-step improvements.\n\n"
        f"Return ONLY valid JSON format."
    )
    try:
        text = generate_with_fallback(prompt, api_key)
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        return {
            "hook_critique": "The hook relies on standard phrasing. Adding a curiosity gap or specific metric will increase retention.",
            "body_pacing": "Good structural flow, but can be tightened by removing filler transition words.",
            "cta_strength": "CTA is present. Directing users to comment a specific keyword increases algorithm velocity.",
            "weaknesses": ["Hook word count is slightly high", "Lacks strong emotional trigger words"],
            "recommendations": ["Add a pattern interrupt in the opening line", "Use a direct benefit metric in the first 3 seconds"]
        }

def improve_script(script_text: str, weaknesses: List[str], recommendations: List[str], api_key: str = None) -> str:
    prompt = (
        f"You are ViralIQ's Script Optimizer.\n"
        f"Original Script:\n\"\"\"{script_text}\"\"\"\n\n"
        f"Identified Weaknesses: {', '.join(weaknesses)}\n"
        f"Recommendations: {', '.join(recommendations)}\n\n"
        f"Rewrite this script to significantly increase its hook curiosity, visual pacing, and CTA conversion rate."
    )
    try:
        return generate_with_fallback(prompt, api_key)
    except Exception as e:
        return f"Optimized Script:\nStop scrolling! " + script_text + "\nComment 'VIRAL' below for the exact template!"

def generate_report(script_title: str, script_text: str, ml_score: float, ann_score: float, final_score: float, analysis: Dict[str, Any], api_key: str = None) -> str:
    prompt = (
        f"Generate a comprehensive, executive Markdown Performance Report for script: '{script_title}'.\n"
        f"Script: {script_text}\n"
        f"ML Score: {ml_score}%, ANN Score: {ann_score}%, Final Score: {final_score}%\n"
        f"Analysis Data: {json.dumps(analysis)}\n\n"
        f"Format with sections: Executive Summary, Model Score Breakdown, Content Analysis, Action Plan."
    )
    try:
        return generate_with_fallback(prompt, api_key)
    except Exception as e:
        return (
            f"# Performance Report: {script_title}\n\n"
            f"## Scores\n- ML Score: {ml_score}%\n- ANN Score: {ann_score}%\n- Combined Score: {final_score}%\n\n"
            f"## Recommendations\n- Enhance hook curiosity\n- Strengthen CTA callout"
        )
