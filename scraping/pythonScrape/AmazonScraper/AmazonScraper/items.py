import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

def initialClean(string):
    return string.strip().encode("ascii", "ignore").decode().strip()

def removeHTMLChars(string):
    return string.replace('&amp;', '&').replace('&nbsp;', ' ').strip()

def removeDollarSigns(string):
    return string.replace('$', '').strip()

def removeCommas(string):
    return string.replace(',', ' ').replace('  ', ' ').strip()

class AmazonscraperItem(scrapy.Item):
    # define the fields for your item here like:
    asin = scrapy.Field(input_processor=MapCompose(initialClean, remove_tags), output_processor=TakeFirst())
    name = scrapy.Field(input_processor=MapCompose(initialClean, removeCommas, removeHTMLChars, remove_tags), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(initialClean, removeDollarSigns, remove_tags), output_processor=TakeFirst())
    rating = scrapy.Field(input_processor=MapCompose(initialClean, remove_tags), output_processor=TakeFirst())
    productlink = scrapy.Field(input_processor=MapCompose(initialClean, removeHTMLChars, remove_tags), output_processor=TakeFirst())
    imagelink = scrapy.Field(input_processor=MapCompose(initialClean, removeHTMLChars, remove_tags), output_processor=TakeFirst())
    pass
