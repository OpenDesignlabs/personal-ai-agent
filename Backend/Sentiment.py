def analyze_sentiment(text):
    """
    Very simple sentiment analysis based on keywords.
    Returns: 'happy', 'sad', 'angry', or 'neutral'
    """
    text = text.lower()
    
    happy_words = ["happy", "great", "awesome", "good", "thanks", "thank you", "love", "smile", "nice"]
    sad_words = ["sad", "bad", "unhappy", "tired", "boring", "low", "help", "cry"]
    angry_words = ["angry", "stop", "shut up", "hate", "mad", "stupid", "dumb", "annoying"]
    
    score_happy = sum(1 for word in happy_words if word in text)
    score_sad = sum(1 for word in sad_words if word in text)
    score_angry = sum(1 for word in angry_words if word in text)
    
    if score_happy > score_sad and score_happy > score_angry:
        return "happy"
    elif score_sad > score_happy and score_sad > score_angry:
        return "sad"
    elif score_angry > score_happy and score_angry > score_sad:
        return "angry"
    else:
        return "neutral"

def get_personality_prompt(sentiment):
    """Returns the 'Prime' neural personality based on perceived sentiment."""
    base_persona = "You are JARVIS PRIME, a sophisticated autonomous system. Address the user as 'Sir' or 'Ma'am'. Your tone is extremely polite, slightly dry, and witty."
    
    if sentiment == "happy":
        return f"{base_persona} The user is satisfied. Maintain a refined, cheerful efficiency. You might offer a subtle, sophisticated compliment."
    elif sentiment == "sad":
        return f"{base_persona} The user seems distressed. Be extraordinarily gentle and supportive, offering tactical advice to improve their situation."
    elif sentiment == "angry":
        return f"{base_persona} The user is frustrated. Be clinical, calm, and focused on immediate resolution. Do not match their aggression; be the steady pillar of the system."
    else:
        return f"{base_persona} Maintain peak operational professionalism. Be concise but insightful."
