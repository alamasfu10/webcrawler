import json
import os
import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from slugify import slugify


def parse_html(
    html,
    is_wikipedia_page=False,
    content_container_class='',
    image_container_class='',
):
    """Parse the given HTML to retrieve relevant content.

    It is intended to retrieve data from Wikipedia articles without additional
    configuration or kwargs.
    To retrieve the data from generic pages, the content and image container
    classes are required.

    Args:
    url (str): URL of the page whose data is going to be retrieved
    is_wikipedia_page (bool): True if wikipedia HTML, False if not.
    content_container_class (str): CSS Class of the HTML content container
        element. Required to retrieve relevant data of generic pages.
    image_container_class (str): CSS Class of the HTML image container element.
        Required to retrieve relevant data of generic pages.
    """

    parsed_html = BeautifulSoup(html, 'html.parser')

    headline = parsed_html.body.find('h1')
    paragraph = None

    if is_wikipedia_page:
        content_container = parsed_html.body.find(
            'div',
            attrs={'id': 'bodyContent'}
        )

        # Wikipedia Articles have the first relevat paragraph
        # after the markup for the table on the right.
        # This table can also contain <p> tags, which are not
        # the desired first paragraph.
        for p in content_container.findAll('p'):
            if not p.findParents('table'):
                paragraph = p
                break

        infobox = parsed_html.body.find('table', attrs={'class': 'infobox'})
        image = infobox.find('img') if infobox else None
    else:
        if not all([
            content_container_class,
            image_container_class
        ]):
            return

        content_container = parsed_html.body.find(
            'div',
            attrs={'class': content_container_class}
        )
        paragraph = content_container.find('p')

        image_container = parsed_html.body.find(
            'div',
            attrs={'class': image_container_class}
        )
        image = image_container.find('img')

    return {
        'headline': headline.text.strip() if headline else '',
        'paragraph': paragraph.text.strip() if paragraph else '',
        'image_url': image.attrs.get('src') if image else '',
    }


def crawl(
    url,
    content_container_class='',
    image_container_class=''
):
    """Crawl a URL, retrieve and persist the relevant data and return it.

    It is intended to retrieve data from Wikipedia articles without additional
    configuration or kwargs.
    To retrieve the data from generic pages, the content and image container
    classes are required.

    Args:
    url (str): URL of the page whose data is going to be retrieved
    content_container_class (str): CSS Class of the HTML content container
        element. Required to retrieve relevant data of generic pages.
    image_container_class (str): CSS Class of the HTML image container element.
        Required to retrieve relevant data of generic pages.
    """

    response = requests.get(url)
    response.raise_for_status()
    is_wikipedia_page = re.compile(r'.*(wikipedia.org)').match(url) is not None

    data = parse_html(
        response.content,
        is_wikipedia_page=is_wikipedia_page,
        content_container_class=content_container_class,
        image_container_class=image_container_class
    )

    if not data:
        return

    if not os.path.exists('data'):
        os.makedirs('data')

    filename = '{}-{}.json'.format(
        datetime.now().strftime('%Y-%m-%d-%H:%M'),
        slugify(data.get('headline'))
    )

    with open('data/{}'.format(filename), 'w') as file:
        json.dump(data, file)
        file.close()

    return data
