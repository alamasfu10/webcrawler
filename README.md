# Webcrawler
Simple webcrawler that retrieves data from Wikipedia Articles. It can also be used to retrieve data from generic pages, if params are correctly given.

The data retrieved is:
- Headline
- First paragraph
- Image


## Requirements
To run this project, you should have installed in your machine `python` (tested in both, `2.7.3` and `3.5.3`) and `virtualenv`
## Set Up
Create a virtual environment
```
$virtualenv env
```
Activate the virtual environment
```
$source env/bin/activate
```
Install the required dependencies
```
$pip install -r requirements.txt
```

## Usage
This crawler is intended to retrieve data from Wikipedia Articles by default. However it can also be configured to retrieve the relevant data from generic pages. It stores the data in `json` files inside the `data` folder. If this folder does not exist, it is automatically created.

Once you have completed the set up, to crawl pages you have to open the python console:
```
$python
```
To retireve the data from a Wikipiedia article, just pass its url as the first argument to the `crawl` function. It will automatically retrieve persist and return the data.
```
from webcrawler import crawl
crawl('https://en.wikipedia.org/wiki/Donald_Trump')
```
For generic pages, the webcrawler accepts additional kwargs in order to correctly retrieve the relevant info of the pages. We need to tell the crawler which is the HTML container of the relevant paragraphs and which is the HTML container of the relevant image. Websites should only have one `h1` element, if they are SEO optimised, so the crawler asumes they only have one.
To retrieve data from a generic page:
```
crawl(
    'http://domain/page',
    content_container_class='content_container_css_lass',
    image_container_class='image_container_css_class',
)
```
## Sample
This project comes with a sample script, that crawls the 10 [most read articles](https://en.wikipedia.org/wiki/Wikipedia:Top_25_Report). To execute this sample file, in the python console:
```
from sample import crawl_most_read_articles
crawl_most_read_articles()
```

## Tests
This project was developed following TDD, using `pytest` and `coverage`.

To run the tests:
```
$pytest
```
To run the coverage tests:
```
$py.test --cov=webcrawler test_webcrawler.py
```