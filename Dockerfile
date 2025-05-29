FROM python:3.10-slim

WORKDIR /app

# ติดตั้ง dependencies ที่จำเป็น พร้อมล้าง cache เพื่อลดขนาด
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# คัดลอกไฟล์ requirements.txt และติดตั้ง Python packages
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์โปรเจกต์อื่นๆ
COPY . .

CMD ["python", "main.py"]
