import sys
import os

print("--- Jarvis Backend Health Check ---")
print(f"Python version: {sys.version}")
print(f"Current Directory: {os.getcwd()}")

modules_to_test = [
    "Backend.Chatbot",
    "Backend.Model",
    "Backend.Automation",
    "Backend.SystemHealth",
    "Backend.Scheduler",
    "Backend.CodeInterpreter",
    "Backend.Vision",
    "Backend.RealtimeSearchEngine",
    "Backend.ImageGeneration",
    "Backend.TextToSpeech",
    "Backend.SpeechToText"
]

for module in modules_to_test:
    try:
        print(f"Testing {module}...", end=" ", flush=True)
        __import__(module)
        print("✅ SUCCESS")
    except Exception as e:
        print(f"❌ FAILED: {e}")

print("--- Check Complete ---")
