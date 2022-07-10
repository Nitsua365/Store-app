import scrapy
from scrapy.loader import ItemLoader
from urllib.parse import urlparse

from requests.models import PreparedRequest

from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

def initialClean(string):
    return string.strip().encode("ascii", "ignore").decode().replace('\n', ' ').strip()

def removeHTMLChars(string):
    return string.replace('&amp;', '&').replace('&nbsp;', ' ').strip()

def removeDollarSigns(string):
    return string.replace('$', '').strip()

def removeCommas(string):
    return string.replace(',', ' ').replace('  ', ' ').strip()

def ratingClean(string):
    return string.strip()[:string.find(' ')]

def appendAmazonURL(string):
    return 'https://www.amazon.com' + string

def cleanQueryParams(URL):
    url_path = urlparse(URL).path
    url_prot = urlparse(URL).scheme
    url_web = urlparse(URL).netloc

    def cleanPath(path_URL):
        split_url = urlparse(path_URL).path.split('/')
        split_url.pop(len(split_url) - 1)
        split_url.pop(0)
        return '/'.join(split_url)

    url_path = cleanPath(URL) if 'ref=' in URL else url_path

    return url_prot + '://' + url_web + '/' + url_path

def addAffiliateParams(URL):
    req = PreparedRequest()
    req.prepare_url(url=URL, params={ 'tag': 'amerizon02-20', 'language': 'en_US', 'linkCode': 'll1' })
    return req.url

class AmazonscraperItem(scrapy.Item):
    # define the fields for your item here like:
    asin = scrapy.Field(input_processor=MapCompose(remove_tags, initialClean), output_processor=TakeFirst())
    productname = scrapy.Field(input_processor=MapCompose(remove_tags, removeHTMLChars, initialClean, removeCommas), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, initialClean, removeDollarSigns), output_processor=TakeFirst())
    department = scrapy.Field(input_processor=MapCompose(remove_tags, initialClean, removeHTMLChars, initialClean), output_processor=TakeFirst())
    rating = scrapy.Field(input_processor=MapCompose(remove_tags, initialClean, ratingClean), output_processor=TakeFirst())
    productpagelink = scrapy.Field(input_processor=MapCompose(remove_tags, initialClean, removeHTMLChars, appendAmazonURL, cleanQueryParams), output_processor=TakeFirst())
    affiliatelink = scrapy.Field(input_processor=MapCompose(remove_tags, initialClean, removeHTMLChars, addAffiliateParams), output_processor=TakeFirst())
    picturereflink = scrapy.Field(input_processor=MapCompose(remove_tags, initialClean, removeHTMLChars), output_processor=TakeFirst())
    manufacturer = scrapy.Field(input_processor=MapCompose(remove_tags, initialClean, removeHTMLChars), output_processor=TakeFirst())
    countryoforigin = scrapy.Field(input_processor=MapCompose(remove_tags, initialClean, removeHTMLChars), output_processor=TakeFirst())
    datescrapped = scrapy.Field()
    pass
