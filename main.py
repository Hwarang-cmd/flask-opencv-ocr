from flask import Flask, request, jsonify
import cv2
import numpy as np
import easyocr
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
reader = easyocr.Reader(['en'], gpu=False)  # เปิด GPU ได้ถ้ารองรับ

@app.route('/')
def home():
    return "Flask OCR API for Blood Pressure Monitor is running!"

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    in_memory_file = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(in_memory_file, cv2.IMREAD_COLOR)

    # 🔍 STEP 1: Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 🔍 STEP 2: Adaptive Threshold (รองรับแสงไม่สม่ำเสมอ)
    adaptive = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=11,
        C=2
    )

    # 🔍 STEP 3: Morphology ลบ noise และเชื่อม segment
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morph = cv2.morphologyEx(adaptive, cv2.MORPH_CLOSE, kernel, iterations=1)

    # 🔍 STEP 4: Resize ให้ใหญ่ขึ้นเพื่อ OCR แม่นยำ
    scale_percent = 250
    width = int(morph.shape[1] * scale_percent / 100)
    height = int(morph.shape[0] * scale_percent / 100)
    resized = cv2.resize(morph, (width, height), interpolation=cv2.INTER_LINEAR)

    # 🔍 STEP 5: OCR เฉพาะตัวเลข
    result = reader.readtext(
        resized,
        detail=0,
        paragraph=False,
        allowlist='0123456789'
    )

    # 🔍 STEP 6: รวมผลลัพธ์แบบสะอาด
    digits_only = ''.join([r.strip() for r in result if r.strip().isdigit()])
    text = ' '.join(result)

    return jsonify({
        'ocr_text_raw': text,
        'ocr_digits_only': digits_only
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
