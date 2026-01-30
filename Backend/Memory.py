import json
import os
from difflib import get_close_matches

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAT_LOG_PATH = os.path.join(ROOT_DIR, "Data", "ChatLog.json")

def search_memory(query):
    """Semantic Context Retrieval: Synthesizes past interactions into a 'Memory Synopsis'."""
    if not os.path.exists(CHAT_LOG_PATH):
        return "Memory Core: Empty. No previous interaction data found."
    
    try:
        with open(CHAT_LOG_PATH, "r") as f:
            messages = json.load(f)
        
        # Filter for meaningful keywords (ignore common filler)
        ignore_words = {"the", "and", "that", "this", "your", "with", "what", "where", "tell"}
        query_words = {word for word in query.lower().split() if len(word) > 3 and word not in ignore_words}
        
        matches = []
        # Reverse search to prioritize recent relevance
        for i in range(len(messages)-1, -1, -1):
            msg = messages[i]
            if msg["role"] == "user":
                content = msg["content"].lower()
                if any(word in content for word in query_words):
                    # Find following assistant response for full context
                    response = messages[i+1]["content"] if i+1 < len(messages) else "..."
                    matches.append(f"User: {msg['content']} | You: {response}")
            
            if len(matches) >= 3: break
            
        if not matches:
            return "No specific semantic links found in memory for this topic."
            
        synopsis = "\n".join(matches)
        return f"RELEVANT NEURAL LINKS FOUND:\n{synopsis}"
        
    except Exception as e:
        return f"Memory Parity Error: {e}"

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
