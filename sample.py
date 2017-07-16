import webcrawler

MOST_READ_ARTICLES = [
    "https://en.wikipedia.org/wiki/Spider-Man:_Homecoming",
    "https://en.wikipedia.org/wiki/Independence_Day_(United_States)",
    "https://en.wikipedia.org/wiki/Omar_Khadr",
    "https://en.wikipedia.org/wiki/G20",
    "https://en.wikipedia.org/wiki/Deaths_in_2017",
    "https://en.wikipedia.org/wiki/Wonder_Woman_(2017_film)",
    "https://en.wikipedia.org/wiki/Hustler",
    "https://en.wikipedia.org/wiki/Transformers:_The_Last_Knight",
    "https://en.wikipedia.org/wiki/Goods_and_Services_Tax_(India)",
    "https://en.wikipedia.org/wiki/Israel"
]


def crawl_most_read_articles():
    for article in MOST_READ_ARTICLES:
        webcrawler.crawl(article)
