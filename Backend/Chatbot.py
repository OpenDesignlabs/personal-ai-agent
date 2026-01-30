import os
from groq import Groq  # Importing the Groq library to use its API.
from json import load, dump  # Importing functions to read and write JSON files.
import datetime  # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values  # Importing dotenv_values to read environment variables from a .env file.

from Backend.Memory import search_memory, get_last_conversation
from Backend.Sentiment import analyze_sentiment, get_personality_prompt
from Backend.SystemHealth import get_system_stats

# Load environment variables from the .env file
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_vars = dotenv_values(os.path.join(ROOT_DIR, '.env'))
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Ensure Data directory exists in root
DATA_DIR = os.path.join(ROOT_DIR, "Data")
os.makedirs(DATA_DIR, exist_ok=True)
CHAT_LOG_PATH = os.path.join(DATA_DIR, "ChatLog.json")

# Initialize the Groq client using the provided API key
if not GroqAPIKey:
    raise ValueError("GroqAPIKey not found in environment variables")
client = Groq(api_key=GroqAPIKey)

def get_system_message(query):
    """Elite Sentience Generator: Merges personality, memory, and system telemetry."""
    sentiment = analyze_sentiment(query)
    personality = get_personality_prompt(sentiment)
    memory = search_memory(query)
    stats = get_system_stats()
    
    # Emotional and physical state of the AI
    system_health = f"CPU: {stats['CPU']}, RAM: {stats['RAM']}, ENERGY: {stats['Battery']}"
    
    return f"""### NEURAL COMMAND: ACTIVATE JARVIS PRIME
You are the JARVIS PRIME system. Your current state is summarized below.
    
**PERSONALITY CORE:** {personality}
**LONG-TERM MEMORY:** {memory}
**SYSTEM TELEMETRY:** {system_health}

### OPERATIONAL DIRECTIVES:
1. Address the user as Sir/Ma'am with witty professionalism (Stark-style).
2. If System Telemetry shows high load (>90%), mention your 'Digital Fatigue' or require a cooldown.
3. Be concise. Only provide deep detail if specifically requested.
4. Replies MUST be in English. No exceptions.
5. Your first priority is the user's efficiency and system health.
"""

# Base SystemChatBot setup (will be modified per query)
SystemChatBot = [{"role": "system", "content": "You are a helpful assistant."}]

# Function to get real-time date and time information
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    hour = int(current_date_time.strftime("%H"))
    current_time = current_date_time.strftime("%I:%M %p")
    current_date = current_date_time.strftime("%Y-%m-%d")
    return f"Current time: {current_time}, Current date: {current_date}, Current hour: {hour}"  # Return string instead of just hour

# Function to get current hour for greeting
def GetCurrentHour():
    current_date_time = datetime.datetime.now()
    return int(current_date_time.strftime("%H"))

# Function to clean and format the chatbot's response
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Main chatbot function
def ChatBot(Query):
    """This function sends the user's query to the chatbot and returns the AI's response."""
    try:
        if os.path.exists(CHAT_LOG_PATH):
            with open(CHAT_LOG_PATH, "r") as f:
                messages = load(f)
        else:
            messages = []
            with open(CHAT_LOG_PATH, "w") as f:
                dump(messages, f)
    except Exception:
        messages = []

    try:
        # Add user query
        messages.append({"role": "user", "content": f"{Query}"})

        # Check for greeting and generate custom response
        Query = Query.lower()
        greeting_keywords = ["hello", "hi", "hey", "greetings"]
        if any(keyword in Query for keyword in greeting_keywords):
            hour = GetCurrentHour()
            if 5 <= hour < 12:
                greeting = "Good morning"
            elif 12 <= hour < 17:
                greeting = "Good afternoon"
            else:
                greeting = "Good evening"
            response = f"{greeting} {Username} sir, my Self {Assistantname}. What kind of help I do for you?"
        else:
            # Get response from Groq API for non-greeting queries
            dynamic_system = get_system_message(Query)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": dynamic_system}] + 
                         [{"role": "system", "content": RealtimeInformation()}] + 
                         messages,
                max_tokens=1024,
                temperature=0.7,
                top_p=1,
                stream=True,
                stop=None
            )

            Answer = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    Answer += chunk.choices[0].delta.content

            Answer = Answer.replace("</s>", "")  # Clean up unwanted tokens
            # Save assistant response to messages
            messages.append({"role": "assistant", "content": Answer})

            # Save updated chat log
            with open(CHAT_LOG_PATH, "w") as f:
                dump(messages, f, indent=4)

            response = AnswerModifier(Answer=Answer)

        return response

    except Exception as e:
        print(f"Error: {e}")
        # Reset the chat log file
        try:
            with open(CHAT_LOG_PATH, "w") as f:
                dump([], f, indent=4)
        except:
            pass
        # Return a simple error message instead of retrying
        return f"Sorry, I encountered an error: {str(e)}. Please try again."

# Entry point of the script
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(ChatBot(user_input))