# ✅ Dockerfile แบบเทพ ขนาดไม่เกิน 4GB ใช้ได้บน Railway
FROM python:3.11-slim

# ลดขนาดโดยติดตั้งเฉพาะ lib ที่ EasyOCR และ OpenCV ต้องใช้
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# คัดลอก requirements.txt แล้วติดตั้งด้วย --no-cache-dir และ --prefer-binary
COPY requirements.txt .
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# คัดลอก source code ทั้งหมด
COPY . .

EXPOSE 8080
CMD ["python", "main.py"]
