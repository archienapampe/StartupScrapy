import scrapy

from startup_scrapy.items import StartupUrlItem


class StartupUrlSpider(scrapy.Spider):
    name = 'startup_url'
    api_url = 'https://e27.co/api/startups/?all_fundraising=&pro=0&tab_name=recentlyupdated&start={}&length=100'
    start_item = 0
    start_urls = [api_url.format(start_item)]
    startup_url = 'https://e27.co/startups/{}'
    custom_settings = {
        'ITEM_PIPELINES': {
            'startup_scrapy.pipelines.DuplicatesUrlPipeline': 50,
            'startup_scrapy.pipelines.CsvUrlPipeline': 100,
        }
    }
    
    def parse(self, response):
        items = StartupUrlItem()
        self.logger.info('start scraping urls')
        
        data_json = response.json()
        data = data_json['data'].get('list')
        if data:
            for slug in data:
                items['url'] = self.startup_url.format(slug['slug'])
                yield items
            self.start_item += 100
            yield scrapy.Request(url=self.api_url.format(self.start_item), callback=self.parse)