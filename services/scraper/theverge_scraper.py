import requests
from bs4 import BeautifulSoup
from newspaper import Article

def scrape_techcrunch(limit=5):
    url = "https://techcrunch.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    seen_urls = set()

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith("https://techcrunch.com/") and href not in seen_urls:
            seen_urls.add(href)
            try:
                article = Article(href)
                article.download()
                article.parse()

                # Skip articles with empty or very short content
                if not article.text.strip() or len(article.text.strip()) < 100:
                    print(f"⚠️ Skipping short/empty content: {href}")
                    continue

                articles.append({
                    "title": article.title,
                    "url": href,
                    "content": article.text,
                    "source": "TechCrunch"
                })

                if len(articles) >= limit:
                    break
            except Exception as e:
                print(f"❌ Skipping {href} due to error: {e}")
                continue

    return articles