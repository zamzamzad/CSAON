# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# List of RSS feed URLs to fetch data from
rss_urls = [
        'https://www.omandaily.om/rssFeed/0',
        # 'https://www.omandaily.om/rssFeed/25',
        # 'https://www.omandaily.om/rssFeed/38',
        # 'https://www.omandaily.om/rssFeed/39',
        # 'https://www.omandaily.om/rssFeed/40',
        # 'https://www.omandaily.om/rssFeed/41',
        # 'https://www.omandaily.om/rssFeed/42',
        # 'https://www.omandaily.om/rssFeed/43',
        # 'https://www.omandaily.om/rssFeed/44',
        # 'https://www.omandaily.om/rssFeed/46',
        # 'https://www.omandaily.om/rssFeed/47',
        # 'https://www.omandaily.om/rssFeed/48',
        # 'https://www.omandaily.om/rssFeed/50',
        # 'https://www.omandaily.om/rssFeed/51',
        # 'https://www.omandaily.om/rssFeed/52',
        # 'https://www.omandaily.om/rssFeed/53',
        # 'https://www.omandaily.om/rssFeed/63',
        # 'https://www.omandaily.om/rssFeed/72',
        # 'https://www.omandaily.om/rssFeed/78',
        # 'https://www.omandaily.om/rssFeed/91',
        # 'https://www.omandaily.om/rssFeed/97',
        # 'https://www.omandaily.om/rssFeed/100',
        # 'https://www.omandaily.om/rssFeed/103',
    # Add other RSS URLs here if needed...
]

# Function to fetch and parse RSS feed
def fetch_rss_feed(rss_url):
    # Send a GET request to the RSS feed URL
    response = requests.get(rss_url)
    
    # Parse the RSS feed content using BeautifulSoup with 'xml' parser
    soup = BeautifulSoup(response.content, features='xml')
    
    # Find all 'item' elements in the RSS feed, each representing an article
    articles = soup.findAll('item')
    
    return articles

# Function to preprocess and clean up text
def preprocess_text(text):
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', text)
    
    # Replace non-word characters (excluding spaces) with a space
    text = re.sub(r'\W', ' ', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    return text

# List to store article data
data = []

# Loop through each RSS feed URL
for rss_url in rss_urls:
    # Fetch and parse articles from the current RSS feed URL
    articles = fetch_rss_feed(rss_url)
    
    # Loop through each article in the RSS feed
    for article in articles:
        # Extract the title of the article
        title = article.title.text
        
        # Extract and preprocess the description of the article
        description = preprocess_text(article.description.text)
        
        # Extract the thumbnail image URL, if available
        thumbnail = article.find('media:thumbnail')
        thumbnail_url = thumbnail['url'] if thumbnail else ''
        
        # Extract the link to the article
        link = article.link.text
        
        # Append the article data to the list
        data.append({
            'title': title,
            'description': description,
            'thumbnail': thumbnail_url,
            'article_link': link
        })

# Create a DataFrame from the list of article data
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('preprocessed_articles.csv', index=False)

# Print a message indicating completion of data collection
print("Data collection complete and saved to 'preprocessed_articles.csv'.")
