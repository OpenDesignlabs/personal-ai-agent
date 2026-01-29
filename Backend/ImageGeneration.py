import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import dotenv_values
import os
from time import sleep

# Function to open and display images based on a given prompt
def open_images(prompt):
    folder_path = r"Data"  # Folder where the images are stored
    prompt = prompt.replace(" ", "_")  # Replace spaces in prompt with underscores
    # Generate the filenames for the images
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]
    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            # Try to open and display the image
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)  # Pause for 1 second before showing the next image
        except IOError:
            print(f"Unable to open {image_path}")

# API details for the Hugging Face Stable Diffusion model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
env_vars = dotenv_values(os.path.join(os.path.dirname(__file__), '..', '.env'))
HuggingFaceAPIKey = env_vars.get("HuggingFaceAPIKey")
headers = {"Authorization": f"Bearer {HuggingFaceAPIKey}"}

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Async function to generate images based on the given prompt
async def generate_images(prompt: str):
    tasks = []
    # Create 4 image generation tasks
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)
    # Wait for all tasks to complete
    image_bytes_list = await asyncio.gather(*tasks)
    # Save the generated images to files
    for i, image_bytes in enumerate(image_bytes_list):
        os.makedirs("Data", exist_ok=True)  # Ensure Data directory exists
        with open(fr"Data\{prompt.replace(' ', '_')}{i+1}.jpg", "wb") as f:  # Fixed replace syntax
            f.write(image_bytes)

# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))  # Generate images first
    open_images(prompt)  # Open the generated images

# Main loop to monitor for image generation requests
def main():
    file_path = r"E:\COde\py\jarvisAI\Frontend\Files\ImageGenration.data"
    try:
        with open(file_path, "r") as f:
            Data: str = f.read()

        Prompt, Status = map(str.strip, Data.split(","))  # Clean inputs
        print(f"Prompt: {Prompt} | Status: {Status}")      # Debugging

        if Status == "True":
            print("Generating Images ... ")
            GenerateImages(prompt=Prompt)

            with open(file_path, "w") as f:
                f.write("False, False")
            print("Exiting main loop as image generation completed.")
        else:
            print("Status is False, exiting main loop.")
    except Exception as e:
        print("Error:", e)
        sleep(1)

if __name__ == "__main__":
    main()