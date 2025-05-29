# เบสอิมเมจขนาดเล็ก
FROM python:3.11-slim

# ติดตั้ง dependency ที่จำเป็นสำหรับ EasyOCR และ OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# สร้าง working directory
WORKDIR /app

# คัดลอกและติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอก source code ทั้งหมด
COPY . .

# ระบุพอร์ต (ใช้ตาม Flask ที่รัน)
EXPOSE 8080

# คำสั่งรันแอป
CMD ["python", "main.py"]
