import requests
from bs4 import BeautifulSoup
import time

# Base URL of the website to scrape
base_url = "調べたいWordPressサイトURL（ex. https://aaa.bb）"

# Function to get all article URLs from the website
def get_article_urls(base_url):
    article_urls = []
    page = 1
    while True:
        # Construct URL for each page of articles
        url = f"{base_url}/page/{page}/"
        response = requests.get(url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all links to articles
        links = soup.find_all('a', href=True)
        page_article_urls = [link['href'] for link in links if "/20" in link['href']]
        if not page_article_urls:
            break
        article_urls.extend(page_article_urls)
        page += 1
        time.sleep(1)  # To avoid overwhelming the server
    return list(set(article_urls))  # Remove duplicates

# Function to check if an article has an eye-catching image
def check_eye_catching_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        thumbnail_area = soup.find('div', class_='entry-thumbnail-area underimage')
        return thumbnail_area is None
    return False

# Get all article URLs
article_urls = get_article_urls(base_url)

# Count articles without an eye-catching image
no_image_count = 0
no_image_titles = []

for url in article_urls:
    full_url = url if url.startswith('http') else base_url + url
    if check_eye_catching_image(full_url):
        no_image_count += 1
        response = requests.get(full_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title').get_text(strip=True)
            no_image_titles.append(title)
        else:
            no_image_titles.append(full_url)

# Output the results
print(f"Number of articles without an eye-catching image: {no_image_count}")
print("Titles of articles without an eye-catching image:")
for title in no_image_titles:
    print(f"- {title}")
