import os
from groq import Groq  # Importing the Groq library to use its API.
from json import load, dump  # Importing functions to read and write JSON files.
import datetime  # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values  # Importing dotenv_values to read environment variables from a .env file.

# Load environment variables from the .env file
env_vars = dotenv_values(os.path.join(os.path.dirname(__file__), '..', '.env'))
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using the provided API key
if not GroqAPIKey:
    raise ValueError("GroqAPIKey not found in environment variables")
client = Groq(api_key=GroqAPIKey)

# Define a system message that provides context to the AI chatbot
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
"""

SystemChatBot = [{"role": "system", "content": System}]

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
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
    except FileNotFoundError:
        # Create the Data directory if it doesn't exist
        os.makedirs("Data", exist_ok=True)
        # Initialize an empty messages list and create the file
        messages = []
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f)

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
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
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
            with open(r"Data\ChatLog.json", "w") as f:
                dump(messages, f, indent=4)

            response = AnswerModifier(Answer=Answer)

        return response

    except Exception as e:
        print(f"Error: {e}")
        # Reset the chat log file
        try:
            with open(r"Data\ChatLog.json", "w") as f:
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