# app/scraper.py

import requests
from bs4 import BeautifulSoup
from app.models import SessionLocal, Document
from datetime import datetime
import threading
import time

def fetch_news_articles():
    """
    Fetch news articles from a predefined news website and store them in the database.
    """
    url = "https://example-news-website.com"  # Replace with actual news website
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')  # Adjust selector as per website structure

        db = SessionLocal()
        for article in articles:
            title = article.find('h2').get_text()
            content = article.find('p').get_text()
            article_url = article.find('a')['href']
            
            # Check if the article already exists
            existing_doc = db.query(Document).filter(Document.url == article_url).first()
            if not existing_doc:
                new_doc = Document(
                    title=title,
                    content=content,
                    url=article_url,
                    created_at=datetime.now()
                )
                db.add(new_doc)
                db.commit()

        db.close()

def start_scraper(interval: int):
    """
    Start the scraper in a background thread to fetch news articles periodically.
    
    Args:
        interval (int): Time interval in seconds for scraping.
    """
    while True:
        fetch_news_articles()
        time.sleep(interval)

# Start scraper in a background thread
scraper_thread = threading.Thread(target=start_scraper, args=(3600,), daemon=True)  # Run every hour
scraper_thread.start()
