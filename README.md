# NOPI AI API

## Brief Description

NOPI AI Models is the artificial intelligence module used in the NOPI (Nota Pintar) application. This repository contains CNN-based receipt classification models, OCR models, OCR parsing systems, benchmarking utilities, and deployment configurations used for automatic receipt transaction extraction.

The system combines a CNN model for receipt validation and PaddleOCR-based extraction to process receipt images into structured transaction data such as item names, quantities, prices, and totals.

---

## Table of Contents

* [NOPI AI API](#nopi-ai-api)

  * [Brief Description](#brief-description)
  * [Table of Contents](#table-of-contents)
  * [Tech Stack](#tech-stack)
  * [Tools](#tools)
  * [Todos](#todos)
  * [Installation](#installation)

    * [Run on Local Environment](#run-on-local-environment)
  * [Workflow](#workflow)
  * [Author](#author)
  * [Thank You](#thank-you)

---

## Tech Stack

1. Python
2. TensorFlow
3. Keras
4. PaddleOCR
5. EasyOCR
6. Tesseract OCR
7. OpenCV
8. FastAPI
9. Pandas
10. NumPy
11. Docker
12. Matplotlib

---

## OCR Models

### PaddleOCR

Main OCR model currently used in NOPI due to better performance compared to other OCR models based on CER and WER evaluation results.

### EasyOCR

Used during OCR benchmarking and model comparison experiments.

### Tesseract OCR

Used as baseline OCR model for OCR comparison and evaluation purposes.

---

## Dataset

The dataset used in this project consists of two main classes:

1. Receipt

   * Primary receipt dataset
   * Secondary receipt dataset

2. Non-Receipt

   * Animal images
   * Landscape images
   * Posters
   * Memes

The receipt and non-receipt datasets are used for CNN model training and receipt image classification. Meanwhile, the OCR module only uses the primary receipt dataset for OCR extraction, parsing evaluation, and benchmarking processes.

---

## Evaluation Metrics

OCR model performance is evaluated using:

* Character Error Rate (CER)
* Word Error Rate (WER)

These evaluation metrics are used to compare text extraction performance between PaddleOCR, EasyOCR, and Tesseract OCR models.

---

## Tools

1. Visual Studio Code
2. Google Colab
3. GitHub
4. Hugging Face Spaces

---

## Todos

* [x] Initialize AI Project
* [x] Prepare Receipt and Non-Receipt Dataset
* [x] Create CNN Receipt Classification Model
* [x] Train CNN Model
* [x] Evaluate CNN Model
* [x] Implement PaddleOCR
* [x] Implement EasyOCR
* [x] Implement Tesseract OCR
* [x] Create OCR Parsing System
* [x] Benchmark OCR Models
* [x] Evaluate OCR using CER and WER
* [x] Create Structured Transaction Dataset
* [x] Integrate CNN and OCR Pipeline
* [x] Create FastAPI Server
* [x] Prepare Docker Deployment
* [x] Improve OCR Parsing Accuracy
* [x] Optimize AI Inference Performance
* [x] Deploy Production AI Model

---

## Installation

### Run on Local Environment

This project uses Python v3.11 and virtual environment (venv).

---

### 1. Clone Repository

```bash
git clone https://github.com/your-organization/nopi-ai-models.git

cd nopi-ai-api
```

---

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

---

### 3. Activate Virtual Environment

Windows

```powershell
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Train CNN Model

Open notebook:

```bash
notebooks/CNN_Model_ReceiptClassification.ipynb
```

This notebook is used to:

* preprocess dataset
* train CNN model
* evaluate model
* save TensorBoard logs

---

### 6. Setup OCR Environment

Open notebook:

```bash
notebooks/setup_ocr.ipynb
```

---

### 7. Run OCR Benchmarking

```bash
python benchmark.py
```

Used to compare parsing quality of:

* PaddleOCR
* EasyOCR
* Tesseract OCR

---

### 8. Generate Structured Dataset from primary receipt images.

```bash
python generate_dataset.py
```

Generates structured CSV transaction datasets from receipt images.

---

### 9. Calculate Parsing Accuracy

```bash
python hitung_akurasi.py
```

Used to evaluate parsing accuracy such as:

* quantity extraction
* total price extraction

---

### 10. Run AI Inference Pipeline

```bash
python inference_notebook.py
```

Combines:

* CNN receipt classifier
* PaddleOCR extraction
* receipt parser

into one AI pipeline.

---

## Workflow

1. User uploads image
2. CNN model validates receipt image
3. PaddleOCR extracts receipt text
4. Parser converts OCR text into structured transaction data
5. Transaction data stored and processed by frontend/backend

---

## Author
* CACC009D6X0878 - Nadya Putri Nur Aletta - Gunadarma University 
* CACC009D6X2186 - Fatiyah Hanna Lathifah - Gunadarma University

---

## Thank You

---

[back to top](#nopi-ai-api)
