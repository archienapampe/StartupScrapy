from scrapy import Item, Field


class StartupUrlItem(Item):
    url = Field()