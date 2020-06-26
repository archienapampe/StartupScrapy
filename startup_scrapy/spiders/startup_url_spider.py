import scrapy
import json

from startup_scrapy.items import StartupUrlItem


class StartupUrlSpider(scrapy.Spider):
    name = 'startup_url'
    api_url = 'https://e27.co/api/startups/?all_fundraising=&pro=0&tab_name=recentlyupdated&start={}&length=1000'
    start_item = 0
    start_urls = [api_url.format(start_item)]
    startup_url = 'https://e27.co/startups/{}'
    custom_settings = {
        'ITEM_PIPELINES': {
            'startup_scrapy.pipelines.CsvUrlPipeline': 100,
        }
    }
    
    def parse(self, response):
        items = StartupUrlItem()
        self.logger.info('start scraping urls')
        
        data_json = json.loads(response.text)
        data = data_json['data'].get('list')
        if data:
            for slug in data:
                items['url'] = self.startup_url.format(slug['slug'])
                yield items
            self.start_item += 1000
            yield scrapy.Request(url=self.api_url.format(self.start_item), callback=self.parse)