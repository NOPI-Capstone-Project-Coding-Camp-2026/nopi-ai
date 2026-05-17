# ------------------------------------------------------------------------------
# Menjalankan PaddleOCR (sebagai model terbaik) ke seluruh 117 dataset primer, 
# untuk diubah menjadi format tabel mendatar yang rapi
# ------------------------------------------------------------------------------

import os
import json
import pandas as pd

# Import khusus model terbaik (PaddleOCR)
from paddle_ocr import extract_text_paddle
from paddle_parser import parse_paddleocr_text

def run_full_extraction_primer():
    folder_path = "dataset_struk"
    
    # 1. Cari HANYA file dataset primer
    semua_file = [
        f for f in os.listdir(folder_path) 
        if f.lower().startswith('primer_') and f.lower().endswith(('.jpg', '.jpeg'))
    ]
    semua_file.sort() # Urutkan agar rapi sesuai abjad
    
    if not semua_file:
        print("⚠️ Tidak menemukan gambar dataset primer di folder.")
        return

    print(f"\n🚀 Menemukan {len(semua_file)} gambar dataset PRIMER. Memulai ekstraksi...\n")
    
    flat_data = []

    # 2. Looping ke seluruh gambar primer
    for idx, nama_file in enumerate(semua_file):
        print(f"[{idx + 1}/{len(semua_file)}] Memproses: {nama_file}...")
        img_path = os.path.join(folder_path, nama_file)
        
        # Ekstrak menggunakan model terbaik (PaddleOCR)
        raw_text = extract_text_paddle(img_path)
        json_str = parse_paddleocr_text(raw_text)
        
        try:
            data = json.loads(json_str)
            toko = data.get("nama_toko", "")
            tanggal = data.get("tanggal", "")
            items = data.get("items", [])
            
            # Jika OCR gagal mengenali barang satu pun
            if len(items) == 0:
                flat_data.append({
                    "filename": nama_file,
                    "sumber": "primer",
                    "nama_toko": toko,
                    "tanggal": tanggal,
                    "nama_barang": None,
                    "jumlah_barang": None,
                    "harga_satuan": None,
                    "total_harga_item": None,
                    "raw_text": raw_text
                })
            else:
                # Jika OCR berhasil, pecah tiap item menjadi 1 baris
                for item in items:
                    flat_data.append({
                        "filename": nama_file,
                        "sumber": "primer",
                        "nama_toko": toko,
                        "tanggal": tanggal,
                        "nama_barang": item.get("nama_barang", ""),
                        "jumlah_barang": item.get("jumlah_barang", 0),
                        "harga_satuan": item.get("harga_satuan", 0),
                        "total_harga_item": item.get("total_harga_item", 0),
                        "raw_text": raw_text
                    })
        except Exception as e:
            print(f"❌ Error saat memproses {nama_file}: {e}")
            
    # 3. Ubah ke format Tabel (DataFrame Pandas)
    df = pd.DataFrame(flat_data)
    
    # Tambahkan kolom 'nomor' secara berurutan (mulai dari 1)
    df.insert(0, 'nomor', range(1, len(df) + 1))
    
    # 4. Susun ulang urutan kolom 
    kolom_urut = [
        "nomor", "filename", "sumber", 
        "nama_toko", "tanggal", "nama_barang", 
        "jumlah_barang", "harga_satuan", "total_harga_item", 
        "raw_text"
    ]
    df = df[kolom_urut]
    
    # 5. Simpan ke dalam CSV Final
    output_filename = "Dataset_Terstruktur_Primer_NOPI.csv"
    df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    
    print(f"\n🎉 SELESAI! File '{output_filename}' telah berhasil dibuat.")

if __name__ == "__main__":
    print("=== MULAI PROSES EKSTRAKSI DATASET FINAL DENGAN PADDLE OCR ===")
    run_full_extraction_primer()