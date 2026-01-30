import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values
import requests  # For network check

# Load environment variables from a .env file
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_vars = dotenv_values(os.path.join(ROOT_DIR, '.env'))
AssistantVoice = env_vars.get("AssistantVoice", "en-CA-LiamNeural")  # Default voice
print(f"Loaded AssistantVoice: {AssistantVoice}")

# Ensure Data directory exists
DATA_DIR = os.path.join(ROOT_DIR, "Data")
os.makedirs(DATA_DIR, exist_ok=True)

# Global event loop to manage asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Check internet connectivity
def check_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        print("No internet connection. Please connect and retry.")
        return False

# Asynchronous function to convert text to an audio file
async def text_to_audio(text):
    file_path = os.path.join(DATA_DIR, "speech.mp3")
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Removed existing file: {file_path}")
        except OSError as e:
            print(f"Error removing file: {e}")
    if not isinstance(AssistantVoice, str) or not AssistantVoice:
        raise ValueError(f"Invalid AssistantVoice: {AssistantVoice}")
    try:
        print(f"Attempting to generate audio with text: {text}")
        communicate = edge_tts.Communicate(text, AssistantVoice)
        await communicate.save(file_path)
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"Successfully generated audio file: {file_path} (size: {os.path.getsize(file_path)} bytes)")
        else:
            raise RuntimeError(f"Audio file generation failed. File exists: {os.path.exists(file_path)}, Size: {os.path.getsize(file_path) if os.path.exists(file_path) else 0} bytes")
    except Exception as e:
        print(f"Error in text_to_audio: {e}")
        raise

def tts(text, func=lambda: True):
    global loop
    try:
        if not check_internet():
            raise ConnectionError("Internet is required for audio generation.")
        loop.run_until_complete(text_to_audio(text))
        file_path = os.path.join(DATA_DIR, "speech.mp3")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        pygame.mixer.init()
        print("Pygame mixer initialized")
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        print("Started playing audio")
        
        while pygame.mixer.music.get_busy():
            if not func():
                break
            pygame.time.wait(10)
        
        # Wait for playback to complete
        pygame.time.wait(2000)
        pygame.mixer.quit()
        
        # Delete the file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Error deleting file: {e}")
        return True
    except Exception as e:
        print(f"Error in tts: {e}")
        return False

def text_to_speech(text):
    sentences = text.split(".")
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]
    if len(sentences) > 4 and len(text) >= 250:
        short_text = ". ".join(sentences[:2]) + "."
        responses = ["Please provide a shorter input.", "Let’s focus on the first part."]
        return tts(short_text + " " + random.choice(responses))
    else:
        return tts(text)

# Main execution loop
if __name__ == "__main__":
    while True:
        user_input = input("Enter the text: ")
        print(f"Processing: {user_input}")
        success = text_to_speech(user_input)
        if not success:
            print("Failed to process the input. Check the error messages above.")