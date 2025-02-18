import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Start WebDriver (without specifying driver path)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open IMDb Top 250 page
url = "https://www.imdb.com/chart/top/"
driver.get(url)

# Get the page source
soup = BeautifulSoup(driver.page_source, "html.parser")

# Close the browser completely
driver.quit()

# Initialize the movie list
movie_list = []

# Find all movie elements on the page
movies = soup.find_all('li', class_="ipc-metadata-list-summary-item")

# Extract movie details
for movie in movies:
    # Get the movie title
    title_tag = movie.find('h3', class_='ipc-title__text')
    title = title_tag.text.strip()

    # Get metadata (release year, duration)
    metadata = movie.find_all('span', class_="cli-title-metadata-item")
    year = metadata[0].text.strip() if len(metadata) > 0 else "N/A"
    duration = metadata[1].text.strip() if len(metadata) > 1 else "N/A"

    # Get the IMDb rating
    rating_tag = movie.find('span', class_="ipc-rating-star--imdb")
    rating = rating_tag.text.strip() if rating_tag else "N/A"

    # Append movie details to the list
    movie_list.append([title, year, duration, rating])

# Convert movie list to a DataFrame and save it as an Excel file
df = pd.DataFrame(movie_list, columns=["Movie Name", "Release Date", "Duration", "Rating"])
df.to_excel("imdb_ratings.xlsx", index=False)

print("IMDb List Created and Browser Closed!")
