# --------------------------------------------------
# Membandingkan hasil benchmark dengan Ground Truth
# --------------------------------------------------

import pandas as pd
import json
import os

def clean_price(price_str):
    """Fungsi untuk membersihkan format Rp 100.000 menjadi angka 100000"""
    if pd.isna(price_str): return 0
    price_str = str(price_str).upper().replace("RP", "").replace(".", "").replace(",", "").replace(" ", "")
    try:
        return int(price_str)
    except:
        return 0

def calculate_accuracy(parsed_val, gt_val):
    """Menghitung persentase akurasi (0-100%)"""
    if gt_val == 0:
        return 100.0 if parsed_val == 0 else 0.0
    error = abs(parsed_val - gt_val) / gt_val
    acc = max(0, 100 - (error * 100))
    return acc

def run_evaluasi():
    print("Membaca file hasil komparasi dan ground truth...")
    
    # 1. Load Data
    try:
        df_hasil = pd.read_csv("hasil_komparasi_ocr_final.csv")
        df_gt = pd.read_csv("ground_truth.csv")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Pastikan file 'hasil_komparasi_ocr_final.csv' dan 'ground_truth.csv' ada di folder ini!")
        return

    # Bersihkan Data Ground Truth
    df_gt['Total Belanja (Asli)'] = df_gt['Total Belanja (Asli)'].apply(clean_price)
    df_gt = df_gt.drop_duplicates(subset=['Nama File']).set_index('Nama File')

    # Samakan format nama file (misal: "dataset_struk\primer_001.jpg" jadi "primer_001.jpg")
    df_hasil['Nama File'] = df_hasil['File'].apply(lambda x: os.path.basename(str(x).replace('\\', '/')))

    # 2. Siapkan wadah penyimpanan metrik
    metrics = {
        "Paddle": {"waktu": [], "success": 0, "acc_qty": [], "acc_price": []},
        "Tesseract": {"waktu": [], "success": 0, "acc_qty": [], "acc_price": []},
        "EasyOCR": {"waktu": [], "success": 0, "acc_qty": [], "acc_price": []}
    }
    
    # Wadah untuk SEMUA model
    detail_semua_model = []

    # 3. Mulai Perhitungan
    total_files_valid = 0

    for idx, row in df_hasil.iterrows():
        nama_file = row['Nama File']
        if nama_file not in df_gt.index:
            continue
            
        total_files_valid += 1
        gt_qty = df_gt.loc[nama_file, 'Jumlah Item (Asli)']
        gt_price = df_gt.loc[nama_file, 'Total Belanja (Asli)']
        
        for model in ["Paddle", "Tesseract", "EasyOCR"]:
            col_json = f"Hasil_{model}"
            col_waktu = f"Waktu_{model}"
            
            waktu = row.get(col_waktu, 0)
            metrics[model]["waktu"].append(waktu)
            
            parsed_qty = 0
            parsed_price = 0
            is_success = False
            
            try:
                data_json = json.loads(row[col_json])
                if len(data_json.get("items", [])) > 0:
                    is_success = True
                    metrics[model]["success"] += 1
                    
                    for item in data_json["items"]:
                        parsed_qty += int(item.get("jumlah_barang", 0))
                        parsed_price += int(item.get("total_harga_item", 0))
            except:
                pass
            
            acc_q = calculate_accuracy(parsed_qty, gt_qty)
            acc_p = calculate_accuracy(parsed_price, gt_price)
            
            metrics[model]["acc_qty"].append(acc_q)
            metrics[model]["acc_price"].append(acc_p)
            
            # --- EVALUASI UNTUK KETIGA MODEL ---
            if acc_q == 100 and acc_p == 100:
                status = "Sempurna (100%)"
            elif is_success:
                status = "Sebagian (Terekstrak tapi ada miss)"
            else:
                status = "Gagal Total (0%)"
                
            detail_semua_model.append({
                "Nama File": nama_file,
                "Model": model,                 # Tambahan kolom model biar gampang di-filter DS
                "Item Asli (GT)": gt_qty,
                "Item Terbaca": parsed_qty,
                "Total Harga Asli (GT)": gt_price,
                "Total Harga Terbaca": parsed_price,
                "Akurasi Item (%)": round(acc_q, 2),
                "Akurasi Harga (%)": round(acc_p, 2),
                "Status": status
            })

    # 4. Rekap Keseluruhan (Untuk CSV 1)
    summary = []
    
    for model, m in metrics.items():
        avg_waktu = sum(m["waktu"]) / len(m["waktu"]) if m["waktu"] else 0
        success_rate = (m["success"] / total_files_valid) * 100 if total_files_valid else 0
        avg_acc_qty = sum(m["acc_qty"]) / len(m["acc_qty"]) if m["acc_qty"] else 0
        avg_acc_price = sum(m["acc_price"]) / len(m["acc_price"]) if m["acc_price"] else 0
        
        summary.append({
            "Nama Model": model,
            "Rata-rata Waktu (Detik)": round(avg_waktu, 2),
            "Success Rate (%)": round(success_rate, 2),
            "Akurasi Jumlah Item (%)": round(avg_acc_qty, 2),
            "Akurasi Total Harga (%)": round(avg_acc_price, 2)
        })

    # 5. Export ke CSV
    df_summary = pd.DataFrame(summary)
    df_summary.to_csv("evaluasi_3_model.csv", index=False)
    
    df_detail = pd.DataFrame(detail_semua_model)
    df_detail.to_csv("detail_akurasi_semua_model.csv", index=False) 

    print("\n✅ SELESAI! 2 File CSV telah berhasil dibuat:\n")
    print("📁 1. evaluasi_3_model.csv --> (Kasih ke DS untuk bikin Bar Chart Komparasi)")
    print("📁 2. detail_akurasi_semua_model.csv --> (Kasih ke DS untuk bikin Pie Chart Detail)")
    print("\n📊 PREVIEW HASIL KOMPARASI:")
    print(df_summary.to_string(index=False))

if __name__ == "__main__":
    run_evaluasi()