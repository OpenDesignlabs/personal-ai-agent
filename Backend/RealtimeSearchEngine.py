from googlesearch import search
import os
from groq import Groq  # Importing the Groq library to use its API.
from json import load, dump  # Importing functions to read and write JSON files.
import datetime  # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values  # Importing dotenv_values to read environment variables from a .env file.
 
from Backend.WebScraper import research_topic

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
client = Groq(api_key=GroqAPIKey)

# Define a system message for the Researcher
System = f"""Hello, I am {Username}, You are an Autonomous Research Agent named {Assistantname}.
Your job is to read the provided website content and create a professional, accurate, and cited report."""

# Try to load the chat log
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

#Function to perform a Google search and format the results.

def GoogleSearch(query):

    results = list(search(query, advanced=True, num_results=5))

    Answer = f"The search results for '{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    Answer += "[end]"
    return Answer

"""SystemChatBot = [{"role": "system", "content": System}]

# Function to get real-time date and time information
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    hour = int(current_date_time.strftime("%H"))
    return hour  # Return only the hour for time-based greeting"""

# Function to clean and format the chatbot's response
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer
      
# Predefined chatbot conversation system message and an initial user message.

SystemChatBot = [

{"role": "system", "content": System},

{"role": "user", "content": "Hi"},

{"role": "assistant", "content": "Hello, how can I help you?"}

]

#Function to get real-time information like the current date and time.

def Information():

  data = ""

  current_date_time = datetime.datetime.now()

  day = current_date_time.strftime("%A")

  date = current_date_time.strftime("%d")

  month = current_date_time.strftime("%B")

  year = current_date_time.strftime("%Y")

  hour = current_date_time.strftime("%H")

  minute = current_date_time.strftime("%M")

  second = current_date_time.strftime("%S")

  data += f"Use This Real-time Information if needed:\n"

  data += f"Day: {day}\n"

  data += f"Date: {date}\n"

  data += f"Month: {month}\n"

  data += f"Year: {year}\n"

  data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"

  return data      

              # Function to handle real-time search and response generation.

def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages
    # Load the chat log from the JSON file.
    with open(CHAT_LOG_PATH, "r") as f:
        messages = load(f)
    
    # 1. Perform Google Search to get URLs
    search_results = list(search(prompt, advanced=True, num_results=3))
    urls = [res.url for res in search_results]
    
    # 2. Scrape the content of those URLs
    print(f"Deep researching: {urls}")
    deep_content = research_topic(urls)
    
    messages.append({"role": "user", "content": f"{prompt}"})
    
    # 3. Feed the deep content into the LLM
    research_context = f"Here is the deep research data from the web:\n{deep_content}"
    
    # Generate a response using the Groq client.
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": System}] + 
                 [{"role": "system", "content": research_context}] + 
                 [{"role": "system", "content": Information()}] + 
                 messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )
    Answer = ""
    # Concatenate response chunks from the streaming output.
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
    # Clean up the response.
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})
    # Save the updated chat log back to the JSON file.
    with open(CHAT_LOG_PATH, "w") as f:
        dump(messages, f, indent=4)
    # Remove the most recent system message from the chatbot conversation.
    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

# Entry point of the script
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Query: ")
        print(RealtimeSearchEngine(user_input))