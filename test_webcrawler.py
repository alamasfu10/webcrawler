# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import os
import requests
import webcrawler

from datetime import datetime
from slugify import slugify

MOCK_HTML = (
    '<html>'
        '<head>'
        '</head>'
        '<body>'
            '<h1>Plain Text</h1>'
            '<p>Irrelevant Paragraph</p>'
            '<img alt=\'Irrelevant Image\' src=\'http://media.istockphoto.com/photos/questions-signpost-in-german-picture-id519749280\'/>'  # noqa
            '<div class=\'content_container\'>'
                '<p>Lorem Ipsum</p>'
            '</div>'
            '<div class=\'image_container\'>'
                '<img src=\'http://media.istockphoto.com/photos/map-pin-flat-above-city-scape-and-network-connection-concept-picture-id612491256\'/>'  # noqa
            '</div>'
        '</body>'
    '</html>'
)


def test_parse_mock_html_without_container_classes():
    """For non-wikipedia pages, container classes need to be defined.
    It is not desired to persist irrelevant data.
    """
    data = webcrawler.parse_html(MOCK_HTML)

    assert data is None


def test_parse_mock_html_with_container_classes():
    data = webcrawler.parse_html(
        MOCK_HTML,
        content_container_class='content_container',
        image_container_class='image_container',
    )

    assert data is not None
    assert data.get('headline') == 'Plain Text'
    assert data.get('paragraph') == 'Lorem Ipsum'
    assert data.get('image_url') == 'http://media.istockphoto.com/photos/map-pin-flat-above-city-scape-and-network-connection-concept-picture-id612491256'  # noqa


def test_url_not_found():
    try:
        webcrawler.crawl('http://www.google.de/this-page-does-not-exist')
    except Exception as e:
        assert type(e) == requests.exceptions.HTTPError
        assert e.response.status_code == 404


def test_parse_wikipedia_page():
    data = webcrawler.crawl('https://en.wikipedia.org/wiki/Donald_Trump')

    assert data is not None
    assert data.get('headline') == 'Donald Trump'
    assert data.get('paragraph') == (
        'Donald John Trump (born June 14, 1946) is the 45th and current '
        'President of the United States, in office since January 20, 2017. '
        'Before entering politics, he was a businessman and television '
        'personality.'
    )
    assert data.get('image_url') == '//upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Donald_Trump_Pentagon_2017.jpg/220px-Donald_Trump_Pentagon_2017.jpg'  # noqa

    filename = '{}-{}.json'.format(
        datetime.now().strftime('%Y-%m-%d-%H:%M'),
        slugify(data.get('headline'))
    )
    os.remove('data/{}'.format(filename))


def test_parse_generic_page_without_container_classes():
    data = webcrawler.crawl(
        'https://as.com/motor/2017/07/15/formula_1/1500113537_936620.html',
    )

    assert data is None


def test_parse_generic_page_with_container_classes():
    data = webcrawler.crawl(
        'https://as.com/motor/2017/07/15/formula_1/1500113537_936620.html',
        content_container_class='int-articulo',
        image_container_class='cont-img-dest-art',
    )

    assert data is not None
    assert data.get('headline') == (
        'Hamilton y Vettel se citan para la pole con Alonso 11º y Sainz 17º'
    )
    assert data.get('paragraph') == (
        'Es esa lluvia fina, como esos trabajos en los que te vas dando '
        'golpes, uno y otro y otro… Y al final acabas saltando, dejando las '
        'llaves del coche de empresa, el pórtatil en la mesa, metiendo el '
        'marco con la foto de tu familia en una caja y largándote a buscar '
        'otra vida. Una mejor, si es posible. Así es esa lluvia de Inglaterra '
        'que mojó Silverstone en la parte final de los terceros entrenamientos'
        ' libres del GP de Inglaterra. Y por eso en esos últimos minutos con '
        'los neumáticos intermedios hubo varias salidas de pista, porque esa '
        'lluvia no es torrencial, pero duele.'
    )
    assert data.get('image_url') == '//as01.epimg.net/motor/imagenes/2017/07/15/formula_1/1500113537_936620_1500113633_noticia_normal.jpg'  # noqa

    filename = '{}-{}.json'.format(
        datetime.now().strftime('%Y-%m-%d-%H:%M'),
        slugify(data.get('headline'))
    )
    os.remove('data/{}'.format(filename))


def test_persisted_data():
    data = webcrawler.crawl('https://en.wikipedia.org/wiki/Donald_Trump')
    filename = '{}-{}.json'.format(
        datetime.now().strftime('%Y-%m-%d-%H:%M'),
        slugify(data.get('headline'))
    )

    with open('data/{}'.format(filename), 'r') as file:
        persisted_data = json.loads(file.read())
        assert data.get('headline') == persisted_data.get('headline')
        assert data.get('paragraph') == persisted_data.get('paragraph')
        assert data.get('image_url') == persisted_data.get('image_url')

    os.remove('data/{}'.format(filename))
