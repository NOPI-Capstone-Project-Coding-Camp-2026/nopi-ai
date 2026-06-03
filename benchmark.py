import time
import pandas as pd
# Import fungsi OCR di sini
from paddle_ocr import extract_text_paddle
from paddle_parser import parse_paddleocr_text
from tesseract_ocr import extract_text_tesseract
from tesseract_parser import parse_tesseract_text 
from easy_ocr import extract_text_easy
from easy_parser import parse_easyocr_text

def run_benchmark(image_paths):
    hasil_komparasi = []

    for img in image_paths:
        print(f"\nMemproses: {img}")
        
        # 1. TES PADDLE OCR
        start_time = time.time()
        raw_paddle = extract_text_paddle(img)
        waktu_paddle = round(time.time() - start_time, 2)
        json_paddle = parse_paddleocr_text(raw_paddle)
        
        # 2. TES TESSERACT OCR
        start_time = time.time()
        raw_tesseract = extract_text_tesseract(img)
        waktu_tesseract = round(time.time() - start_time, 2)
        json_tesseract = parse_tesseract_text(raw_tesseract)

        # 3. TES EASY OCR (Nanti Punya Hanna Masuk Sini)

        start_time = time.time()

        raw_easy = extract_text_easy(img)

        waktu_easy = round(
            time.time() - start_time,
            2
        )

        json_easy = parse_easyocr_text(
            raw_easy
        )

        # Simpan hasil sementara
        hasil_komparasi.append({
            "File": img,

            "Waktu_Paddle": waktu_paddle,
            "Hasil_Paddle": json_paddle,

            "Waktu_Tesseract": waktu_tesseract,
            "Hasil_Tesseract": json_tesseract,

            "Waktu_EasyOCR": waktu_easy,
            "Hasil_EasyOCR": json_easy
        })

    # Export ke CSV untuk bahan laporan di GDocs
    df = pd.DataFrame(hasil_komparasi)
    df.to_csv("hasil_komparasi_ocr_coba.csv", index=False)
    print("\n✅ Selesai! Hasil uji coba tersimpan di 'hasil_komparasi_ocr.csv'")

import os

if __name__ == "__main__":
    folder_path = r"dataset_struk/try2"

    daftar_foto = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp"))
    ]

    run_benchmark(daftar_foto)