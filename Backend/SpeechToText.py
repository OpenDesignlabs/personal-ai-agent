import os
import time
import numpy as np
import pyaudio
import wave
from dotenv import dotenv_values
import mtranslate as mt
try:
    import whisper
except ImportError as e:
    print(f"Error importing Whisper: {e}")
    raise

# Load environment variables from the .env file.
env_vars = dotenv_values(os.path.join(os.path.dirname(__file__), '..', '.env'))
InputLanguage = env_vars.get("InputLanguage", "en")

# Audio recording parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5  # Reduced from 10 for faster processing
TEMP_AUDIO_PATH = "Data/temp_audio.wav"
silence_threshold = 50

# Ensure Data directory exists
os.makedirs("Data", exist_ok=True)

# Define the path for temporary files.
current_dir = os.getcwd()
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
os.makedirs(TempDirPath, exist_ok=True)

# Function to set the assistant's status by writing it to a file.
def SetAssistantStatus(Status):
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding='utf-8') as file:
        file.write(Status)

# Function to modify a query to ensure proper punctuation and formatting.
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]
    if any(word + " " in new_query for word in question_words):
        if query_words and query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words and query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

# Function to translate text into English using the mtranslate library.
def UniversalTranslator(Text):
    try:
        english_translation = mt.translate(Text, "en", "auto")
        return english_translation.capitalize()
    except Exception as e:
        return Text

# Function to record audio and perform speech recognition using Whisper
def SpeechRecognition():
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    except Exception as e:
        return "[Audio initialization failed]"

    print("Listening... Please speak.")
    
    frames = []
    max_wait = 15
    timeout = time.time() + max_wait
    silence_duration = 2
    last_sound_time = time.time()

    # Record audio
    try:
        while time.time() < timeout:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
            
            audio_data = np.frombuffer(data, dtype=np.int16)
            rms = np.sqrt(np.mean(np.square(audio_data), where=(audio_data!=0)))
            if rms > silence_threshold:
                last_sound_time = time.time()
            elif time.time() - last_sound_time > silence_duration:
                break
    except Exception as e:
        stream.stop_stream()
        stream.close()
        p.terminate()
        return "[Recording error]"

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a WAV file
    if frames:
        try:
            wf = wave.open(TEMP_AUDIO_PATH, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            time.sleep(1)
        except Exception as e:
            return "[Audio file saving error]"

        # Transcribe the audio using Whisper
        try:
            model = whisper.load_model("small")  # Changed to small model for speed
            if os.path.exists(TEMP_AUDIO_PATH) and os.path.getsize(TEMP_AUDIO_PATH) > 0:
                result = model.transcribe(TEMP_AUDIO_PATH, fp16=False)  # CPU-only, FP32
                text = result["text"].strip()
                if os.path.exists(TEMP_AUDIO_PATH):
                    os.remove(TEMP_AUDIO_PATH)
                if text:
                    return text
                else:
                    return "[No speech detected]"
            else:
                return "[No audio file for transcription]"
        except Exception as e:
            return f"[Transcription error: {str(e)}]"
    else:
        return "[No speech detected]"

if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        print(f"Final output: {Text}")