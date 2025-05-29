# ใช้ base image ที่เล็กและเร็ว
FROM python:3.11-slim

# ติดตั้ง lib สำหรับ easyocr และ opencv
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ตั้ง working directory
WORKDIR /app

# คัดลอกไฟล์ dependencies และติดตั้ง
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมดเข้ามาใน container
COPY . .

# สั่งให้ container รัน Flask app
CMD ["python", "main.py"]
