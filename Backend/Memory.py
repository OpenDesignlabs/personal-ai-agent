import json
import os
from difflib import get_close_matches

CHAT_LOG_PATH = os.path.join("Data", "ChatLog.json")

def search_memory(query):
    """Searches past conversations for relevant topics."""
    if not os.path.exists(CHAT_LOG_PATH):
        return "I don't have any memories yet."
    
    try:
        with open(CHAT_LOG_PATH, "r") as f:
            messages = json.load(f)
        
        # Simple keyword/similarity search
        relevant_context = []
        query_words = set(query.lower().split())
        
        for msg in messages:
            if msg["role"] == "user":
                msg_content = msg["content"].lower()
                # Check if overlap exists
                if any(word in msg_content for word in query_words if len(word) > 3):
                    relevant_context.append(msg)
        
        if not relevant_context:
            return "I couldn't find anything specific in my memory about that."
        
        # Take last 3 relevant memories
        memories = relevant_context[-3:]
        result = "Based on what we discussed before:\n"
        for m in memories:
            result += f"- You said: {m['content']}\n"
        
        return result
    except Exception as e:
        return f"Error accessing memory: {e}"

def get_last_conversation(limit=5):
    """Returns the last few messages for immediate context."""
    if not os.path.exists(CHAT_LOG_PATH):
        return []
    try:
        with open(CHAT_LOG_PATH, "r") as f:
            messages = json.load(f)
            return messages[-limit:]
    except:
        return []
