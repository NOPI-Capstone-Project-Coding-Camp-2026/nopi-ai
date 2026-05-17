# ------------------------------------------------------------------------------
# Model easy ocr (tidak digunakan saat ini (karna sudah menggunakan paddle ocr), 
# tapi digunakan saat tahapan komparasi 3 model OCR)
# ------------------------------------------------------------------------------

import easyocr

from easyocr_preprocess import (
    get_preprocessed_image
)


# INIT EASYOCR
reader = easyocr.Reader(
    ['id', 'en'],
    gpu=False
)


# EXTRACT TEXT EASYOCR
def extract_text_easy(image_path):

    image = get_preprocessed_image(
        image_path
    )

    results = reader.readtext(image)

    parsed_results = []

    for result in results:

        bbox = result[0]
        text = result[1]
        confidence = result[2]

        parsed_results.append({

            "bbox": bbox,
            "text": text,
            "confidence": confidence

        })

    return parsed_results


# TEST
if __name__ == "__main__":

    image_path = r"dataset_struk/primer_0071.jpg"

    hasil = extract_text_easy(
        image_path
    )

    print("\n=== HASIL EASYOCR ===\n")

    for h in hasil:

        print(h)