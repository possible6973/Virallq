import re
import numpy as np

CURIOSITY_WORDS = {
    'secret', 'stop', 'mistake', 'myth', 'illegal', 'hack', 'trick', 'failing',
    'don\'t', 'never', 'hidden', 'proof', 'truth', 'exposed', 'shocking', 'formula',
    'cheat', 'weird', 'banned', 'quietly', 'free', 'lakh', 'crore'
}

CTA_WORDS = {
    'comment', 'share', 'save', 'link', 'bio', 'dm', 'follow', 'subscribe',
    'double tap', 'click', 'check out', 'drop', 'download', 'tag'
}

EMOTION_WORDS = {
    'free', 'secret', 'dangerous', 'worst', 'ultimate', 'double', 'quick',
    'fail', 'guaranteed', 'luxury', 'dream', 'insane', 'unbelievable', 'massive',
    'fail', 'rich', 'poor', 'lose', 'gain', 'easy', 'simple', 'fast'
}

URGENCY_WORDS = {
    'now', 'today', 'before', 'immediately', 'stop', 'hurry', 'limited', 'quick', 'fast'
}

FEATURE_NAMES = [
    'word_count',
    'estimated_duration',
    'duration_diff',
    'hook_word_count',
    'hook_has_question',
    'hook_curiosity_score',
    'cta_present',
    'question_count',
    'number_count',
    'emotional_density',
    'avg_sentence_len',
    'has_listicle',
    'line_count',
    'you_count',
    'urgency_score'
]

def extract_script_features(script_text: str, target_duration: int = 30) -> dict:
    text = script_text.strip() if script_text else ""
    if not text:
        return {name: 0.0 for name in FEATURE_NAMES}
    
    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    
    # 1. Word Count
    word_count = total_words
    
    # 2. Estimated Duration (typical speaking rate ~2.3 - 2.6 words/sec)
    est_duration = total_words / 2.5 if total_words > 0 else 0.0
    
    # 3. Duration Difference
    duration_diff = abs(est_duration - target_duration)
    
    # Sentences
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    first_sentence = sentences[0] if sentences else ""
    hook_words = re.findall(r'\b\w+\b', first_sentence.lower())
    hook_word_count = len(hook_words)
    
    # 4. Hook Has Question
    hook_has_question = 1.0 if ('?' in first_sentence or any(w in ['why', 'how', 'what', 'who', 'where', 'are', 'is', 'do'] for w in hook_words[:3])) else 0.0
    
    # 5. Hook Curiosity Score
    hook_curiosity_matches = sum(1 for w in hook_words if w in CURIOSITY_WORDS)
    hook_curiosity_score = float(hook_curiosity_matches)
    
    # 6. CTA Present
    text_lower = text.lower()
    cta_present = 1.0 if any(cta in text_lower for cta in CTA_WORDS) else 0.0
    
    # 7. Question Count
    question_count = float(text.count('?'))
    
    # 8. Number Count (digit sequences or spelled numbers)
    number_count = float(len(re.findall(r'\d+', text)))
    
    # 9. Emotional Density
    emotion_matches = sum(1 for w in words if w in EMOTION_WORDS)
    emotional_density = (emotion_matches / total_words) * 100.0 if total_words > 0 else 0.0
    
    # 10. Avg Sentence Length
    avg_sentence_len = total_words / len(sentences) if sentences else 0.0
    
    # 11. Has Listicle
    has_listicle = 1.0 if (re.search(r'\b(step\s*\d|\d\s*tool|\d\s*way|\d\s*reason|number\s*\d|\d\s*step|\d:)\b', text_lower)) else 0.0
    
    # 12. Line Count
    line_count = float(len([line for line in text.split('\n') if line.strip()]))
    
    # 13. Direct Addressing ("you", "your", "you're")
    you_matches = sum(1 for w in words if w in {'you', 'your', 'youre', 'yours'})
    you_count = float(you_matches)
    
    # 14. Urgency Score
    urgency_matches = sum(1 for w in words if w in URGENCY_WORDS)
    urgency_score = float(urgency_matches)
    
    return {
        'word_count': float(word_count),
        'estimated_duration': float(est_duration),
        'duration_diff': float(duration_diff),
        'hook_word_count': float(hook_word_count),
        'hook_has_question': float(hook_has_question),
        'hook_curiosity_score': float(hook_curiosity_score),
        'cta_present': float(cta_present),
        'question_count': float(question_count),
        'number_count': float(number_count),
        'emotional_density': float(emotional_density),
        'avg_sentence_len': float(avg_sentence_len),
        'has_listicle': float(has_listicle),
        'line_count': float(line_count),
        'you_count': float(you_count),
        'urgency_score': float(urgency_score)
    }

def features_to_vector(features_dict: dict) -> np.ndarray:
    return np.array([[features_dict[name] for name in FEATURE_NAMES]], dtype=np.float32)
