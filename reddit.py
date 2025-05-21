import praw
import pandas as pd
import os

# Reddit API Bağlantısı
reddit = praw.Reddit(
    client_id='3Kf0PQIJ9gCntLJC_JWqGg',
    client_secret='wnPik67csb1178Im_YPebNXgMj4uQQ',
    user_agent='name'
)

# Veri kümesi oluşturma
veri = []

# Daha fazla subreddit ve etiketi eşleştiriyoruz
subreddit_etiket = {
    # Spor
  



}

os.makedirs("reddit_verileri", exist_ok=True)
def temizle(text):
    if text:
        return text.replace('\n', ' ').replace('\r', ' ').strip()
    return ""

# Her subreddit için ayrı CSV dosyası
for subreddit_adi, etiket in subreddit_etiket.items():
    veri = []
    subreddit = reddit.subreddit(subreddit_adi)

    dosya_yolu = f"reddit_verileri/{"subreddit_adi"}.csv"

    # Eski dosya varsa yükle
    try:
        df_eski = pd.read_csv(dosya_yolu)
        eski_idler = df_eski['post_id'].tolist()
    except FileNotFoundError:
        df_eski = pd.DataFrame(columns=['metin', 'etiket', 'post_id'])
        eski_idler = []

    zaman_dilimleri = ['hour', 'day', 'week', 'month', 'year', 'all']
    for zaman in zaman_dilimleri:
        try:
            for post in subreddit.top(time_filter=zaman, limit=1000):
                post_id = post.id
                if post_id not in eski_idler:
                    metin = temizle(post.title) + " " + temizle(post.selftext)
                    veri.append({"metin": metin, "etiket": etiket, "post_id": post_id})
                    eski_idler.append(post_id)
        except Exception as e:
            print(f"Hata oluştu: {subreddit_adi} / {zaman} → {e}")

    # Yeni veriyi dataframe'e çevir
    df_yeni = pd.DataFrame(veri)

    # Eski ve yeni verileri birleştir
    df_toplam = pd.concat([df_eski, df_yeni], ignore_index=True)

    # CSV olarak kaydet
    df_toplam.to_csv(dosya_yolu, index=False, encoding='utf-8')
    print(f"{subreddit_adi} subreddit'i için veriler kaydedildi!")
    