# -------------------------------------------------------------------------------
# Random Sampling 20 dataset primer (hanya untuk pembuatan dataset di benchmark),
# tidak digunakan (tidak berpengaruh ke model)
# -------------------------------------------------------------------------------

# import os
# import random

# #Buat random sampling pilih data uji secara acak buat komparasi model
# def pilih_struk_random():
#     folder_path = "dataset_struk"
    
#     # Daftar 10 struk yang sudah masuk di Ground Truth saat ini
#     struk_lama = [
#         "primer_0067.jpg", "primer_0071.jpg", "primer_0081.jpg", 
#         "primer_0082.jpg", "primer_0096.jpg", "primer_0099.jpg", 
#         "primer_0108.jpg", "primer_0109.jpg", "primer_0111.jpg", 
#         "primer_0117.jpg"
#     ]
    
#     # Ambil semua gambar HANYA YANG BERAWALAN 'primer_' 
#     semua_file = [
#         f for f in os.listdir(folder_path) 
#         if f.lower().startswith('primer_') and f.lower().endswith(('.jpg', '.jpeg'))
#     ]
    
#     # Saring file, buang 10 struk yang sudah dipakai sebelumnya
#     sisa_file = [f for f in semua_file if f not in struk_lama]
    
#     # Pastikan file sisanya cukup
#     if len(sisa_file) < 20:
#         print(f"Waduh, sisa file primer di folder cuma ada {len(sisa_file)}, nggak nyampe 20!")
#         return
        
#     # Pilih 20 secara acak (random)
#     struk_baru = random.sample(sisa_file, 20)
#     struk_baru.sort() # Urutkan sesuai abjad biar rapi
    
#     print("✅ BERHASIL MEMILIH 20 STRUK PRIMER BARU SECARA ACAK!\n")
#     print("Silakan copy-paste daftar di bawah ini ke dalam list 'daftar_foto' di benchmark.py:\n")
    
#     for f in struk_baru:
#         # Nge-print dalam format path string biar gampang di-copy
#         print(f'        r"dataset_struk\\{f}",')

# if __name__ == "__main__":
#     pilih_struk_random()