
"""
Chris Foltz

This program scrapes a url provided by the user and saves the headlines (after string conversion) into a text file.

"""

import requests
from bs4 import BeautifulSoup

def scrape_news():
    url_input = input("Please enter a website (e.g., cnn.com or bbc.com): ")
    # Ensure the URL is properly formatted
    if not url_input.startswith("http"):
        url = "https://" + url_input
    else:
        url = url_input

    # Headers make the request look like it's coming from a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        headingCount = 0

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # BROAD SEARCH: Look for common headline tags instead of a specific class
            headlines = soup.find_all(['h1', 'h2', 'h3', 'h4'])

            news_list = []
            for headline in headlines:
                text = headline.get_text().strip()
                
                # Filter out empty or very short strings (like "Menu" or "Search")
                if len(text) > 15:
                    # Find the nearest link associated with this headline
                    link_tag = headline.find('a') or headline.find_parent('a')
                    link = link_tag['href'] if link_tag else "No link found"
                    
                    # Fix relative links (e.g., /story -> https://site.com/story)
                    if link.startswith('/'):
                        link = url.rstrip('/') + link

                    news_item = {
                        "headline": text,
                        "link": link,
                    }
                    news_list.append(news_item)
                    headingCount += 1
            
            return news_list, headingCount, url
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None, 0, url
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, 0, url

if __name__ == "__main__":
    file_path = "NewsLog.txt"
    
    news, headingCount, url = scrape_news()
    if news:
        for item in news:
            print(f"Headline: {item['headline']}")
            print(f"Link: {item['link']}")
            print("-" * 50)
        print(f"Total number of headings scraped from {url} are: {headingCount}")
    else:
        print("Could not retrieve news from", url)
    with open(file_path, "w") as file:

        file.write(str(news))
