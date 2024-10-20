from PIL import ImageGrab
from datetime import datetime
from openai import OpenAI
from read_api_key import read_api_key

import base64


# Capture the screenshot from the clipboard
screenshot = ImageGrab.grabclipboard()

if screenshot:
    # Specify the file path where the screenshot will be saved, by using current date and time
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = f"screenshot_{current_time}.png"

    # Save the screenshot
    screenshot.save(save_path)
    print(f"Screenshot saved at {save_path}")
else:
    print("No image found in the clipboard.")


API_KEY = read_api_key()


client = OpenAI(api_key=API_KEY)


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Getting the base64 string
base64_image = encode_image(save_path)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Convert the image in the file to Latex typeset. Do not create a general Latex preamble. Output just the typeset for the image and nothing else.",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high",
                    },
                },
            ],
        }
    ],
)

with open("output.txt", "w") as file:
    answer = response.choices[0].message.content
    print(answer)
    file.write(answer)
