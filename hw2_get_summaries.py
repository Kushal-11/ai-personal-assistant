import httpx
import os
import asyncio
from bs4 import BeautifulSoup

import json

async def fetch_news():
    interest = "technology"
    news_api_key = os.getenv('NEWS_API_KEY')
    url = f"https://newsapi.org/v2/everything?q={interest}&apiKey={news_api_key}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        articles = response.json()['articles']

        for i, article in enumerate(articles):
            if i==15:
                break
            filename = f"news_summaries/summary_{i+1}.txt"
            with open(filename, "w", encoding='utf-8') as file:
                file.write(article['title'] + "\n\n")
                if article['description'] is not None:
                    file.write(article['description'])

        # since the summary is too short, i will use the beautifulsoup library to get the full article
                # Get the full text of the article
                article_url = article['url']
                article_response = await client.get(article_url, timeout=30.0)
                soup = BeautifulSoup(article_response.text, 'html.parser')
                paragraphs = soup.find_all('p')
                for paragraph in paragraphs:
                    file.write(paragraph.text)


# Call the async function
async def main():
    await fetch_news()

# Create an event loop and run the main function
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

