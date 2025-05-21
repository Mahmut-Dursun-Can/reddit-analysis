import os
import csv

klasor = r"C:\Users\cmahm\labeling\reddit_verileri"

for dosya in os.listdir(klasor):
    if dosya.endswith(".csv"):
        yol = os.path.join(klasor, dosya)
        temiz_yol = os.path.join(klasor, dosya.replace(".csv", "_clean.csv"))
        with open(yol, encoding="utf-8") as f_in, open(temiz_yol, "w", encoding="utf-8", newline="") as f_out:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)
            try:
                header = next(reader)
            except Exception as e:
                print(f"{dosya} başlık okunamıyor: {e}")
                continue
            writer.writerow(header)
            sutun_sayisi = len(header)
            for i, row in enumerate(reader, start=2):
                if len(row) == sutun_sayisi:
                    writer.writerow(row)
                else:
                    print(f"{dosya} dosyasında {i}. satır hatalı, silindi: {row}")