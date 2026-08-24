import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.gemini_service import enhance_prompt as gemini_enhance_prompt
from database.crud import search_viral_scripts

def enhance_user_prompt(
    informal_text: str,
    category: str = "General",
    audience: str = "General",
    platform: str = "Instagram",
    duration: int = 30,
    api_key: str = None
) -> str:
    """
    Enhances raw user prompt into a structured prompt using Gemini and contextual viral library patterns.
    """
    if not informal_text or not informal_text.strip():
        return "Please enter a valid script topic or requirement."
        
    # Retrieve relevant contextual examples from SQLite Viral Script Library
    examples = search_viral_scripts(category=category, topic=informal_text, limit=2)
    
    enhanced = gemini_enhance_prompt(
        informal_prompt=informal_text,
        category=category,
        audience=audience,
        platform=platform,
        duration=duration,
        api_key=api_key
    )
    
    # Inject context from database if available
    if examples:
        context_block = "\n\n### Relevant High-Performing Script Context (From SQLite Viral Library):\n"
        for ex in examples:
            context_block += f"- Pattern: {ex['category']} | Hook: \"{ex['hook']}\" | Engagement Rate: {ex['engagement_rate']}%\n"
        enhanced += context_block
        
    return enhanced
