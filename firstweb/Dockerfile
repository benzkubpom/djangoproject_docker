# ใช้ Python เวอร์ชันทางการแบบ slim (เล็ก เบา เหมาะกับ container)
FROM python:3.13-slim

# ไม่ให้ Python เขียนไฟล์ .pyc และให้ log ออกมาทันที ไม่ค้างใน buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# โฟลเดอร์ทำงานภายใน container (ตรงกับ volume .:/app ใน docker-compose.yml)
WORKDIR /app

# คัดลอก requirements.txt เข้ามาก่อน เพื่อใช้ layer cache ตอน build
COPY requirements.txt .

# ติดตั้ง dependency ตาม requirements.txt (--no-cache-dir ไม่เก็บ cache ให้ image เล็กลง)
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดที่เหลือทั้งหมดเข้า container
COPY . .

# บอกว่า container เปิดใช้งาน port 8000
EXPOSE 8000

# คำสั่งเริ่มต้นตอน container รัน: รัน dev server ที่ 0.0.0.0:8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
