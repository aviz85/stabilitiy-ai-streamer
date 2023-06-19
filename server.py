from flask import Flask, request, make_response
from flask_cors import CORS
from flask import send_from_directory
from PIL import Image
import numpy as np
import cv2
import base64
import os
import io
import requests
import time

def resize_image(input_image_path, output_image_path, size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    print(f"The original image size is {width} wide x {height} tall")

    resized_image = original_image.resize(size)
    width, height = resized_image.size
    print(f"The resized image size is {width} wide x {height} tall")
    resized_image.show()
    resized_image.save(output_image_path)

def crop_and_resize_image(image, size):
    width, height = image.size
    min_dim = min(width, height)
    left = (width - min_dim)/2
    top = (height - min_dim)/2
    right = (width + min_dim)/2
    bottom = (height + min_dim)/2

    cropped_image = image.crop((left, top, right, bottom))

    # Resize the image
    return cropped_image.resize(size)

def decode_image(image_data):
    # Decode the base64 image
    base64_img_bytes = image_data[image_data.find(",")+1:].encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    image = Image.open(io.BytesIO(decoded_image_data))

    # Crop and resize image
    resized_image = crop_and_resize_image(image, (512, 512))

    # Convert the image to RGB before saving if it's in RGBA
    if resized_image.mode in ("RGBA", "P"):
        resized_image = resized_image.convert("RGB")

    # Save the resized image to a BytesIO object
    temp_image_io = io.BytesIO()
    resized_image.save(temp_image_io, format='JPEG')
    temp_image_io.seek(0)

    return Image.open(temp_image_io)




app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5002"}})

@app.route('/input-image')
def serve_image():
    return send_from_directory('.', 'input.png')



@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/save-image', methods=['POST'])
def save_image():
    image = request.json['image']
    image = decode_image(image)

    # Save the image
    cv2.imwrite('frame.png', cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))

    # Call the API every 2 seconds
    if int(time.time()) % 2 == 0:
        send_to_api()

    return 'Image received'

def decode_image(image_data):
    # Decode the base64 image
    base64_img_bytes = image_data[image_data.find(",")+1:].encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    image = Image.open(io.BytesIO(decoded_image_data))

    # Crop and resize image
    resized_image = crop_and_resize_image(image, (512, 512))

    # Convert the image to RGB before saving if it's in RGBA
    if resized_image.mode in ("RGBA", "P"):
        resized_image = resized_image.convert("RGB")

    # Save the resized image to a temporary location
    temp_image_path = "/tmp/resized_image.jpg"
    resized_image.save(temp_image_path)

    return Image.open(temp_image_path)

def send_to_api():
    engine_id = "stable-diffusion-v1-5"
    api_host = os.getenv("API_HOST", "https://api.stability.ai")
    api_key = os.getenv("STABILITY_API_KEY")

    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/image-to-image",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        files={
            "init_image": open('frame.png', 'rb')
        },
        data={
            "image_strength": 0.4,
            "init_image_mode": "IMAGE_STRENGTH",
            "text_prompts[0][text]": "cyborg man cyberpunk dystopian",
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "samples": 1,
            "steps": 10,
            "seed": 100
        }
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    for i, image in enumerate(data["artifacts"]):
        with open(f"input.png", "wb") as f:
            f.write(base64.b64decode(image["base64"]))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)
