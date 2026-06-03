import os
import pandas as pd

from paddle_ocr import extract_text_paddle
from easy_ocr import extract_text_easy_raw
from tesseract_ocr import extract_text_tesseract

from metrics_utils import (
    calculate_cer,
    calculate_wer
)

# ======================================================
# DAFTAR FOTO
# ======================================================

daftar_foto = [

    r"dataset_struk/primer_0002.jpg",
    r"dataset_struk/primer_0051.jpg",
    r"dataset_struk/primer_0052.jpg",
    r"dataset_struk/primer_0040.jpg",
    r"dataset_struk/primer_0061.jpg",
    r"dataset_struk/primer_0062.jpg",
    r"dataset_struk/primer_0092.jpg",
    r"dataset_struk/primer_0093.jpg",
    r"dataset_struk/primer_0116.jpg",
    r"dataset_struk/primer_0082.jpg",
    r"dataset_struk/primer_0096.jpg",
    r"dataset_struk/primer_0099.jpg",
    r"dataset_struk/primer_0109.jpg",
    r"dataset_struk/primer_0111.jpg",
    r"dataset_struk/primer_0117.jpg"

]

# ======================================================
# PROCESS
# ======================================================

results = []

total_cer_paddle = []
total_cer_easy = []
total_cer_tesseract = []

total_wer_paddle = []
total_wer_easy = []
total_wer_tesseract = []

for image_path in daftar_foto:

    filename = os.path.basename(
        image_path
    )

    gt_path = os.path.join(
        "ground_truth",
        filename.replace(".jpg", ".txt")
    )

    # skip jika GT tidak ada
    if not os.path.exists(gt_path):

        print(f"Ground Truth tidak ditemukan: {filename}")
        continue

    print(f"Processing {filename}")

    # ==================================================
    # LOAD GROUND TRUTH
    # ==================================================

    with open(
        gt_path,
        "r",
        encoding="utf-8"
    ) as f:

        gt_text = f.read()

    # ==================================================
    # PADDLE OCR
    # ==================================================

    raw_paddle = extract_text_paddle(
        image_path
    )

    cer_paddle = calculate_cer(
        raw_paddle,
        gt_text
    )

    wer_paddle = calculate_wer(
        raw_paddle,
        gt_text
    )

    # ==================================================
    # EASY OCR
    # ==================================================

    raw_easy = extract_text_easy_raw(
        image_path
    )

    cer_easy = calculate_cer(
        raw_easy,
        gt_text
    )

    wer_easy = calculate_wer(
        raw_easy,
        gt_text
    )

    # ==================================================
    # TESSERACT OCR
    # ==================================================

    raw_tesseract = extract_text_tesseract(
        image_path
    )

    cer_tesseract = calculate_cer(
        raw_tesseract,
        gt_text
    )

    wer_tesseract = calculate_wer(
        raw_tesseract,
        gt_text
    )

    # ==================================================
    # SIMPAN TOTAL UNTUK AVG
    # ==================================================

    total_cer_paddle.append(cer_paddle)
    total_cer_easy.append(cer_easy)
    total_cer_tesseract.append(cer_tesseract)

    total_wer_paddle.append(wer_paddle)
    total_wer_easy.append(wer_easy)
    total_wer_tesseract.append(wer_tesseract)

    # ==================================================
    # SIMPAN HASIL
    # ==================================================

    results.append({

        "file_name": filename,
        "raw_text_paddle": raw_paddle,
        "raw_text_easy": raw_easy,
        "raw_text_tasseract": raw_tesseract,

        "cer_paddle": cer_paddle,
        "cer_easy": cer_easy,
        "cer_tesseract": cer_tesseract,

        "wer_paddle": wer_paddle,
        "wer_easy": wer_easy,
        "wer_tesseract": wer_tesseract,

        "ground_truth": gt_text

    })

# ======================================================
# DATAFRAME
# ======================================================

df = pd.DataFrame(results)

# ======================================================
# HITUNG RATA-RATA
# ======================================================

avg_cer_paddle = round(
    sum(total_cer_paddle) / len(total_cer_paddle),
    4
)

avg_cer_easy = round(
    sum(total_cer_easy) / len(total_cer_easy),
    4
)

avg_cer_tesseract = round(
    sum(total_cer_tesseract) / len(total_cer_tesseract),
    4
)

avg_wer_paddle = round(
    sum(total_wer_paddle) / len(total_wer_paddle),
    4
)

avg_wer_easy = round(
    sum(total_wer_easy) / len(total_wer_easy),
    4
)

avg_wer_tesseract = round(
    sum(total_wer_tesseract) / len(total_wer_tesseract),
    4
)

# ======================================================
# TAMBAHKAN AVG KE CSV
# ======================================================

df["avg_cer_paddle"] = avg_cer_paddle
df["avg_cer_easy"] = avg_cer_easy
df["avg_cer_tesseract"] = avg_cer_tesseract

df["avg_wer_paddle"] = avg_wer_paddle
df["avg_wer_easy"] = avg_wer_easy
df["avg_wer_tesseract"] = avg_wer_tesseract

# ======================================================
# BUAT FOLDER RESULTS
# ======================================================

os.makedirs(
    "results",
    exist_ok=True
)

# ======================================================
# SAVE CSV
# ======================================================

output_path = "results/hasil_perbandingan_ocr_V2.csv"

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\nSelesai!")
print(f"Hasil disimpan di: {output_path}")

# ======================================================
# PRINT AVG
# ======================================================

print("\n===== RATA-RATA OCR =====")

print(f"AVG CER Paddle     : {avg_cer_paddle}")
print(f"AVG CER EasyOCR    : {avg_cer_easy}")
print(f"AVG CER Tesseract  : {avg_cer_tesseract}")

print(f"AVG WER Paddle     : {avg_wer_paddle}")
print(f"AVG WER EasyOCR    : {avg_wer_easy}")
print(f"AVG WER Tesseract  : {avg_wer_tesseract}")