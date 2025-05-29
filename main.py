from flask import Flask, request, jsonify
import cv2
import numpy as np
import easyocr
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # อนุญาตให้ Flutter frontend เรียกได้
reader = easyocr.Reader(['en'])

@app.route('/')
def home():
    return "Flask OCR API is running!"

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    in_memory_file = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(in_memory_file, cv2.IMREAD_COLOR)

    # 👇 คุณสามารถใส่ preprocessing ด้วย OpenCV ตรงนี้
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    # 👇 อ่านด้วย EasyOCR
    result = reader.readtext(thresh)
    text = ' '.join([item[1] for item in result])

    return jsonify({'ocr_text': text})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
