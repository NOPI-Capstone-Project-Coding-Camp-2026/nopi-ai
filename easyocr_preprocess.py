# ------------------------------------------------------------------------------------------------
# Preprocess untuk model easy ocr (tidak digunakan saat ini (karna sudah menggunakan paddle ocr), 
# tapi digunakan saat tahapan komparasi 3 model OCR)
# ------------------------------------------------------------------------------------------------

import cv2

# PREPROCESS IMAGE

def get_preprocessed_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(
            f"Gagal membaca gambar: {image_path}"
        )

    # RESIZE

    h, w = image.shape[:2]

    scale = 1400 / max(h, w)

    if scale < 1:

        image = cv2.resize(
            image,
            None,
            fx=scale,
            fy=scale
        )

    # GRAYSCALE

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # DENOISE

    gray = cv2.bilateralFilter(
        gray,
        9,
        75,
        75
    )

    # THRESHOLD

    thresh = cv2.adaptiveThreshold(

        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15

    )

    return thresh