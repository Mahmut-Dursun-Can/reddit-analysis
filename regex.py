import re

# Girdi dosyası ve çıktı dosyası yolu
input_file = r"C:\Users\cmahm\labeling\reddit_verileri\space.csv"
output_file = r"C:\Users\cmahm\labeling\temp.csv"

with open(input_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
    for line in f_in:
        temiz_line = re.sub(r"http[s]?://\S+", "", line)
        f_out.write(temiz_line)

