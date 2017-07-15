import requests

from bs4 import BeautifulSoup


def parse_html(html, **kwargs):
    parsed_html = BeautifulSoup(html, 'lxml')

    headline = parsed_html.body.find('h1')
    paragraph = None

    # Parse Paragraph
    content_container = parsed_html.body.find(
        'div',
        attrs={'id': 'bodyContent'}
    )
    for p in content_container.findAll('p'):
        if not p.findParents('table'):
            paragraph = p
            break

    # Parse Image
    infobox = parsed_html.body.find('table', attrs={'class': 'infobox'})
    image = infobox.find('img') if infobox else None

    return {
        'headline': headline.text.strip() if headline else '',
        'paragraph': paragraph.text.strip() if paragraph else '',
        'image_url': image.attrs.get('src') if image else '',
    }


def crawl(url, **kwargs):
    response = requests.get(url)
    response.raise_for_status()
    data = parse_html(response.content, **kwargs)

    # TODOs: Persist data

    return data
