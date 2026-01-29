from whisper import load_model
model = load_model("medium")     
result = model.transcribe("Data/temp_audio.wav")
print(result["text"])