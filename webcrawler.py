import json
import os
import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from slugify import slugify


def parse_html(html, **kwargs):
    is_wikipedia_page = kwargs.get('is_wikipedia_page')
    parsed_html = BeautifulSoup(html, 'html.parser')

    headline = parsed_html.body.find('h1')
    paragraph = None

    if is_wikipedia_page:
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
    else:
        content_container_class = kwargs.get('content_container_class')
        image_container_class = kwargs.get('image_container_class')

        if not all([
            content_container_class,
            image_container_class
        ]):
            return

        content_container = parsed_html.body.find('div', attrs={'class': content_container_class})
        paragraph = content_container.find('p')

        image_container = parsed_html.body.find('div', attrs={'class': image_container_class})
        image = image_container.find('img')

    return {
        'headline': headline.text.strip() if headline else '',
        'paragraph': paragraph.text.strip() if paragraph else '',
        'image_url': image.attrs.get('src') if image else '',
    }


def crawl(url, **kwargs):
    response = requests.get(url)
    response.raise_for_status()
    is_wikipedia_page = re.compile(r'.*(wikipedia.org)').match(url) is not None

    if is_wikipedia_page:
        kwargs.update({
            'is_wikipedia_page': is_wikipedia_page
        })

    data = parse_html(response.content, **kwargs)

    if not data:
        return

    # Persist Data
    if not os.path.exists('data'):
        os.makedirs('data')

    filename = '{}-{}.json'.format(
        datetime.now().strftime('%Y-%m-%d-%H:%M'),
        slugify(data.get('headline'))
    )

    with open('data/{}'.format(filename), 'w') as file:  # noqa
        json.dump(data, file)
        file.close()

    return data
