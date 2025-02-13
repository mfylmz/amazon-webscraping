import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.amazon.ca/s?k=video+game+collectibles&crid=2T2LIDY1GU6K8&sprefix=video+game%2Caps%2C113&ref=nb_sb_ss_mvt-t11-ranker_7_10"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    title = soup.find("span", {"id": "productTitle"})
    title = title.get_text(strip=True) if title else "Bilinmeyen Ürün"

    # Fiyat (bazı ürünlerde farklı HTML yapı olabilir, bu yüzden birkaç seçenek deneyelim)
    price = soup.find("span", {"class": "a-price-whole"})
    price = price.get_text(strip=True) if price else "Fiyat Bulunamadı"

    # Veriyi DataFrame'e ekle
    df = pd.DataFrame([[title, price]], columns=["Ürün Adı", "Fiyat"])

    # Excel'e kaydet
    df.to_excel("amazon_urunleri.xlsx", index=False)

    print(f"Ürün: {title}, Fiyat: {price}")
    print("Excel dosyası kaydedildi: amazon_urunleri.xlsx")
else:
    print("Veri çekme başarısız! Amazon bot koruması olabilir.")