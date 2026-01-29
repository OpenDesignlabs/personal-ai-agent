import pyautogui
import base64
import os
from io import BytesIO
from Backend.Chatbot import GroqAPIKey
from groq import Groq

client = Groq(api_key=GroqAPIKey)

def capture_screen():
    """Captures the primary screen and saves it as a temp file."""
    screenshot = pyautogui.screenshot()
    path = "Data/screen.png"
    os.makedirs("Data", exist_ok=True)
    screenshot.save(path)
    return path

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_screen(prompt="What is on my screen?"):
    """Captures screen and uses Vision AI to explain it."""
    try:
        image_path = capture_screen()
        base64_image = encode_image(image_path)
        
        # Using Llama-3.2 Vision model on Groq
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=1024,
        )
        
        # Cleanup
        if os.path.exists(image_path):
            os.remove(image_path)
            
        return response.choices[0].message.content
    except Exception as e:
        return f"Vision Error: {str(e)}"

if __name__ == "__main__":
    print(analyze_screen("Describe the code in this editor."))
