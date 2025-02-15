import requests
from bs4 import BeautifulSoup
import pandas as pd
url = "https://www.imdb.com/chart/top/"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


request = requests.get(url, headers=headers)
soup = BeautifulSoup(request.text, "html.parser")

movie_list=[]

movies = soup.find_all('li', class_="ipc-metadata-list-summary-item")

for movie in movies:
    title_tag=movie.find('h3', class_='ipc-title__text')
    title = title_tag.text.strip()
    metadata = movie.find_all('span', class_="cli-title-metadata-item")
    year = metadata[0].text.strip()
    duration = metadata[1].text.strip()
    
    rating_tag = movie.find('span', class_="ipc-rating-star--imdb")
    rating = rating_tag.text.strip()
    
    movie_list.append([title, year, duration, rating])



    
df= pd.DataFrame(movie_list, columns=["Movie Name", "Release Date", "Duration", "Rating"])
df.to_excel("imdb_ratings.xlsx", index=False)

print("Imdb List Created")