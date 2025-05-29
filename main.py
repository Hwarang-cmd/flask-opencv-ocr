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

    # ✅ ขั้นตอน preprocessing สำหรับ 7-segment display
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # ปรับ contrast และลบ noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    enhanced = cv2.equalizeHist(blur)
    
    # แปลงเป็น binary image (invert ทำให้ตัวเลขเป็นสีขาวพื้นดำ)
    _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh = 255 - thresh  # Invert เพื่อให้ตัวเลขชัดขึ้น

    # optional: ปรับขนาดเพื่อให้ OCR อ่านง่าย
    scale_percent = 200
    width = int(thresh.shape[1] * scale_percent / 100)
    height = int(thresh.shape[0] * scale_percent / 100)
    resized = cv2.resize(thresh, (width, height), interpolation=cv2.INTER_LINEAR)

    # 🧠 OCR ด้วย EasyOCR
    result = reader.readtext(resized, detail=0, paragraph=False)
    text = ' '.join(result)

    return jsonify({'ocr_text': text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
