import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options  # Headless mode için eklendi

# Headless mode aktif et
chrome_options = Options()
chrome_options.add_argument("--headless")  # Tarayıcıyı görünmez yap
chrome_options.add_argument("--disable-gpu")  # Windows için gerekli olabilir
chrome_options.add_argument("--no-sandbox")  # Linux sistemler için
chrome_options.add_argument("--disable-dev-shm-usage")  # Docker için

# WebDriver'ı başlat (headless mode aktif)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# IMDb Top 250 sayfasını aç
url = "https://www.imdb.com/chart/top/"
driver.get(url)

# Sayfanın kaynağını al
soup = BeautifulSoup(driver.page_source, "html.parser")

driver.quit()  # Tarayıcıyı tamamen kapat

movie_list = []

movies = soup.find_all('li', class_="ipc-metadata-list-summary-item")

for movie in movies:
    title_tag = movie.find('h3', class_='ipc-title__text')
    title = title_tag.text.strip()
    metadata = movie.find_all('span', class_="cli-title-metadata-item")

    year = metadata[0].text.strip() if len(metadata) > 0 else "N/A"
    duration = metadata[1].text.strip() if len(metadata) > 1 else "N/A"

    rating_tag = movie.find('span', class_="ipc-rating-star--imdb")
    rating = rating_tag.text.strip() if rating_tag else "N/A"

    movie_list.append([title, year, duration, rating])

df = pd.DataFrame(movie_list, columns=["Movie Name", "Release Date", "Duration", "Rating"])
df.to_excel("imdb_ratings.xlsx", index=False)

print("IMDb List Created in Headless Mode!")
