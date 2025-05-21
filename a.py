import os
import csv

klasor = r"C:\Users\cmahm\labeling\reddit_verileri"  # Klasör yolunu güncelle

for dosya in os.listdir(klasor):
    if dosya.endswith("_clean.csv"):
        yol = os.path.join(klasor, dosya)
        with open(yol, encoding="utf-8") as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except Exception as e:
                print(f"{dosya} dosyasının başlığı okunamıyor: {e}")
                continue
            expected_cols = len(header)
            for i, row in enumerate(reader, start=2):  # Başlık 1. satır, veri 2. satırdan başlar
                if len(row) != expected_cols:
                    print(f"HATA: {dosya} dosyası, {i}. satır: {row} (Beklenen sütun: {expected_cols}, Bulunan: {len(row)})")