import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from flask import Flask, request, render_template_string

app = Flask(__name__)
klasor = r"C:\Users\cmahm\labeling\reddit_verileri"  # Dosya yolu

tum_veriler = []

for dosya in os.listdir(klasor):
    if dosya.endswith("_clean.csv") and not dosya.endswith("duygu.csv"):
        yol = os.path.join(klasor, dosya)
        df = pd.read_csv(yol)
        tum_veriler.append(df)

df_tum = pd.concat(tum_veriler, ignore_index=True)

# TF-IDF ve model eğitimi
vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
X = vectorizer.fit_transform(df_tum['metin'].astype(str))
y = df_tum['etiket']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = MultinomialNB()
model.fit(X_train, y_train)

# Sınıflandırma raporu
y_pred = model.predict(X_test)
print("=== Sınıflandırma Raporu ===")
print(classification_report(y_test, y_pred))

# Flask arayüzü
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8" />
    <title>Etiket Tahmini</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f4f7fa;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 50px 20px;
            min-height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            max-width: 700px;
            width: 100%;
        }
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 25px;
        }
        textarea {
            width: 100%;
            border: 2px solid #ccc;
            border-radius: 8px;
            padding: 15px;
            font-size: 16px;
            resize: vertical;
            font-family: inherit;
            transition: border-color 0.3s ease;
            color: #333;
        }
        textarea::placeholder {
            color: #999;
            font-style: italic;
        }
        textarea:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 5px #007bff;
        }
        button {
            display: block;
            width: 100%;
            background-color: #007bff;
            color: white;
            border: none;
            padding: 14px 0;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 20px;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 30px;
            background: #e9f2ff;
            border-left: 6px solid #007bff;
            padding: 20px 25px;
            border-radius: 8px;
            color: #222;
            font-size: 17px;
            line-height: 1.4;
            white-space: pre-wrap;
        }
        .result b {
            color: #007bff;
        }
        @media (max-width: 480px) {
            .container {
                padding: 20px;
            }
            textarea {
                font-size: 14px;
            }
            button {
                font-size: 16px;
                padding: 12px 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Metin Girin ve Etiket Tahmini Alın</h2>
        <form method="POST">
            <textarea name="metin" rows="6" placeholder="Metni buraya yazın..." required>{{ girilen_metin|default('') }}</textarea>
            <button type="submit">Tahmin Et</button>
        </form>
        {% if tahmin %}
            <div class="result">
                <p><b>Metin:</b><br> {{ girilen_metin }}</p>
                <p><b>Tahmin Edilen Etiket(ler):</b><br> {{ tahmin }}</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    tahmin = None
    girilen_metin = None

    if request.method == "POST":
        girilen_metin = request.form["metin"]
        yeni_vec = vectorizer.transform([girilen_metin])
        olasiliklar = model.predict_proba(yeni_vec)[0]
        siniflar = model.classes_

        en_iyi_idx = olasiliklar.argsort()[::-1][:3]
        tahminler = [f"{siniflar[idx]} (olasılık: {olasiliklar[idx]:.2f})" for idx in en_iyi_idx]
        tahmin = ", ".join(tahminler)

    return render_template_string(HTML_TEMPLATE, tahmin=tahmin, girilen_metin=girilen_metin)

if __name__ == "__main__":
    app.run(debug=True)