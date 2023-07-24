import os
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, render_template, jsonify
from PIL import Image
import pytesseract
import io
import requests

app = Flask(__name__)
executor = ThreadPoolExecutor(2)


def process_image(image_data, lang, config):
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image, lang=lang, config=config)
    return text


def process_image_from_url(image_url, lang, config):
    response = requests.get(image_url)
    image_data = response.content
    return process_image(image_data, lang, config)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the language parameter from the request
        lang = request.form.get('lang', 'eng')  # Default language is English ('eng')

        # Get the config parameter from the request
        config = request.form.get('config', '')  # Default config is an empty string

        # Check if the image is uploaded or provided as a URL
        if 'image' in request.files:
            # Read the uploaded image data
            image_file = request.files['image']
            image_data = image_file.read()
            # Process the image using OCR
            future = executor.submit(process_image, image_data, lang, config)
            # Get the OCR result
            result = future.result()
            # Return the result as JSON response
            return jsonify({'result': result})
        elif 'image_url' in request.form:
            # Get the image URL from the request
            image_url = request.form['image_url']
            # Process the image from the URL using OCR
            future = executor.submit(process_image_from_url, image_url, lang, config)
            result = future.result()
            # Return the result as JSON response
            return jsonify({'result': result})
        else:
            # Return an error response if no image or image URL is provided
            return jsonify({'error': 'No image or image URL provided.'}), 400

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
