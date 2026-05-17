# ------------------------------------------------------------------------------
# Parsing easy ocr (tidak digunakan saat ini (karna sudah menggunakan paddle ocr), 
# tapi digunakan saat tahapan komparasi 3 model OCR)
# ------------------------------------------------------------------------------

import re
import json
from collections import defaultdict

class ReceiptParser:
    def __init__(self):
        # Memperluas blacklist kata kunci sampah
        self.garbage_keywords = [
            "TOTAL", "SUBTOTAL", "SUB TOTAL", "KEMBALI", "TUNAI", "CASH", "CHANGE", 
            "NON TUNAI", "DEBIT", "QRIS", "BANK", "TERIMA KASIH", "TERIMAKASIH", 
            "PELANGGAN", "CUSTOMER", "ALAMAT", "ADDRESS", "TELP", "FAKTUR", "NPWP", 
            "NO. NOTA", "DISCREPANCY", "AMOUNT PAID", "PAYMENT TYPE", "PRINT TIME", 
            "LAYANAN KONSUMEN", "WIRANIAGA", "DRIVER", "HELPER", "TANGGAL", "DATE",
            "NOMOR", "ORDER", "SHIPMENT", "SALES", "BATCH", "MOBIL", "POLISI", "SOPIR",
            "PINDAHAN DARI", "END OF DOCUMENT", "SEDEKAH", "DONASI", "MEMBER", "KRITIK",
            "KASIR", "BAYAR", "KEMBALIAN", "DUE", "BAL", "MERDEKA", "SURAT JALAN",
            "TAXABLE", "TAX", "JAX", "TUAI", "IOTAL", "SUBT0TAL", "DITERIMA", "PENGIRIM", 
            "KODE NAMA", "ITEM", "ITEMS", "KOLI", "HARGA DISKON", "KECAMATAN", "KABUPATEN"
        ]
        self.discount_keywords = ["DISC", "DISKON", "POTONGAN", "PROMO DISCOUNT", "TRADE PROMO", "CUTTING", "VOID", "OISIDE"]

    def clean_text_basic(self, text):
        # Membersihkan simbol karakter aneh hasil degradasi OCR thermal
        text = re.sub(r"[~`|_\[\]\{\}\(\)\"\'\u2713>>«»\-#\*]", "", text)
        return text.strip()

    def merge_split_amounts(self, row_tokens):
        merged_tokens = []
        i = 0
        while i < len(row_tokens):
            current_token = row_tokens[i]
            current_text = self.clean_text_basic(current_token["text"])
            
            if current_text.isdigit() and len(current_text) <= 4 and i + 1 < len(row_tokens):
                next_text = self.clean_text_basic(row_tokens[i+1]["text"])
                if next_text == "000" or (next_text.isdigit() and len(next_text) == 3):
                    combined_text = current_text + next_text
                    current_token["text"] = combined_text
                    merged_tokens.append(current_token)
                    i += 2
                    continue
            merged_tokens.append(current_token)
            i += 1
        return merged_tokens

    def group_into_lines(self, ocr_results):
        grouped = defaultdict(list)
        for r in ocr_results:
            if "text" not in r or not r["text"].strip():
                continue
            bbox = r["bbox"]
            center_y = (bbox[0][1] + bbox[2][1]) / 2
            
            matched_key = None
            for key in grouped.keys():
                if abs(key - center_y) < 15: # Diketatkan ke 15 agar tidak salah menyerap baris alamat bawah
                    matched_key = key
                    break
            
            if matched_key is None:
                matched_key = center_y
            grouped[matched_key].append(r)
            
        lines = []
        for key in sorted(grouped.keys()):
            row = sorted(grouped[key], key=lambda x: x["bbox"][0][0])
            row = self.merge_split_amounts(row)
            lines.append(row)
        return lines

    def extract_store_name(self, lines):
        candidates = []
        for i, row in enumerate(lines[:8]):
            row_text = " ".join([r["text"] for r in row]).strip()
            row_upper = row_text.upper()
            
            if len(row_text) < 5 or any(kw in row_upper for kw in ["TANGGAL", "DATE", "NO.", "FAKTUR", "NPWP", "JL.", "ALAMAT", "TELP", "KECAMATAN"]):
                continue
            
            score = 10 - i  
            if any(kw in row_upper for kw in ["TOKO", "MART", "CAFE", "RESTAURANT", "SWALAYAN", "JAYA", "INDOMARET", "ALFAMART", "LAWSON", "SUKATANI"]):
                score += 20
            if any(kw in row_upper for kw in ["PT.", "CV.", "BALINA", "FASTRATA", "DISTRIBUSINDO"]):
                score += 15
                
            candidates.append((score, row_text))
            
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            # Pastikan nama toko tidak berisi teks acak rusak
            final_name = self.clean_text_basic(candidates[0][1])
            if len([c for c in final_name if c.isalpha()]) > 3:
                return final_name
        return "NOT FOUND"

    def extract_date(self, text):
        patterns = [
            r"\b\d{2}[/\-\.\s]\d{2}[/\-\.\s]\d{4}\b", 
            r"\b\d{4}[/\-\.\s]\d{2}[/\-\.\s]\d{2}\b", 
            r"\b\d{2}[/\-\.\s]\d{2}[/\-\.\s]\d{2}\b"  
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                clean_date = match.group().replace(".", "-").replace(" ", "-")
                return clean_date
        return "NOT FOUND"

    def process_item_line(self, row_tokens):
        line_text = " ".join([t["text"] for t in row_tokens])
        line_upper = line_text.upper()
        
        # 1. VALIDASI KATA KUNCI SAMPAH SECARA KETAT
        if any(kw in line_upper for kw in self.garbage_keywords):
            return None
                
        if any(kw in line_upper for kw in self.discount_keywords):
            return None

        # Filter baris yang mengandung indikasi alamat (RT/RW/Kecamatan/No.Telp)
        if any(addr in line_upper for addr in ["JL.", "ALAMAT", "RT.", "RW.", "TELP", "FAX", "NPWP"]):
            return None

        # 2. EKSTRAKSI ANGKA HARGA VALID
        raw_numbers = []
        for t in row_tokens:
            t_clean = self.clean_text_basic(t["text"]).replace(".", "").replace(",", "")
            if t_clean.isdigit():
                raw_numbers.append(int(t_clean))

        if not raw_numbers:
            return None

        # Filter nominal tidak masuk akal yang biasanya merupakan bagian dari nomor jalan/RT
        valid_prices = [p for p in raw_numbers if 500 <= p <= 15000000]
        if not valid_prices:
            return None

        qty = 1
        unit_price = 0
        total_price = 0
        
        qty_x_match = re.search(r"\b(\d+)\s*[Xx]\s*", line_text)
        qty_unit_match = re.search(r"\b(\d+)\s*(?:PCS|BOX|BKS|BTL|PACK|BAG|GR|ML|PC|KARTON|ZAK)\b", line_upper)
        
        if qty_x_match:
            qty = int(qty_x_match.group(1))
        elif qty_unit_match:
            qty = int(qty_unit_match.group(1))
            
        if len(valid_prices) >= 2:
            total_price = valid_prices[-1]
            unit_price = valid_prices[-2]
            
            if not qty_x_match and not qty_unit_match:
                # Cek jika angka pertama baris adalah Qty kecil (misal di bawah 100)
                if raw_numbers[0] < 100 and raw_numbers[0] > 0:
                    qty = raw_numbers[0]
                elif unit_price > 0 and total_price % unit_price == 0:
                    calculated_qty = total_price // unit_price
                    if 1 < calculated_qty < 100:
                        qty = calculated_qty
        else:
            total_price = valid_prices[0]
            unit_price = total_price // qty if qty > 0 else total_price

        # Mengamankan jikalau posisi terbalik antara total dan harga satuan
        if total_price < unit_price and total_price > 0 and qty == 1:
            unit_price, total_price = total_price, unit_price

        # 3. PEMBERSIHAN NAMA BARANG DARI ELEMEN NUMERIK HARGA
        item_name_parts = []
        for t in row_tokens:
            t_clean = self.clean_text_basic(t["text"])
            t_upper = t_clean.upper()
            t_num = t_clean.replace(".", "").replace(",", "")
            
            if t_num.isdigit():
                val = int(t_num)
                # Skip angka jika merupakan representasi harga satuan, total, atau qty
                if val in [unit_price, total_price] or val == qty:
                    continue
            
            if t_upper in ["X", "PCS", "BOX", "BKS", "BTL", "RP", "PC", "PACK", "KARTON", "ZAK"]:
                continue
                
            item_name_parts.append(t["text"])

        item_name = " ".join(item_name_parts)
        
        # Regex pembersihan tahap akhir dari karakter sisa angka di ujung string
        item_name = re.sub(r"^\d{4,}\s*", "", item_name) # Buang kode barcode depan
        item_name = re.sub(r"^\d+\s*[Xx]\s*", "", item_name) # Buang angka pengali depan
        item_name = re.sub(r"\s+\d+[\.,\s]*\d*$", "", item_name) # Buang angka sisa belakang
        item_name = self.clean_text_basic(item_name)
        
        # 4. FILTER KETAT KELAYAKAN NAMA BARANG
        # Nama barang asli harus memiliki minimal 4 karakter huruf alfabet dominan
        letters_only = [c for c in item_name if c.isalpha()]
        if len(letters_only) < 4:
            return None
            
        # Cegah kebocoran jika teks nama barang hanya berisi kata-kata pendek tidak jelas (contoh: "b p Rp")
        if len(item_name.split()) == 1 and len(item_name) <= 3:
            return None

        return {
            "nama_barang": item_name,
            "jumlah_barang": qty,
            "harga_satuan": unit_price,
            "total_harga_item": total_price
        }

    def parse(self, raw_input):
        ocr_results = []
        if isinstance(raw_input, list):
            for item in raw_input:
                if isinstance(item, (list, tuple)) and len(item) == 3 and isinstance(item[1], str):
                    ocr_results.append({"bbox": item[0], "text": item[1]})
                elif isinstance(item, dict) and "bbox" in item and "text" in item:
                    ocr_results.append(item)
        else:
            return json.dumps({"error": "Format input harus berupa list data OCR"}, indent=4)

        lines = self.group_into_lines(ocr_results)
        
        all_text_lines = [" ".join([r["text"] for r in row]) for row in lines]
        full_text = "\n".join(all_text_lines)
        
        items = []
        for row in lines:
            item_data = self.process_item_line(row)
            if item_data:
                # ANTI-DUPLIKASI SUB-BARIS: Cek apakah nama barang sudah ada sebagian di list
                is_duplicate = False
                for existing_item in items:
                    if item_data["nama_barang"] in existing_item["nama_barang"] and item_data["total_harga_item"] == existing_item["total_harga_item"]:
                        is_duplicate = True
                        break
                if not is_duplicate:
                    items.append(item_data)

        # Saringan pembersih tahap akhir untuk Nama Toko agar tidak mengeluarkan teks sampah random
        store_name = self.extract_store_name(lines)
        if len([c for c in store_name if c.isalpha()]) < 3:
            store_name = "NOT FOUND"

        parsed = {
            "nama_toko": store_name,
            "tanggal": self.extract_date(full_text),
            "items": items
        }
        return json.dumps(parsed, indent=4)


def parse_easyocr_text(ocr_results):
    parser = ReceiptParser()
    return parser.parse(ocr_results)