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
    """Returns a system message modifier based on sentiment."""
    if sentiment == "happy":
        return "The user is in a great mood. Be cheerful, use emojis occasionally, and match their energy!"
    elif sentiment == "sad":
        return "The user seems a bit down. Be extra supportive, gentle, and encouraging."
    elif sentiment == "angry":
        return "The user is frustrated. Be extremely professional, concise, and helpful. Avoid jokes."
    else:
        return "Be your usual helpful, professional AI self."
