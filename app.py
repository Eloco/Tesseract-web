import os
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, render_template, jsonify
from PIL import Image
import pytesseract
import io

app = Flask(__name__)
executor = ThreadPoolExecutor(2)


def process_image(image_data, lang, config):
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image, lang=lang, config=config)
    return text


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Read the uploaded image data
        image_file = request.files['image']
        image_data = image_file.read()

        # Get the language parameter from the request
        lang = request.form.get('lang', 'eng')  # Default language is English ('eng')

        # Get the config parameter from the request
        config = request.form.get('config', '')  # Default config is empty string

        # Process the image using OCR
        future = executor.submit(process_image, image_data, lang, config)

        # Get the OCR result
        result = future.result()

        # Return the result as JSON response
        return jsonify({'result': result})

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
