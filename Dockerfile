# --------------------------------------------------------------------------------------
# Mengatur deployment model AI (CNN dan OCR) ke Hugging Face Space dengan PaddleOCR
# --------------------------------------------------------------------------------------

# Pakai komputer Linux dengan Python 3.12 
FROM python:3.12-slim

# Buat folder kerja di dalam cloud
WORKDIR /app

# Mengajari Cloud untuk meng-install library grafis modern dan matematika (libgomp1)
RUN apt-get update && \
    apt-get install -y libgl1 libglib2.0-0 libgomp1 && \
    apt-get clean

# Copy daftar library dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file kodingan ke dalam cloud
COPY . .

# Nyalakan FastAPI di port 7860 (Port wajib dari Hugging Face)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]