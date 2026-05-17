# ---------------------------------------------
# Model OCR UTAMA (paddle ocr) dipakai di NOPI,
# TERBAIK DIANTARA 2 MODEL LAINNYA (tesseract dan easy)
# ---------------------------------------------

import cv2
import numpy as np
from paddleocr import PaddleOCR

# Inisialisasi versi 2.7.3 yang stabil dan aman dari bug paddlex
ocr_engine = PaddleOCR(use_angle_cls=False, lang='en', show_log=False)

def extract_text_paddle(image_path: str) -> str:
    """
    Fungsi mengekstrak teks menggunakan standar PaddleOCR v2.7
    """
    try:
        result = ocr_engine.ocr(image_path, cls=False)
        
        if not result or result[0] is None:
            return ""
            
        ocr_lines = []
        for line in result[0]:
            text = line[1][0]  # Mengambil string teks
            ocr_lines.append(text)
            
        full_text = "\n".join(ocr_lines)
        return full_text
        
    except Exception as e:
        return f"Error saat menjalankan PaddleOCR: {str(e)}"

# # --- BLOK TES ---
# if __name__ == "__main__":
#     path_gambar = r"dataset_struk\primer_0071.jpg" 
    
#     print("Mulai membaca dengan PaddleOCR...")
#     hasil_teks = extract_text_paddle(path_gambar)
    
#     print("\n=== HASIL BACAAN PADDLEOCR ===")
#     print(hasil_teks)

