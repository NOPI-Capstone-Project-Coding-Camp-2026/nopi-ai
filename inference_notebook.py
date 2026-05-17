# ----------------------------------------
# Gabungin model CNN dan OCR (paddle ocr)
# ----------------------------------------

# -*- coding: utf-8 -*-
"""
Full Pipeline Inference: CNN Classification + PaddleOCR + Regex Parser
"""

# =========================================================================================
# KODE AGAR ANTI-CRASH (JANGAN DIHAPUS) !!!!!!
import os
# Memaksa Protobuf pakai mode pure-python agar TensorFlow (CNN) dan PaddleOCR tidak bentrok
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
# =========================================================================================

import tensorflow as tf
from custom_layer import FeatureScalingLayer
from custom_layer import custom_loss
import cv2
import numpy as np
from PIL import Image
import json


# IMPORT PADDLE OCR 
from paddle_ocr import extract_text_paddle
from paddle_parser import parse_paddleocr_text


# LOAD MODEL CNN
model = tf.keras.models.load_model(
    "model2.keras", 
    custom_objects={'custom_loss': custom_loss, 'FeatureScalingLayer': FeatureScalingLayer}
)

IMG_SIZE = (224, 224)

# 1. LOAD IMAGE
def load_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


# 2. PREPROCESS FOR CNN
def preprocess_for_cnn(image):
    img = Image.fromarray(image)
    img = img.resize(IMG_SIZE)

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


# 4. CNN CLASSIFIER
def predict_receipt(image_array):
    pred = model.predict(image_array, verbose=0)[0][0]

    label = "struk" if pred > 0.5 else "non_struk"
    confidence = float(pred if pred > 0.5 else 1 - pred)

    return label, confidence


# 5. OCR ENGINE (PADDLE OCR)
def run_ocr(image_path):
    """
    Menjalankan PaddleOCR
    """
    print("📝 Menjalankan PaddleOCR...")
    return extract_text_paddle(image_path)


# 6. PARSER HASIL OCR (PADDLE PARSER)
def parse_receipt(text):
    """
    Menjalankan Rule-Based Regex milik Paddle
    """
    print("✂️ Memotong teks dengan Regex...")
    # Parser paddle mengembalikan format string JSON, kita ubah jadi Dictionary (Object)
    json_str = parse_paddleocr_text(text)
    try:
        parsed_data = json.loads(json_str)
    except:
        parsed_data = {"nama_toko": "", "tanggal": "", "items": []}
    
    return {
        "raw_text": text,
        "parsed_items": parsed_data
    }


# 7. FULL PIPELINE
def inference_pipeline(image_path):
    # 1. load image
    image = load_image(image_path)

    # 2. preprocessing (split CNN & OCR)
    cnn_input = preprocess_for_cnn(image)

    # 3. CNN prediction
    label, confidence = predict_receipt(cnn_input)

    # 4. filter non-struk
    if label == "non_struk":
        return {
            "status": "rejected",
            "stage": "cnn",
            "reason": "Bukan struk",
            "confidence": confidence
        }

    # 5. OCR (panggil Paddle dengan image_path)
    text = run_ocr(image_path)

    # 6. parsing
    data = parse_receipt(text)

    # 7. output final
    return {
        "status": "success",
        "stage": "cnn+ocr+parser",
        "cnn_confidence": confidence,
        "data": data
    }

# # BLOK UJI COBA (Jalan kalau di-Run langsung)
# if __name__ == "__main__":
#     import json
    
#     # Sesuaikan path dengan nama file gambar struk yang ada di laptop
#     gambar_tes = "struk_tes.jpeg" 
    
#     print(f"\n🚀 MEMULAI UJI COBA PIPELINE...")
#     print(f"📂 Gambar yang diproses: {gambar_tes}")
    
#     try:
#         # Jalankan fungsi gabungan kalian!
#         hasil_akhir = inference_pipeline(gambar_tes)
        
#         # Tampilkan hasilnya dengan format JSON yang rapi
#         print("\n📦 HASIL AKHIR (Siap dikirim ke Frontend):")
#         print(json.dumps(hasil_akhir, indent=4))
        
#     except Exception as e:
#         print(f"\n💥 YAH ERROR: {e}")